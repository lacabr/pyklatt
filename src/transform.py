# -*- coding: utf-8 -*-
"""
CPSC 599 module: src.transform

Purpose
=======
 Applies rules and generates synthetic speech, given IPA input.
 
Legal
=====
 All code, unless otherwise indicated, is original, and subject to the
 terms of the GPLv2, which is provided in COPYING.
 
 (C) Neil Tallim, Sydni Bennie, 2009
"""
import re

import ipa
import language_rules
import parwave
import universal_rules

#'mnŋpbtdɾkgfvθðszʃʒhʔɹjlwʍieɛæaIəʊuoʌɔ'
_IPA_CHARACTERS = u'mn\u014bpbtd\u027ekgfv\u03b8\xf0sz\u0283\u0292h\u0294\u0279jlw\u028die\u025b\xe6aI\u0259\u028auo\u028c\u0254' #: A list of all characters the regular expression will have to deal with; not unlike an IPA [A-Z].
_WORD_REGEXP = re.compile('^((?:[*]|"|[*]"|"[*])?\'?)([%s][%s<>]*[,]?)((?:[*]|"|[*]"|"[*])?(?:[.]|[?]|!|[?]!|![?])?)$' % (_IPA_CHARACTERS, _IPA_CHARACTERS)) #: The regular expression that matches tokens in the input file.

#Sentence markup enumeration.
_SENTENCE_QUESTION = 1 #: Identifies a sentence as a question.
_SENTENCE_EXCLAMATION = 2 #: Identifies a sentence as an exclamation.

#Word markup enumeration.
_WORD_QUOTED = 1 #: Identifies a word as being quoted.
_WORD_EMPHASIZED = 2 #: Identifies a word as being emphasized.
_WORD_CONTENT = 3 #: Identifies a word as a key content item in a phrase.

def paragraphToSound(paragraph, options, synthesizer):
	"""
	Transforms a paragraph into a collection of collections of integers,
	representing synthesized speech.
	
	@type paragraph: unicode
	@param paragraph: The text to be synthesized.
	@type options: optparse.Values
	@param options: The options with which synthesis should occur.
	@type synthesizer: L{parwave.Synthesizer}
	@param synthesizer: The synthesizer to use when rendering sounds.
	
	@rtype: list
	@return: A list of tuples containing integers that represent synthesized
	    speech.
	"""
	if options.verbose:
			print u"Processing '%s'..." % (paragraph)
			
	tokens = paragraph.split()
	
	sentences = []
	while tokens:
		(sentence, tokens) = _extractSentence(tokens)
		sentences.append(sentence)
	if options.verbose:
		print "\tParagraph analyzed."
	if options.debug:
		print sentences
		
	silent_half_second = synthesizer.generateSilence(500) #Half of a second of silence.
	sounds = []
	for (i, sentence) in enumerate(sentences): #Add the sentence, plus a half-second of silence.
		sounds.append(_sentenceToSound(sentence, i + 1, len(sentences) - i - 1, options, synthesizer))
		sounds.append(silent_half_second)
	return sounds
	
def _sentenceToSound(sentence, position, remaining_sentences, options, synthesizer):
	"""
	Transforms a sentence into a collections of integers, representing
	synthesized speech.
	
	@type sentence: tuple(2)
	@param sentence: A collection of tokens comprising the words in the sentence,
	    plus the sentence's markup flags.
	@type position: int
	@param position: The current sentence's position in its paragraph,
	    indexed from 1.
	@type remaining_sentences: int
	@param remaining_sentences: The number of sentences remaining before the end
	    of the paragraph is reached, not including the current sentence.
	@type options: optparse.Values
	@param options: The options with which synthesis should occur.
	@type synthesizer: L{parwave.Synthesizer}
	@param synthesizer: The synthesizer to use when rendering sounds.
	
	@rtype: tuple
	@return: A collection of integers that represent synthesized speech.
	"""
	(words, markup) = sentence
	
	#Set markup flags.
	is_question = _SENTENCE_QUESTION in markup
	is_exclamation = _SENTENCE_EXCLAMATION in markup
	
	previous_words = []
	sounds = ()
	for (i, word) in enumerate(words):
		(new_sounds, word_characters) = _wordToSound(word, i + 1, len(words) - i - 1, previous_words, position, remaining_sentences, is_question, is_exclamation, options, synthesizer)
		previous_words.append(word_characters)
		sounds += new_sounds
	return sounds
	
def _wordToSound(word, position, remaining_words, previous_words, sentence_position, remaining_sentences, is_question, is_exclamation, options, synthesizer):
	"""
	Transforms a word into a collections of integers, representing
	synthesized speech.
	
	@type word: tuple(2)
	@param word: The word being processed, plus the word's markup flags.
	@type position: int
	@param position: The current word's position in its sentence, indexed
	    from 1.
	@type remaining_words: int
	@param remaining_words: The number of words remaining before the end of the
	    sentence is reached, not including the current word.
	@type previous_words: sequence
	@param previous_words: A collection of all words that have been previously
	    synthesized.
	@type sentence_position: int
	@param sentence_position: The current sentence's position in its paragraph,
	    indexed from 1.
	@type remaining_sentences: int
	@param remaining_sentences: The number of sentences remaining before the end
	    of the paragraph is reached, not including the current sentence.
	@type is_question: bool
	@param is_question: True if the current sentence ends with a question mark.
	@type is_exclamation: bool
	@param is_exclamation: True if the current sentence ends with an exclamation
	    mark.
	@type options: optparse.Values
	@param options: The options with which synthesis should occur.
	@type synthesizer: L{parwave.Synthesizer}
	@param synthesizer: The synthesizer to use when rendering sounds.
	
	@rtype: tuple(2)
	@return: A collection of integers that represent synthesized speech, and a
	    unicode string of characters that make up the word.
	"""
	(token, markup) = word
	
	#Determine whether the word ends with timing-affecting punctuation.
	terminal_pause = token.endswith(u',')
	if terminal_pause:
		token = token[:-1]
		
	#Set markup flags.
	is_quoted = _WORD_QUOTED in markup
	is_emphasized = _WORD_EMPHASIZED in markup
	is_content = _WORD_CONTENT in markup
	
	ipa_tokens = ipa.reduceIPAClusters(token)
	phonemes = []
	subject = ipa_tokens[0]
	multiplier = 1.0
	#For each character in the token, post-IPA-reduction, collapse extension syntax into the multiplier associated with the last-seen character.
	for i in ipa_tokens[1:]:
		if i == u'>':
			multiplier *= 1.5
		elif i == u'<':
			multiplier *= 0.5
		else:
			phonemes.append((subject, multiplier))
			subject = i
			multiplier = 1.0
	phonemes.append((subject, multiplier))
	
	characters = u''.join([phoneme for (phoneme, multiplier) in phonemes])
	if options.verbose:
		print u"\tSynthesizing '%s'..." % (characters)
		
	sounds = ()
	for (i, phoneme) in enumerate(phonemes):
		sounds += _phonemeToSound(phoneme, [p for (p, d) in phonemes[:i]], [p for (p, d) in phonemes[i + 1:]], position, remaining_words, previous_words, sentence_position, remaining_sentences, is_quoted, is_emphasized, is_content, is_question, is_exclamation, options, synthesizer)
	if terminal_pause: #Add a quarter of a second of silence.
		sounds += synthesizer.generateSilence(250)
	return (sounds, characters)
	
def _phonemeToSound(phoneme, preceding_phonemes, following_phonemes, word_position, remaining_words, previous_words, sentence_position, remaining_sentences, is_quoted, is_emphasized, is_content, is_question, is_exclamation, options, synthesizer):
	"""
	Transforms a phoneme into a collections of integers, representing
	synthesized speech.
	
	@type phoneme: tuple(2)
	@param word: The IPA character being processed, plus the phoneme's
	    duration multiplier.
	@type preceding_phonemes: sequence
	@param preceding_phonemes: A collection of all phonemes, in order, that
	    precede the current IPA character in the current word.
	@type following_phonemes: sequence
	@param following_phonemes: A collection of all phonemes, in order, that
	    follow the current IPA character in the current word.
	@type word_position: int
	@param word_position: The current word's position in its sentence, indexed
	    from 1.
	@type remaining_words: int
	@param remaining_words: The number of words remaining before the end of the
	    sentence is reached, not including the current word.
	@type previous_words: sequence
	@param previous_words: A collection of all words that have been previously
	    synthesized.
	@type sentence_position: int
	@param sentence_position: The current sentence's position in its paragraph,
	    indexed from 1.
	@type remaining_sentences: int
	@param remaining_sentences: The number of sentences remaining before the end
	    of the paragraph is reached, not including the current sentence.
	@type is_quoted: bool
	@param is_quoted: True if the current word is part of a quoted body.
	@type is_emphasized: bool
	@param is_emphasized: True if the current word is part of an emphasized body.
	@type is_content: bool
	@param is_content: True if the current word was marked as a content word.
	@type is_question: bool
	@param is_question: True if the current sentence ends with a question mark.
	@type is_exclamation: bool
	@param is_exclamation: True if the current sentence ends with an exclamation
	    mark.
	@type options: optparse.Values
	@param options: The options with which synthesis should occur.
	@type synthesizer: L{parwave.Synthesizer}
	@param synthesizer: The synthesizer to use when rendering sounds.
	
	@rtype: tuple
	@return: A collection of integers that represent synthesized speech.
	"""
	(ipa_character, duration_multiplier) = phoneme
	
	#Retrieve synthesis parameters.
	(parameters, regions) = ipa.IPA_DATA[ipa_character]
	
	#Parameters need to be mutable.
	parameters = list(parameters)
	parameters[-1] = int(parameters[-1] * duration_multiplier) #Adjust the duration based on markup.
	#Universal rules may append additional steps, so there needs to be a list of parameters.
	parameters_list = [parameters]
	
	#Apply vowel nasalization.
	parameters_list = universal_rules.nasalizeVowel(ipa_character, following_phonemes, parameters_list)
	
	#Apply liasons.
	parameters_list = universal_rules.bridgeWords(ipa_character, preceding_phonemes, following_phonemes, previous_words, parameters_list)
	
	#Apply contour-shaping.
	parameters_list = universal_rules.shapeContours(ipa_character, preceding_phonemes, following_phonemes, parameters_list)
	
	#Apply language-specific rules to the parameters.
	(parameters_list, f0_multipliers) = language_rules.applyRules(ipa_character, preceding_phonemes, following_phonemes, word_position, remaining_words, previous_words, sentence_position, remaining_sentences, is_quoted, is_emphasized, is_content, is_question, is_exclamation, parameters_list)
	
	#Synthesize sound.
	sounds = ()
	for (parameters, f0_multiplier) in zip(parameters_list, f0_multipliers):
		if options.debug:
			print parameters
		sounds += synthesizer.synthesize(parameters, f0_multiplier)
	return sounds
	
def _extractSentence(tokens):
	"""
	Reads through the token stream to assemble the next sentence, applying
	context evaluation to its elements along the way.
	
	@type tokens: list
	@param tokens: A list of all tokens remaining in the input data.
	
	@rtype: tuple(2)
	@return: A tuple containing every token that forms a word in the extracted
	    sentence, plus flags that describe the sentence's nature, and a list of
	    all remaining tokens that form successive sentences.
	"""
	#Cache commonly-referenced variables in the local scope for efficiency.
	word_regexp = _WORD_REGEXP
	word_quoted = _WORD_QUOTED
	word_emphasized = _WORD_EMPHASIZED
	word_content = _WORD_CONTENT
	
	words = []
	markup = []
	
	quotation = False
	emphasis = False
	while tokens:
		token = tokens.pop(0) #Get the first token remaining in the queue.
		match = word_regexp.match(token) #Break the token into its component elements.
		if not match:
			raise ValueError(u"Invalid token in IPA input: %s" % (token))
			
		#Set word-level markup flags.
		if '"' in match.group(1):
			quotation = True
		if '*' in match.group(1):
			emphasis = True
			
		#Describe and record the word in the sentence's token-list.
		word_markup = []
		if quotation:
			word_markup.append(word_quoted)
		if emphasis:
			word_markup.append(word_emphasized)
		if "'" in match.group(1):
			word_markup.append(word_content)
		words.append((match.group(2), tuple(word_markup)))
		
		#Unset word-level markup flags.
		if '"' in match.group(3):
			quotation = False
		if '*' in match.group(3):
			emphasis = False
			
		#Look for the end of the sentence, and set sentence-level markup flags.
		if '.' in match.group(3):
			break
		elif '?' in match.group(3):
			markup.append(_SENTENCE_QUESTION)
			if '!' in match.group(3):
				markup.append(_SENTENCE_EXCLAMATION)
			break
		elif '!' in match.group(3):
			if '?' in match.group(3):
				markup.append(_SENTENCE_QUESTION)
			markup.append(_SENTENCE_EXCLAMATION)
			break
	return ((tuple(words), tuple(markup)), tokens)
	