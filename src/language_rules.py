# -*- coding: utf-8 -*-
"""
Klatt CPSC 599 module: src.language_rules

Purpose
=======
 Contains a collection of rules to apply to phonemes, specific to Canadian
 English.
 
Legal
=====
 All code, unless otherwise indicated, is original, and subject to the
 terms of the GPLv2, which is provided in COPYING.
 
 (C) Neil Tallim, Sydni Bennie, 2009
"""
import ipa

def applyRules(parameters_list, ipa_character, preceding_sounds, following_sounds, word_position, remaining_words, sentence_position, remaining_sentences, is_quoted, is_emphasized, is_question, is_exclamation):
	transformed_parameters = []
	
	for parameters in parameters_list:
		"""
		feed data to appropriate function, storing returned parameters elements in transformed_parameters
		this happens using the EXACT SAME data for each parameters element in parameters_list
		"""
		transformed_parameters.append(parameters)
	return transformed_parameters
	