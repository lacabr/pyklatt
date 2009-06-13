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
	Lops off 0.05s from the end of the current sound, if it's a vowel followed by
	a nasal, and inserts 0.05s of two nasalized variants of the vowel's
	parameters.
	
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
	if not ipa_character in ipa.VOWELS:
		return parameters_list
		
	parameters_list = parameters_list[:] #Make a local copy.
	
	#Unpack the base parameters.
	(fgp, fgz, fgs, fnp, fnz,
	 f1, f2, f3, f4, f5, f6,
	 bgp, bgz, bgs, bnp, bnz,
	 bw1, bw2, bw3, bw4, bw5, bw6,
	 a2, a3, a4, a5, a6,
	 ab, ah, af, av, avs,
	 duration) = parameters_list[0]
	
	#Reduce duration by 50ms.
	parameters_list[0] = [
	 fgp, fgz, fgs, fnp, fnz,
	 f1, f2, f3, f4, f5, f6,
	 bgp, bgz, bgs, bnp, bnz,
	 bw1, bw2, bw3, bw4, bw5, bw6,
	 a2, a3, a4, a5, a6,
	 ab, ah, af, av, avs,
	 max(50, duration - 50)]
	 
	#Add nasalized terminator.
	parameters_list.insert(1, [
	 fgp, fgz, fgs, 270, 450,
	 f1 + 100, f2 + 100, f3 + 100, f4, f5, f6,
	 bgp, bgz, bgs, bnp, bnz,
	 min(40, bw1 - 10), bw2 * 1.25, max(300, bw3 * 1.5), bw4, bw5, bw6,
	 a2, a3, a4, a5, a6,
	 ab, ah, af, 50, 30,
	 25]
	)
	#Add half-nasalized step.
	parameters_list.insert(1, [
	 fgp, fgz, fgs, 250, 400,
	 f1 + 50, f2 + 50, f3 + 50, f4, f5, f6,
	 bgp, bgz, bgs, bnp, bnz,
	 min(40, bw1 - 10), bw2 * 1.125, max(300, bw3 * 1.25), bw4, bw5, bw6,
	 a2, a3, a4, a5, a6,
	 ab, ah, af, 50, 30,
	 25]
	)
	
	return parameters_list
	