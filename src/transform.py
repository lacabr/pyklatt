# -*- coding: utf-8 -*-
"""
Klatt CPSC 599 module: src.transform

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

_WORD_REGEXP = re.compile('([*"]*)(\w[\w<>]+[:,]?)([*".!?]*)')

_SENTENCE_QUESTION = 1
_SENTENCE_EXCLAMATION = 2

_WORD_QUOTED = 1
_WORD_EMPHASIZED = 2

def paragraphToSound(paragraph, options, synthesizer):
	tokens = paragraph.split()
	
	sentences = []
	while tokens:
		(sentence, tokens) = _extractSentence(tokens)
		sentences.append(sentence)
	if options.verbose:
		print "\tParagraph analyzed."
	if options.debug:
		print sentences
		
	silent_half_second = ((0,) * (options.samples_per_frame / 2))
	sounds = []
	for (i, sentence) in enumerate(sentences): #Add the sentence, plus a half-second of silence.
		sounds.append(_sentenceToSound(sentence, i + 1, len(sentences) - i - 1, options, synthesizer))
		sounds.append(silent_half_second)
	return sounds
	
def _sentenceToSound(sentence, position, remaining_sentences, options, synthesizer):
	(words, markup) = sentence
	
	is_question = _SENTENCE_QUESTION in markup
	is_exclamation = _SENTENCE_EXCLAMATION in markup
	
	silent_sixth_second = ((0,) * (options.samples_per_frame / 6))
	sounds = ()
	for (i, word) in enumerate(words): #Add the word, plus a sixth of a second of silence.
		sounds += _wordToSound(word, i + 1, len(words) - i - 1, sentence_position, remaining_sentences, is_question, is_exclamation, options, synthesizer)) + silent_sixth_second
	return sounds
	
def _wordToSound(word, position, remaining_words, sentence_position, remaining_sentences, is_question, is_exclamation, options, synthesizer):
	(token, markup) = word
	
	is_quoted = _WORD_QUOTED in markup
	is_emphasized = _WORD_EMPHASIZED in markup
	
	terminal_pause = ()
	if token.endswidth((',', ':')):
		terminal_pause = ((0,) * (options.samples_per_frame / 6)) #A sixth of a second of silence.
		token = token[:-1]
		
	phonemes = []
	multiplier = 1.0
	subject = token[0]
	for i in token[1:]:
		if i == '>':
			multiplier *= 1.5
		elif i == '<':
			multiplier *= 0.5
		else:
			phonemes.append((subject, multiplier))
			subject = i
			multiplier = 1.0
	phonemes.append((subject, multiplier))
	
	if options.verbose:
		print "\tSynthesizing '%s'..." % (''.join([phoneme for (phoneme, multiplier) in phonemes]))
		
	synthesizer.reset()
	sounds = ()
	for (i, phoneme) in enumerate(phonemes):
		sounds += _phonemeToSound(phoneme, [p for (p, d) in phonemes[:i]], [p for (p, d) in phonemes[i + 1:]], position, remaining_words, sentence_position, remaining_sentences, is_quoted, is_emphasized, is_question, is_exclamation, options, synthesizer)
	return sounds
	
def _phonemeToSound(phoneme, preceding_sounds, following_sounds, word_position, remaining_words, sentence_position, remaining_sentences, is_quoted, is_emphasized, is_question, is_exclamation, options, synthesizer):
	(ipa_character, duration_multiplier) = phoneme
	
	#Retrieve synthesis parameters.
	regions = None
	(handled, parameters) = ipa.screenIPAClusters(ipa_character, preceding_sounds, following_sounds)
	if handled:
		if parameters is None: #Second half of a cluster.
			return ()
		regions = ipa.IPA_REGIONS[ipa_character]
	elif not handled: #Look up the synthesis parameters.
		(parameters, regions) = ipa.IPA_DATA[ipa_character]
		
	#Parameters need to be mutable.
	parameters = list(parameters)
	parameters[-1] = int(parameters[-1] * duration_multiplier) #Adjust the duration based on markup.
	#Universal rules may append additional steps, so there needs to be a list of parameters.
	parameters_list = [parameters]
	
	#Apply universal rules to the parameters.
	parameters_list = universal_rules.nasalizeVowel(ipa_character, following_sounds, parameters_list)
	
	#Apply language-specific rules to the parameters.
	parameters_list = language_rules.applyRules(parameters_list, ipa_character, preceding_sounds, following_sounds, word_position, remaining_words, sentence_position, remaining_sentences, is_quoted, is_emphasized, is_question, is_exclamation)
	
	#Synthesize sound.
	sounds = ()
	for parameters in parameters_list:
		if options.debug:
			print parameters
		sounds += synthesizer.synthesize(parameters)
	return sounds
	
def _extractSentence(tokens):
	word_regexp = _WORD_REGEXP
	word_quoted = _WORD_QUOTED
	word_emphasized = _WORD_EMPHASIZED
	
	words = []
	markup = []
	
	quotation = False
	emphasis = False
	while tokens:
		token = tokens.pop(0)
		match = word_regexp.match(token)
		if not match:
			raise ValueError("Invalid token in IPA input: %s" % (token))
			
		if '"' in match.group(0):
			quotation = True
		if '*' in match.group(0):
			emphasis = True
			
		word_markup = []
		if quotation:
			word_markup.append(word_quoted)
		if emphasis:
			word_markup.append(word_emphasized)
		if word_markup:
			word_markup = tuple(word_markup)
		else:
			word_markup = None
		words.append((match.group(1), word_markup))
		
		if '"' in match.group(2):
			quotation = False
		if '*' in match.group(2):
			emphasis = False
			
		if '.' in match.group(2):
			break
		elif '?' in match.group(2):
			markup.append(_SENTENCE_QUESTION)
			if '!' in match.group(2):
				markup.append(_SENTENCE_EXCLAMATION)
			break
		elif '!' in match.group(2):
			if '?' in match.group(2):
				markup.append(_SENTENCE_QUESTION)
			markup.append(_SENTENCE_EXCLAMATION)
			break
			
	if markup:
		markup = tuple(markup)
	else:
		markup = None
	return ((words, markup), tokens)
	