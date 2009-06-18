# -*- coding: utf-8 -*-
"""
CPSC 599 module: src.language_rules

Purpose
=======
 Contains a collection of rules to apply to phonemes.
 
Language
========
 This file applies to Canadian English.
 
Legal
=====
 All code, unless otherwise indicated, is original, and subject to the
 terms of the GPLv2, which is provided in COPYING.
 
 (C) Neil Tallim, Sydni Bennie, 2009
"""
import ipa

def applyRules(ipa_character, preceding_phonemes, following_phonemes, word_position, remaining_words, previous_words, sentence_position, remaining_sentences, is_quoted, is_emphasized, is_content, is_question, is_exclamation, parameters_list):
	"""
	Iterates through all parameters that make up the current phoneme, applying
	all applicable language-specific rules, in a specific order, to each
	parameter-set.
	
	The input list of parameters is not altered by this function.
	
	@type ipa_character: unicode
	@param ipa_character: The character, representative of a phoneme, being
	    processed.
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
	@type parameters_list: list
	@param parameters_list: A collection of all sounds currently associated with
	    the phoneme being processed.
	
	@rtype: tuple(2)
	@return: An updated list of parameters, consisting of transformations of
	    the base sounds, plus anything added to the stream, and a f0 multiplier
	    value, with higher numbers meaning lower-pitched sounds.
	"""
	f0_multipliers = []
	transformed_parameters = []
	for parameters in parameters_list: #Transforms each parameter-set in the input-list, in order.
		parameters = parameters[:] #Make a local copy.
		f0_multiplier = 1.0
		preceding_parameters = []
		following_parameters = []
		for function in _ORDERED_FUNCTIONS: #Applies each language rule, in order. New parameters lists appear on either side of the central parameter set.
			(preceding_params, following_params, multiplier) = function(ipa_character, preceding_phonemes, following_phonemes, word_position, remaining_words, previous_words, sentence_position, remaining_sentences, is_quoted, is_emphasized, is_content, is_question, is_exclamation, parameters)
			f0_multiplier *= multiplier
			preceding_parameters = preceding_parameters + preceding_params
			following_parameters = following_params + following_parameters
			
		#Add everything that came out of the process to the parameters lists.
		transformed_parameters += preceding_parameters + [parameters] + following_parameters
		f0_multipliers += [f0_multiplier] * (len(preceding_parameters) + 1 + len(following_parameters))
	return (transformed_parameters, f0_multipliers)
	
def _inflectQuestionPitch(ipa_character, preceding_phonemes, following_phonemes, word_position, remaining_words, previous_words, sentence_position, remaining_sentences, is_quoted, is_emphasized, is_content, is_question, is_exclamation, parameters):
	"""
	Changes the pitch at the end of a question-sentence, rising in most cases,
	and falling in the case of a 'wh' question.
	
	This function may modify the input parameter-set.
	
	@type ipa_character: unicode
	@param ipa_character: The character, representative of a phoneme, being
	    processed.
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
	@type parameters: list(33)
	@param parameters: A collection of parameters associated with the sound
	    currently being procesed.
	
	@rtype: tuple(3)
	@return: A list of parameter-sets that precede this sound, a list of
	    parameter-sets that follow this sound, and an f0 multiplier.
	
	@author: Sydni Bennie
	"""
	if is_question and remaining_words <= 1: #Ignore questions and early positions in sentences.
		if previous_words:
			first_word = previous_words[0]
			if first_word[0] == 'w' and first_word != u'w\u028ad': #If it starts with 'would' (wʊd)...
				return _inflectQuestionPitch_fall(remaining_words)
				
		if remaining_words == 0:
			return _inflectQuestionPitch_rise()
			
	return ([], [], 1.0)
	
def _inflectQuestionPitch_rise():
	"""
	Implements the rising-intonation branch of question-inflection.
	
	@rtype: tuple(3)
	@return: A list of parameter-sets that precede this sound, a list of
	    parameter-sets that follow this sound, and an f0 multiplier.
	
	@author: Sydni Bennie
	"""
	return ([], [], 0.8) #Increase pitch.
	
def _inflectQuestionPitch_fall(remaining_words):
	"""
	Implements the falling-intonation branch of question-inflection.
	
	@type remaining_words: int
	@param remaning_words: The number of words remaining before the end of the
	    sentence is reached, not including the current word.
	
	@rtype: tuple(3)
	@return: A list of parameter-sets that precede this sound, a list of
	    parameter-sets that follow this sound, and an f0 multiplier.
	
	@author: Sydni Bennie
	"""
	if remaining_words == 1:
		return ([], [], 1.1) #Lower pitch slightly on the second-last word.
	return ([], [], 1.2) #Lower pitch a bit more on the last word.
	
def _amplifyContent(ipa_character, preceding_phonemes, following_phonemes, word_position, remaining_words, previous_words, sentence_position, remaining_sentences, is_quoted, is_emphasized, is_content, is_question, is_exclamation, parameters):
	"""
	Increases the emphasis placed on a word identified as content-bearing in a
	sentence.
	
	This function may modify the input parameter-set.
	
	@type ipa_character: unicode
	@param ipa_character: The character, representative of a phoneme, being
	    processed.
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
	@type parameters: list(33)
	@param parameters: A collection of parameters associated with the sound
	    currently being procesed.
	
	@rtype: tuple(3)
	@return: A list of parameter-sets that precede this sound, a list of
	    parameter-sets that follow this sound, and an f0 multiplier.
	
	@author: Sydni Bennie
	"""
	if is_content:
		parameters[5] *= 1.25 #Boost f1.
		if ipa_character in ipa.VOWELS:
			parameters[32] *= 1.05 #Increase duration, just a little.
			return ([], [], 0.95) #Increase pitch, just a little.
	return ([], [], 1.0)
	
	
_ORDERED_FUNCTIONS = (
 _inflectQuestionPitch,
 _amplifyContent,
) #: A collection of all functions to call, in order, to apply this language's rules. 
