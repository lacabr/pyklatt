# -*- coding: utf-8 -*-
"""
Klatt CPSC 599 module: src.universal_rules

Purpose
=======
 Contains a collection of rules to apply to phonemes, regardless of language.
 
Legal
=====
 All code, unless otherwise indicated, is original, and subject to the
 terms of the GPLv2, which is provided in COPYING.
 
 Nasalization concept inspired by a function described in "Klatt Synthesizer
 in Simulink®", a graduate research paper written by Sean McLennan in 2000 for
 S522 - Digital Signal Processing under Dr. Diane Kewley-Port at Indiana
 University. This information, lacking in-text licensing terms, is presumed to
 have been published as public-domain work or otherwise under terms agreeable to
 non-commercial academic research.
 
 The referenced paper was retrieved from
 http://www.shaav.com/professional/linguistics/klatt.pdf on June 7th, 2009.
 
 (C) Neil Tallim, Sydni Bennie, 2009
"""
import ipa

def nasalizeVowel(ipa_character, following_sounds, parameters):
	"""
	Lops off 0.1s from the end of the current sound, if it's a vowel followed by
	a nasal, and inserts 0.1s of a nasalized variant of the vowel's parameters.
	
	@author: Neil Tallim
	"""
	if not following_sounds or not following_sounds[0] in ipa.NASALS:
		return parameters
	if not ipa_character in ipa.VOWELS:
		return parameters
		
	(fgp, fgz, fgs, fnp, fnz,
	 f1, f2, f3, f4, f5, f6,
	 bgp, bgz, bgs, bnp, bnz,
	 bw1, bw2, bw3, bw4, bw5, bw6,
	 a2, a3, a4, a5, a6,
	 ab, ah, af, av, avs,
	 duration) = parameters[0]
	
	parameters[0][-1] = min(100, duration - 100)
	parameters.insert(0, (fgp, fgz, fgs, 270, 450,
	 f1 + 100, f2 + 100, f3 + 100, f4, f5, f6,
	 bgp, bgz, bgs, bnp, bnz,
	 min(40, bw1 - 10), bw2 * 1.25, max(300, bw3 * 1.5), bw4, bw5, bw6,
	 a2, a3, a4, a5, a6,
	 ab, ah, af, 50, 30,
	 100)
	)
	