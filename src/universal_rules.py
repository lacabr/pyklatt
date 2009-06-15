# -*- coding: utf-8 -*-
"""
CPSC 599 module: src.universal_rules

Purpose
=======
 Contains a collection of rules to apply to phonemes, regardless of language.
 
Legal
=====
 All code, unless otherwise indicated, is original, and subject to the
 terms of the GPLv2, which is provided in COPYING.
 
 (C) Neil Tallim, Sydni Bennie, 2009
"""
import ipa

def nasalizeVowel(ipa_character, following_phonemes, parameters_list):
	"""
	Lops off half of the current sound, if it's a vowel followed by a nasal, and
	inserts one sixth and one third of its duration as two nasalized variants of
	the vowel's parameters.
	
	The input list of parameters is not altered by this function.
	
	Nasalization concept inspired by a function described in "Klatt Synthesizer
	in Simulink®", a graduate research paper written by Sean McLennan in 2000 for
	S522 - Digital Signal Processing under Dr. Diane Kewley-Port at Indiana
	University. This information, lacking in-text licensing terms, is presumed to
	have been published as public-domain work or otherwise under terms agreeable
	to non-commercial academic research.
	
	The referenced paper was retrieved from
	http://www.shaav.com/professional/linguistics/klatt.pdf on June 7th, 2009.
	
	@type ipa_character: unicode
	@param ipa_character: The character, representative of a phoneme, being
	    processed.
	@type following_phonemes: sequence
	@param following_phonemes: A collection of all phonemes, in order, that
	    follow the current IPA character in the current word.
	@type parameters_list: list
	@param parameters_list: A collection of all sounds currently associated with
	    the IPA character being processed. The first element is assumed to be the
	    base sound, and any additional sounds will be inserted immediately after
	    it, occupying indecies 1 and 2 and offsetting any other elements in the
	    list.
	
	@rtype: list
	@return: An updated list of parameters.
	
	@author: Neil Tallim
	"""
	if not following_phonemes or not following_phonemes[0] in ipa.NASALS:
		return parameters_list
	if not ipa_character in ipa.VOWELS or ipa_character in ipa.NASALS:
		return parameters_list
		
	parameters_list = parameters_list[:] #Make a local copy.
	
	#Extract vowel parameters.
	vowel = parameters_list[0]
	vowel_duration = vowel[32]
	vowel_values = vowel[:32]
	
	#Multiplex the nasal and vowel values.
	values = zip(vowel_values, ipa.IPA_PARAMETERS[following_phonemes[0]][:32])
	
	#Reduce vowel duration by 50%.
	parameters_list[0] = vowel_values + [int(vowel_duration * 0.5)]
	#Add nazalized lead-in = 1/3 nasalized sound, 2/3 base vowel.
	parameters_list.insert(1, [(v * 2 + n) / 3 for (v, n) in values] + [int(vowel_duration * 0.167)])
	#Add nasalized terminator = 2/3 nasalized sound, 1/3 base vowel.
	parameters_list.insert(2, [(v + n * 2) / 3 for (v, n) in values] + [int(vowel_duration * 0.333)])
	
	return parameters_list
	