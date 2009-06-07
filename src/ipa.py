# -*- coding: utf-8 -*-
"""
Klatt CPSC 599 module: src.ipa

Purpose
=======
 Provides IPA-to-parameter lookup functions.
 
Limitations
===========
 At present, only the following IPA symbols are supported:
  mnŋpbtdkgfvθðszʃʒhɹjwl
  ieɛæaIəʊuoʌɔ
 
Legal
=====
 All code, unless otherwise indicated, is original, and subject to the
 terms of the GPLv2, which is provided in COPYING.
 
 Resonator data and interpretation logic derived from "Klatt Synthesizer in
 Simulink®", a graduate research paper written by Sean McLennan in 2000 for
 S522 - Digital Signal Processing under Dr. Diane Kewley-Port at Indiana
 University. This information, lacking in-text licensing terms, is presumed to
 have been published as public-domain work or otherwise under terms agreeable to
 non-commercial academic research.
 
 The referenced paper was retrieved from
 http://www.shaav.com/professional/linguistics/klatt.pdf on June 7th, 2009.
 
 (C) Neil Tallim, Sydni Bennie, 2009
"""
LABIAL = 1
CORONAL = 2
DORSAL = 3
RADICAL = 4
GLOTTAL = 5

FRONT = 1
NEAR_FRONT = 2
CENTRAL = 3
NEAR_BACK = 4
BACK = 5

_IPA_MAPPING = {
 'm': {
  'freq-glottal-pole': 0,
  'freq-glottal-zero': 1500,
  'freq-glottal-sine': 0,
  'freq-nasal-pole': 270,
  'freq-nasal-zero': 450,
  'freq (1-6)': (480, 1270, 2130, 3300, 3750, 4900),
  'bwidth-glottal-pole': 100,
  'bwidth-glottal-zero': 6000,
  'bwidth-glottal-sine': 100,
  'bwidth-nasal-pole': 100,
  'bwidth-nasal-zero': 100,
  'bwidth (1-6)': (40, 200, 200, 250, 200, 1000),
  'formant-gain (2-6)': (0, 0, 0, 0, 0),
  'formant-bypass-gain': 0,
  'formant-cascade-gain': 0,
  'formant-parallel-gain': 0,
  'voicing-linear-gain': 40,
  'voicing-sine-gain': 50,
  'nominal-duration': 150,
  'vowel': False,
  'nasal': True,
  'regions': [LABIAL]
 },
 'n': {
  'freq-glottal-pole': 0,
  'freq-glottal-zero': 1500,
  'freq-glottal-sine': 0,
  'freq-nasal-pole': 270,
  'freq-nasal-zero': 450,
  'freq (1-6)': (480, 1340, 2470, 3300, 3750, 4900),
  'bwidth-glottal-pole': 100,
  'bwidth-glottal-zero': 6000,
  'bwidth-glottal-sine': 100,
  'bwidth-nasal-pole': 100,
  'bwidth-nasal-zero': 100,
  'bwidth (1-6)': (40, 300, 300, 250, 200, 1000),
  'formant-gain (2-6)': (0, 0, 0, 0, 0),
  'formant-bypass-gain': 0,
  'formant-cascade-gain': 0,
  'formant-parallel-gain': 0,
  'voicing-linear-gain': 40,
  'voicing-sine-gain': 50,
  'nominal-duration': 150,
  'vowel': False,
  'nasal': True,
  'regions': [CORONAL]
 },
 'ŋ': {
  'freq-glottal-pole': 0,
  'freq-glottal-zero': 1500,
  'freq-glottal-sine': 0,
  'freq-nasal-pole': 270,
  'freq-nasal-zero': 450,
  'freq (1-6)': (480, 2000, 2900, 3300, 3750, 4900),
  'bwidth-glottal-pole': 100,
  'bwidth-glottal-zero': 6000,
  'bwidth-glottal-sine': 100,
  'bwidth-nasal-pole': 100,
  'bwidth-nasal-zero': 100,
  'bwidth (1-6)': (40, 300, 300, 250, 200, 1000),
  'formant-gain (2-6)': (0, 0, 0, 0, 0),
  'formant-bypass-gain': 0,
  'formant-cascade-gain': 0,
  'formant-parallel-gain': 0,
  'voicing-linear-gain': 40,
  'voicing-sine-gain': 50,
  'nominal-duration': 150,
  'vowel': False,
  'nasal': True,
  'regions': [DORSAL]
 },
 'p': {
  'freq-glottal-pole': 0,
  'freq-glottal-zero': 1500,
  'freq-glottal-sine': 0,
  'freq-nasal-pole': 250,
  'freq-nasal-zero': 250,
  'freq (1-6)': (400, 1100, 2150, 3300, 3750, 4900),
  'bwidth-glottal-pole': 100,
  'bwidth-glottal-zero': 6000,
  'bwidth-glottal-sine': 100,
  'bwidth-nasal-pole': 100,
  'bwidth-nasal-zero': 100,
  'bwidth (1-6)': (300, 150, 220, 250, 200, 1000),
  'formant-gain (2-6)': (0, 0, 0, 0, 0),
  'formant-bypass-gain': 63,
  'formant-cascade-gain': 0,
  'formant-parallel-gain': 20,
  'voicing-linear-gain': 0,
  'voicing-sine-gain': 0,
  'nominal-duration': 150,
  'vowel': False,
  'nasal': False,
  'regions': [LABIAL]
 },
 'b': {
  'freq-glottal-pole': 0,
  'freq-glottal-zero': 1500,
  'freq-glottal-sine': 0,
  'freq-nasal-pole': 250,
  'freq-nasal-zero': 250,
  'freq (1-6)': (200, 1100, 2150, 3300, 3750, 4900),
  'bwidth-glottal-pole': 100,
  'bwidth-glottal-zero': 6000,
  'bwidth-glottal-sine': 100,
  'bwidth-nasal-pole': 100,
  'bwidth-nasal-zero': 100,
  'bwidth (1-6)': (60, 100, 130, 250, 200, 1000),
  'formant-gain (2-6)': (0, 0, 0, 0, 0),
  'formant-bypass-gain': 63,
  'formant-cascade-gain': 0,
  'formant-parallel-gain': 10,
  'voicing-linear-gain': 20,
  'voicing-sine-gain': 20,
  'nominal-duration': 150,
  'vowel': False,
  'nasal': False,
  'regions': [LABIAL]
 },
 't': {
  'freq-glottal-pole': 0,
  'freq-glottal-zero': 1500,
  'freq-glottal-sine': 0,
  'freq-nasal-pole': 250,
  'freq-nasal-zero': 250,
  'freq (1-6)': (400, 1600, 2600, 3300, 3750, 4900),
  'bwidth-glottal-pole': 100,
  'bwidth-glottal-zero': 6000,
  'bwidth-glottal-sine': 100,
  'bwidth-nasal-pole': 100,
  'bwidth-nasal-zero': 100,
  'bwidth (1-6)': (300, 120, 250, 250, 200, 1000),
  'formant-gain (2-6)': (0, 15, 23, 28, 32),
  'formant-bypass-gain': 0,
  'formant-cascade-gain': 0,
  'formant-parallel-gain': 20,
  'voicing-linear-gain': 0,
  'voicing-sine-gain': 0,
  'nominal-duration': 150,
  'vowel': False,
  'nasal': False,
  'regions': [CORONAL]
 },
 'd': {
  'freq-glottal-pole': 0,
  'freq-glottal-zero': 1500,
  'freq-glottal-sine': 0,
  'freq-nasal-pole': 250,
  'freq-nasal-zero': 250,
  'freq (1-6)': (200, 1600, 2600, 3300, 3750, 4900),
  'bwidth-glottal-pole': 100,
  'bwidth-glottal-zero': 6000,
  'bwidth-glottal-sine': 100,
  'bwidth-nasal-pole': 100,
  'bwidth-nasal-zero': 100,
  'bwidth (1-6)': (60, 100, 170, 250, 200, 1000),
  'formant-gain (2-6)': (0, 23, 30, 31, 30),
  'formant-bypass-gain': 0,
  'formant-cascade-gain': 0,
  'formant-parallel-gain': 10,
  'voicing-linear-gain': 20,
  'voicing-sine-gain': 20,
  'nominal-duration': 150,
  'vowel': False,
  'nasal': False,
  'regions': [CORONAL]
 },
 'k': {
  'freq-glottal-pole': 0,
  'freq-glottal-zero': 1500,
  'freq-glottal-sine': 0,
  'freq-nasal-pole': 250,
  'freq-nasal-zero': 250,
  'freq (1-6)': (300, 1990, 2850, 3300, 3750, 4900),
  'bwidth-glottal-pole': 100,
  'bwidth-glottal-zero': 6000,
  'bwidth-glottal-sine': 100,
  'bwidth-nasal-pole': 100,
  'bwidth-nasal-zero': 100,
  'bwidth (1-6)': (250, 160, 330, 250, 200, 1000),
  'formant-gain (2-6)': (30, 26, 22, 23, 23),
  'formant-bypass-gain': 0,
  'formant-cascade-gain': 0,
  'formant-parallel-gain': 20,
  'voicing-linear-gain': 0,
  'voicing-sine-gain': 0,
  'nominal-duration': 150,
  'vowel': False,
  'nasal': False,
  'regions': [DORSAL]
 },
 'g': {
  'freq-glottal-pole': 0,
  'freq-glottal-zero': 1500,
  'freq-glottal-sine': 0,
  'freq-nasal-pole': 250,
  'freq-nasal-zero': 250,
  'freq (1-6)': (200, 1990, 2850, 3300, 3750, 4900),
  'bwidth-glottal-pole': 100,
  'bwidth-glottal-zero': 6000,
  'bwidth-glottal-sine': 100,
  'bwidth-nasal-pole': 100,
  'bwidth-nasal-zero': 100,
  'bwidth (1-6)': (60, 150, 280, 250, 200, 1000),
  'formant-gain (2-6)': (30, 27, 22, 23, 23),
  'formant-bypass-gain': 0,
  'formant-cascade-gain': 0,
  'formant-parallel-gain': 10,
  'voicing-linear-gain': 20,
  'voicing-sine-gain': 20,
  'nominal-duration': 150,
  'vowel': False,
  'nasal': False,
  'regions': [DORSAL]
 },
 'f': {
  'freq-glottal-pole': 0,
  'freq-glottal-zero': 1500,
  'freq-glottal-sine': 0,
  'freq-nasal-pole': 250,
  'freq-nasal-zero': 250,
  'freq (1-6)': (340, 1100, 2080, 3300, 3750, 4900),
  'bwidth-glottal-pole': 100,
  'bwidth-glottal-zero': 6000,
  'bwidth-glottal-sine': 100,
  'bwidth-nasal-pole': 100,
  'bwidth-nasal-zero': 100,
  'bwidth (1-6)': (200, 120, 150, 250, 200, 1000),
  'formant-gain (2-6)': (0, 0, 0, 0, 0),
  'formant-bypass-gain': 57,
  'formant-cascade-gain': 0,
  'formant-parallel-gain': 20,
  'voicing-linear-gain': 0,
  'voicing-sine-gain': 0,
  'nominal-duration': 150,
  'vowel': False,
  'nasal': False,
  'regions': [LABIAL]
 },
 'v': {
  'freq-glottal-pole': 0,
  'freq-glottal-zero': 1500,
  'freq-glottal-sine': 0,
  'freq-nasal-pole': 250,
  'freq-nasal-zero': 250,
  'freq (1-6)': (220, 1100, 2080, 3300, 3750, 4900),
  'bwidth-glottal-pole': 100,
  'bwidth-glottal-zero': 6000,
  'bwidth-glottal-sine': 100,
  'bwidth-nasal-pole': 100,
  'bwidth-nasal-zero': 100,
  'bwidth (1-6)': (60, 90, 120, 250, 200, 1000),
  'formant-gain (2-6)': (0, 0, 0, 0, 0),
  'formant-bypass-gain': 57,
  'formant-cascade-gain': 0,
  'formant-parallel-gain': 20,
  'voicing-linear-gain': 47,
  'voicing-sine-gain': 47,
  'nominal-duration': 150,
  'vowel': False,
  'nasal': False,
  'regions': [LABIAL]
 },
 'θ': {
  'freq-glottal-pole': 0,
  'freq-glottal-zero': 1500,
  'freq-glottal-sine': 0,
  'freq-nasal-pole': 250,
  'freq-nasal-zero': 250,
  'freq (1-6)': (320, 1290, 2540, 3300, 3750, 4900),
  'bwidth-glottal-pole': 100,
  'bwidth-glottal-zero': 6000,
  'bwidth-glottal-sine': 100,
  'bwidth-nasal-pole': 100,
  'bwidth-nasal-zero': 100,
  'bwidth (1-6)': (200, 90, 200, 250, 200, 1000),
  'formant-gain (2-6)': (0, 0, 0, 0, 28),
  'formant-bypass-gain': 38,
  'formant-cascade-gain': 0,
  'formant-parallel-gain': 20,
  'voicing-linear-gain': 0,
  'voicing-sine-gain': 0,
  'nominal-duration': 150,
  'vowel': False,
  'nasal': False,
  'regions': [CORONAL]
 },
 'ð': {
  'freq-glottal-pole': 0,
  'freq-glottal-zero': 1500,
  'freq-glottal-sine': 0,
  'freq-nasal-pole': 250,
  'freq-nasal-zero': 250,
  'freq (1-6)': (270, 1290, 2540, 3300, 3750, 4900),
  'bwidth-glottal-pole': 100,
  'bwidth-glottal-zero': 6000,
  'bwidth-glottal-sine': 100,
  'bwidth-nasal-pole': 100,
  'bwidth-nasal-zero': 100,
  'bwidth (1-6)': (60, 80, 170, 250, 200, 1000),
  'formant-gain (2-6)': (0, 0, 0, 0, 28),
  'formant-bypass-gain': 38,
  'formant-cascade-gain': 0,
  'formant-parallel-gain': 20,
  'voicing-linear-gain': 47,
  'voicing-sine-gain': 47,
  'nominal-duration': 150,
  'vowel': False,
  'nasal': False,
  'regions': [CORONAL]
 },
 's': {
  'freq-glottal-pole': 0,
  'freq-glottal-zero': 1500,
  'freq-glottal-sine': 0,
  'freq-nasal-pole': 250,
  'freq-nasal-zero': 250,
  'freq (1-6)': (320, 1390, 2530, 3300, 3750, 4900),
  'bwidth-glottal-pole': 100,
  'bwidth-glottal-zero': 6000,
  'bwidth-glottal-sine': 100,
  'bwidth-nasal-pole': 100,
  'bwidth-nasal-zero': 100,
  'bwidth (1-6)': (200, 80, 200, 250, 200, 1000),
  'formant-gain (2-6)': (0, 0, 0, 0, 52),
  'formant-bypass-gain': 0,
  'formant-cascade-gain': 0,
  'formant-parallel-gain': 20,
  'voicing-linear-gain': 0,
  'voicing-sine-gain': 0,
  'nominal-duration': 150,
  'vowel': False,
  'nasal': False,
  'regions': [CORONAL]
 },
 'z': {
  'freq-glottal-pole': 0,
  'freq-glottal-zero': 1500,
  'freq-glottal-sine': 0,
  'freq-nasal-pole': 250,
  'freq-nasal-zero': 250,
  'freq (1-6)': (240, 1390, 2530, 3300, 3750, 4900),
  'bwidth-glottal-pole': 100,
  'bwidth-glottal-zero': 6000,
  'bwidth-glottal-sine': 100,
  'bwidth-nasal-pole': 100,
  'bwidth-nasal-zero': 100,
  'bwidth (1-6)': (70, 60, 180, 250, 200, 1000),
  'formant-gain (2-6)': (0, 0, 0, 0, 52),
  'formant-bypass-gain': 0,
  'formant-cascade-gain': 0,
  'formant-parallel-gain': 20,
  'voicing-linear-gain': 47,
  'voicing-sine-gain': 47,
  'nominal-duration': 150,
  'vowel': False,
  'nasal': False,
  'regions': [CORONAL]
 },
 'ʃ': {
  'freq-glottal-pole': 0,
  'freq-glottal-zero': 1500,
  'freq-glottal-sine': 0,
  'freq-nasal-pole': 250,
  'freq-nasal-zero': 250,
  'freq (1-6)': (300, 1840, 2750, 3300, 3750, 4900),
  'bwidth-glottal-pole': 100,
  'bwidth-glottal-zero': 6000,
  'bwidth-glottal-sine': 100,
  'bwidth-nasal-pole': 100,
  'bwidth-nasal-zero': 100,
  'bwidth (1-6)': (200, 100, 300, 250, 200, 1000),
  'formant-gain (2-6)': (0, 28, 24, 24, 23),
  'formant-bypass-gain': 0,
  'formant-cascade-gain': 0,
  'formant-parallel-gain': 20,
  'voicing-linear-gain': 0,
  'voicing-sine-gain': 0,
  'nominal-duration': 150,
  'vowel': False,
  'nasal': False,
  'regions': [CORONAL]
 },
 'ʒ': {
  'freq-glottal-pole': 0,
  'freq-glottal-zero': 1500,
  'freq-glottal-sine': 0,
  'freq-nasal-pole': 250,
  'freq-nasal-zero': 250,
  'freq (1-6)': (300, 1840, 2750, 3300, 3750, 4900),
  'bwidth-glottal-pole': 100,
  'bwidth-glottal-zero': 6000,
  'bwidth-glottal-sine': 100,
  'bwidth-nasal-pole': 100,
  'bwidth-nasal-zero': 100,
  'bwidth (1-6)': (70, 60, 280, 250, 200, 1000),
  'formant-gain (2-6)': (0, 28, 24, 24, 23),
  'formant-bypass-gain': 0,
  'formant-cascade-gain': 0,
  'formant-parallel-gain': 20,
  'voicing-linear-gain': 47,
  'voicing-sine-gain': 47,
  'nominal-duration': 150,
  'vowel': False,
  'nasal': False,
  'regions': [CORONAL]
 },
 'h': {
  'freq-glottal-pole': 0,
  'freq-glottal-zero': 1500,
  'freq-glottal-sine': 0,
  'freq-nasal-pole': 250,
  'freq-nasal-zero': 250,
  'freq (1-6)': (50, 75, 100, 3300, 3750, 4900),
  'bwidth-glottal-pole': 100,
  'bwidth-glottal-zero': 6000,
  'bwidth-glottal-sine': 100,
  'bwidth-nasal-pole': 100,
  'bwidth-nasal-zero': 100,
  'bwidth (1-6)': (60, 90, 120, 250, 200, 1000),
  'formant-gain (2-6)': (0, 0, 0, 0, 0),
  'formant-bypass-gain': 0,
  'formant-cascade-gain': 0,
  'formant-parallel-gain': 0,
  'voicing-linear-gain': 25,
  'voicing-sine-gain': 0,
  'nominal-duration': 150,
  'vowel': False,
  'nasal': False,
  'regions': [GLOTTAL]
 },
 'ɹ': {
  'freq-glottal-pole': 0,
  'freq-glottal-zero': 1500,
  'freq-glottal-sine': 0,
  'freq-nasal-pole': 250,
  'freq-nasal-zero': 250,
  'freq (1-6)': (310, 1060, 1380, 3300, 3750, 4900),
  'bwidth-glottal-pole': 100,
  'bwidth-glottal-zero': 6000,
  'bwidth-glottal-sine': 100,
  'bwidth-nasal-pole': 100,
  'bwidth-nasal-zero': 100,
  'bwidth (1-6)': (70, 100, 120, 250, 200, 1000),
  'formant-gain (2-6)': (0, 0, 0, 0, 0),
  'formant-bypass-gain': 0,
  'formant-cascade-gain': 0,
  'formant-parallel-gain': 0,
  'voicing-linear-gain': 50,
  'voicing-sine-gain': 0,
  'nominal-duration': 150,
  'vowel': False,
  'nasal': False,
  'regions': [CORONAL]
 },
 'j': {
  'freq-glottal-pole': 0,
  'freq-glottal-zero': 1500,
  'freq-glottal-sine': 0,
  'freq-nasal-pole': 250,
  'freq-nasal-zero': 250,
  'freq (1-6)': (260, 2070, 3020, 3300, 3750, 4900),
  'bwidth-glottal-pole': 100,
  'bwidth-glottal-zero': 6000,
  'bwidth-glottal-sine': 100,
  'bwidth-nasal-pole': 100,
  'bwidth-nasal-zero': 100,
  'bwidth (1-6)': (40, 250, 500, 250, 200, 1000),
  'formant-gain (2-6)': (0, 0, 0, 0, 0),
  'formant-bypass-gain': 0,
  'formant-cascade-gain': 0,
  'formant-parallel-gain': 0,
  'voicing-linear-gain': 50,
  'voicing-sine-gain': 0,
  'nominal-duration': 150,
  'vowel': False,
  'nasal': False,
  'regions': [DORSAL]
 },
 'l': {
  'freq-glottal-pole': 0,
  'freq-glottal-zero': 1500,
  'freq-glottal-sine': 0,
  'freq-nasal-pole': 250,
  'freq-nasal-zero': 250,
  'freq (1-6)': (310, 1050, 2880, 3300, 3750, 4900),
  'bwidth-glottal-pole': 100,
  'bwidth-glottal-zero': 6000,
  'bwidth-glottal-sine': 100,
  'bwidth-nasal-pole': 100,
  'bwidth-nasal-zero': 100,
  'bwidth (1-6)': (50, 100, 280, 250, 200, 1000),
  'formant-gain (2-6)': (0, 0, 0, 0, 0),
  'formant-bypass-gain': 0,
  'formant-cascade-gain': 0,
  'formant-parallel-gain': 0,
  'voicing-linear-gain': 50,
  'voicing-sine-gain': 0,
  'nominal-duration': 150,
  'vowel': False,
  'nasal': False,
  'regions': [CORONAL]
 },
 'w': {
  'freq-glottal-pole': 0,
  'freq-glottal-zero': 1500,
  'freq-glottal-sine': 0,
  'freq-nasal-pole': 250,
  'freq-nasal-zero': 250,
  'freq (1-6)': (290, 610, 2150, 3300, 3750, 4900),
  'bwidth-glottal-pole': 100,
  'bwidth-glottal-zero': 6000,
  'bwidth-glottal-sine': 100,
  'bwidth-nasal-pole': 100,
  'bwidth-nasal-zero': 100,
  'bwidth (1-6)': (50, 80, 60, 250, 200, 1000),
  'formant-gain (2-6)': (0, 0, 0, 0, 0),
  'formant-bypass-gain': 0,
  'formant-cascade-gain': 0,
  'formant-parallel-gain': 0,
  'voicing-linear-gain': 50,
  'voicing-sine-gain': 0,
  'nominal-duration': 150,
  'vowel': False,
  'nasal': False,
  'regions': [LABIAL, DORSAL]
 },
###############################################################################
 'i': {
  'freq-glottal-pole': 0,
  'freq-glottal-zero': 1500,
  'freq-glottal-sine': 0,
  'freq-nasal-pole': 250,
  'freq-nasal-zero': 250,
  'freq (1-6)': (310, 2020, 2960, 3300, 3750, 4900),
  'bwidth-glottal-pole': 100,
  'bwidth-glottal-zero': 6000,
  'bwidth-glottal-sine': 100,
  'bwidth-nasal-pole': 100,
  'bwidth-nasal-zero': 100,
  'bwidth (1-6)': (45, 200, 400, 250, 200, 1000),
  'formant-gain (2-6)': (0, 0, 0, 0, 0),
  'formant-bypass-gain': 0,
  'formant-cascade-gain': 0,
  'formant-parallel-gain': 0,
  'voicing-linear-gain': 60,
  'voicing-sine-gain': 0,
  'nominal-duration': 275,
  'vowel': True,
  'nasal': False,
  'regions': [FRONT]
 },
 'e': {
  'freq-glottal-pole': 0,
  'freq-glottal-zero': 1500,
  'freq-glottal-sine': 0,
  'freq-nasal-pole': 250,
  'freq-nasal-zero': 250,
  'freq (1-6)': (480, 1720, 2520, 3300, 3750, 4900),
  'bwidth-glottal-pole': 100,
  'bwidth-glottal-zero': 6000,
  'bwidth-glottal-sine': 100,
  'bwidth-nasal-pole': 100,
  'bwidth-nasal-zero': 100,
  'bwidth (1-6)': (70, 100, 200, 250, 200, 1000),
  'formant-gain (2-6)': (0, 0, 0, 0, 0),
  'formant-bypass-gain': 0,
  'formant-cascade-gain': 0,
  'formant-parallel-gain': 0,
  'voicing-linear-gain': 60,
  'voicing-sine-gain': 0,
  'nominal-duration': 275,
  'vowel': True,
  'nasal': False,
  'regions': [FRONT]
 },
 'ɛ': {
  'freq-glottal-pole': 0,
  'freq-glottal-zero': 1500,
  'freq-glottal-sine': 0,
  'freq-nasal-pole': 250,
  'freq-nasal-zero': 250,
  'freq (1-6)': (530, 1680, 2500, 3300, 3750, 4900),
  'bwidth-glottal-pole': 100,
  'bwidth-glottal-zero': 6000,
  'bwidth-glottal-sine': 100,
  'bwidth-nasal-pole': 100,
  'bwidth-nasal-zero': 100,
  'bwidth (1-6)': (60, 90, 200, 250, 200, 1000),
  'formant-gain (2-6)': (0, 0, 0, 0, 0),
  'formant-bypass-gain': 0,
  'formant-cascade-gain': 0,
  'formant-parallel-gain': 0,
  'voicing-linear-gain': 60,
  'voicing-sine-gain': 0,
  'nominal-duration': 225,
  'vowel': True,
  'nasal': False,
  'regions': [NEAR_FRONT]
 },
 'æ': {
  'freq-glottal-pole': 0,
  'freq-glottal-zero': 1500,
  'freq-glottal-sine': 0,
  'freq-nasal-pole': 250,
  'freq-nasal-zero': 250,
  'freq (1-6)': (620, 1660, 2430, 3300, 3750, 4900),
  'bwidth-glottal-pole': 100,
  'bwidth-glottal-zero': 6000,
  'bwidth-glottal-sine': 100,
  'bwidth-nasal-pole': 100,
  'bwidth-nasal-zero': 100,
  'bwidth (1-6)': (70, 150, 320, 250, 200, 1000),
  'formant-gain (2-6)': (0, 0, 0, 0, 0),
  'formant-bypass-gain': 0,
  'formant-cascade-gain': 0,
  'formant-parallel-gain': 0,
  'voicing-linear-gain': 60,
  'voicing-sine-gain': 0,
  'nominal-duration': 325,
  'vowel': True,
  'nasal': False,
  'regions': [NEAR_FRONT]
 },
 'a': {
  'freq-glottal-pole': 0,
  'freq-glottal-zero': 1500,
  'freq-glottal-sine': 0,
  'freq-nasal-pole': 250,
  'freq-nasal-zero': 250,
  'freq (1-6)': (700, 1220, 2600, 3300, 3750, 4900),
  'bwidth-glottal-pole': 100,
  'bwidth-glottal-zero': 6000,
  'bwidth-glottal-sine': 100,
  'bwidth-nasal-pole': 100,
  'bwidth-nasal-zero': 100,
  'bwidth (1-6)': (130, 70, 160, 250, 200, 1000),
  'formant-gain (2-6)': (0, 0, 0, 0, 0),
  'formant-bypass-gain': 0,
  'formant-cascade-gain': 0,
  'formant-parallel-gain': 0,
  'voicing-linear-gain': 60,
  'voicing-sine-gain': 0,
  'nominal-duration': 300,
  'vowel': True,
  'nasal': False,
  'regions': [CENTRAL]
 },
 'I': {
  'freq-glottal-pole': 0,
  'freq-glottal-zero': 1500,
  'freq-glottal-sine': 0,
  'freq-nasal-pole': 250,
  'freq-nasal-zero': 250,
  'freq (1-6)': (400, 1800, 2570, 3300, 3750, 4900),
  'bwidth-glottal-pole': 100,
  'bwidth-glottal-zero': 6000,
  'bwidth-glottal-sine': 100,
  'bwidth-nasal-pole': 100,
  'bwidth-nasal-zero': 100,
  'bwidth (1-6)': (50, 100, 140, 250, 200, 1000),
  'formant-gain (2-6)': (0, 0, 0, 0, 0),
  'formant-bypass-gain': 0,
  'formant-cascade-gain': 0,
  'formant-parallel-gain': 0,
  'voicing-linear-gain': 60,
  'voicing-sine-gain': 0,
  'nominal-duration': 225,
  'vowel': True,
  'nasal': False,
  'regions': [NEAR_FRONT]
 },
 'ə': {
  'freq-glottal-pole': 0,
  'freq-glottal-zero': 1500,
  'freq-glottal-sine': 0,
  'freq-nasal-pole': 250,
  'freq-nasal-zero': 250,
  'freq (1-6)': (500, 1400, 2300, 3300, 3750, 4900),
  'bwidth-glottal-pole': 100,
  'bwidth-glottal-zero': 6000,
  'bwidth-glottal-sine': 100,
  'bwidth-nasal-pole': 100,
  'bwidth-nasal-zero': 100,
  'bwidth (1-6)': (100, 60, 110, 250, 200, 1000),
  'formant-gain (2-6)': (0, 0, 0, 0, 0),
  'formant-bypass-gain': 0,
  'formant-cascade-gain': 0,
  'formant-parallel-gain': 0,
  'voicing-linear-gain': 50,
  'voicing-sine-gain': 0,
  'nominal-duration': 175,
  'vowel': True,
  'nasal': False,
  'regions': [CENTRAL]
 },
 'ʊ': {
  'freq-glottal-pole': 0,
  'freq-glottal-zero': 1500,
  'freq-glottal-sine': 0,
  'freq-nasal-pole': 250,
  'freq-nasal-zero': 250,
  'freq (1-6)': (450, 1100, 2350, 3300, 3750, 4900),
  'bwidth-glottal-pole': 100,
  'bwidth-glottal-zero': 6000,
  'bwidth-glottal-sine': 100,
  'bwidth-nasal-pole': 100,
  'bwidth-nasal-zero': 100,
  'bwidth (1-6)': (80, 100, 80, 250, 200, 1000),
  'formant-gain (2-6)': (0, 0, 0, 0, 0),
  'formant-bypass-gain': 0,
  'formant-cascade-gain': 0,
  'formant-parallel-gain': 0,
  'voicing-linear-gain': 60,
  'voicing-sine-gain': 0,
  'nominal-duration': 225,
  'vowel': True,
  'nasal': False,
  'regions': [NEAR_BACK]
 },
 'u': {
  'freq-glottal-pole': 0,
  'freq-glottal-zero': 1500,
  'freq-glottal-sine': 0,
  'freq-nasal-pole': 250,
  'freq-nasal-zero': 250,
  'freq (1-6)': (350, 1250, 2200, 3300, 3750, 4900),
  'bwidth-glottal-pole': 100,
  'bwidth-glottal-zero': 6000,
  'bwidth-glottal-sine': 100,
  'bwidth-nasal-pole': 100,
  'bwidth-nasal-zero': 100,
  'bwidth (1-6)': (65, 110, 140, 250, 200, 1000),
  'formant-gain (2-6)': (0, 0, 0, 0, 0),
  'formant-bypass-gain': 0,
  'formant-cascade-gain': 0,
  'formant-parallel-gain': 0,
  'voicing-linear-gain': 60,
  'voicing-sine-gain': 0,
  'nominal-duration': 275,
  'vowel': True,
  'nasal': False,
  'regions': [BACK]
 },
 'o': {
  'freq-glottal-pole': 0,
  'freq-glottal-zero': 1500,
  'freq-glottal-sine': 0,
  'freq-nasal-pole': 250,
  'freq-nasal-zero': 250,
  'freq (1-6)': (540, 1100, 2300, 3300, 3750, 4900),
  'bwidth-glottal-pole': 100,
  'bwidth-glottal-zero': 6000,
  'bwidth-glottal-sine': 100,
  'bwidth-nasal-pole': 100,
  'bwidth-nasal-zero': 100,
  'bwidth (1-6)': (80, 70, 70, 250, 200, 1000),
  'formant-gain (2-6)': (0, 0, 0, 0, 0),
  'formant-bypass-gain': 0,
  'formant-cascade-gain': 0,
  'formant-parallel-gain': 0,
  'voicing-linear-gain': 60,
  'voicing-sine-gain': 0,
  'nominal-duration': 275,
  'vowel': True,
  'nasal': False,
  'regions': [BACK]
 },
 'ʌ': {
  'freq-glottal-pole': 0,
  'freq-glottal-zero': 1500,
  'freq-glottal-sine': 0,
  'freq-nasal-pole': 250,
  'freq-nasal-zero': 250,
  'freq (1-6)': (620, 1220, 2550, 3300, 3750, 4900),
  'bwidth-glottal-pole': 100,
  'bwidth-glottal-zero': 6000,
  'bwidth-glottal-sine': 100,
  'bwidth-nasal-pole': 100,
  'bwidth-nasal-zero': 100,
  'bwidth (1-6)': (80, 50, 140, 250, 200, 1000),
  'formant-gain (2-6)': (0, 0, 0, 0, 0),
  'formant-bypass-gain': 0,
  'formant-cascade-gain': 0,
  'formant-parallel-gain': 0,
  'voicing-linear-gain': 60,
  'voicing-sine-gain': 0,
  'nominal-duration': 200,
  'vowel': True,
  'nasal': False,
  'regions': [BACK]
 },
 'ɔ': {
  'freq-glottal-pole': 0,
  'freq-glottal-zero': 1500,
  'freq-glottal-sine': 0,
  'freq-nasal-pole': 250,
  'freq-nasal-zero': 250,
  'freq (1-6)': (600, 990, 2570, 3300, 3750, 4900),
  'bwidth-glottal-pole': 100,
  'bwidth-glottal-zero': 6000,
  'bwidth-glottal-sine': 100,
  'bwidth-nasal-pole': 100,
  'bwidth-nasal-zero': 100,
  'bwidth (1-6)': (90, 100, 80, 250, 200, 1000),
  'formant-gain (2-6)': (0, 0, 0, 0, 0),
  'formant-bypass-gain': 0,
  'formant-cascade-gain': 0,
  'formant-parallel-gain': 0,
  'voicing-linear-gain': 60,
  'voicing-sine-gain': 0,
  'nominal-duration': 275,
  'vowel': True,
  'nasal': False,
  'regions': [BACK]
 }
} #: A neatly organized dictionary to make it easier for linguists to alter settings.

_IPA_CLUSTERS = (
 (('d', 'ʒ'), (
  0, 1500, 0, #Glottal frequencies.
  250, 250, #Nasal frequencies.
  260, 1800, 2820, 3300, 3750, 4900, #Formant frequencies.
  100, 6000, 100, #Glottal bandwidths.
  100, 100, #Nasal bandwidths.
  60, 80, 270, 250, 200, 1000, #Formant bandwidths.
  0, 22, 30, 26, 26, #Formant gains.
  0, #Formant bypass gain.
  0, #Formant cascade gain.
  10, #Formant parallel gain.
  37, #Voicing linear gain.
  37, #Voicing sinusoidal gain.
  150 #Nominal duration.
 )),
 (('t', 'ʃ'), (
  0, 1500, 0, #Glottal frequencies.
  250, 250, #Nasal frequencies.
  350, 1800, 2820, 3300, 3750, 4900, #Formant frequencies.
  100, 6000, 100, #Glottal bandwidths.
  100, 100, #Nasal bandwidths.
  200, 90, 300, 250, 200, 1000, #Formant bandwidths.
  0, 22, 30, 26, 26, #Formant gains.
  0, #Formant bypass gain.
  0, #Formant cascade gain.
  10, #Formant parallel gain.
  0, #Voicing linear gain.
  0, #Voicing sinusoidal gain.
  150 #Nominal duration.
 )),
 (('a', 'j'), (
  0, 1500, 0, #Glottal frequencies.
  250, 250, #Nasal frequencies.
  660, 1200, 2550, 3300, 3750, 4900, #Formant frequencies.
  100, 6000, 100, #Glottal bandwidths.
  100, 100, #Nasal bandwidths.
  100, 70, 200, 250, 200, 1000, #Formant bandwidths.
  0, 0, 0, 0, 0, #Formant gains.
  0, #Formant bypass gain.
  0, #Formant cascade gain.
  0, #Formant parallel gain.
  60, #Voicing linear gain.
  0, #Voicing sinusoidal gain.
  325 #Nominal duration.
 ),
 (('a', 'w'), (
  0, 1500, 0, #Glottal frequencies.
  250, 250, #Nasal frequencies.
  640, 1230, 2550, 3300, 3750, 4900, #Formant frequencies.
  100, 6000, 100, #Glottal bandwidths.
  100, 100, #Nasal bandwidths.
  80, 70, 140, 250, 200, 1000, #Formant bandwidths.
  0, 0, 0, 0, 0, #Formant gains.
  0, #Formant bypass gain.
  0, #Formant cascade gain.
  0, #Formant parallel gain.
  60, #Voicing linear gain.
  0, #Voicing sinusoidal gain.
  325 #Nominal duration.
 ),
 (('ɔ', 'j'), (
  0, 1500, 0, #Glottal frequencies.
  250, 250, #Nasal frequencies.
  550, 960, 2400, 3300, 3750, 4900, #Formant frequencies.
  100, 6000, 100, #Glottal bandwidths.
  100, 100, #Nasal bandwidths.
  80, 50, 130, 250, 200, 1000, #Formant bandwidths.
  0, 0, 0, 0, 0, #Formant gains.
  0, #Formant bypass gain.
  0, #Formant cascade gain.
  0, #Formant parallel gain.
  60, #Voicing linear gain.
  0, #Voicing sinusoidal gain.
  325 #Nominal duration.
 )
) #: An arbitrary mapping of complex IPA symbols that need to be specially handled.

#Reduce IPA data to efficient structures.
VOWELS = tuple([ipa_character for (ipa_character, details) in _IPA_MAPPING.iteritems() if details['vowel']])
NASALS = tuple([ipa_character for (ipa_character, details) in _IPA_MAPPING.iteritems() if details['nasal']])
IPA_PARAMETERS = {}
IPA_REGIONS = {}
IPA_DATA = {}
for (ipa_character, details) in _IPA_MAPPING.iteritems():
	parameters = (
	 details['freq-glottal-pole'],
	 details['freq-glottal-zero'],
	 details['freq-glottal-sine'],
	 details['freq-nasal-pole'],
	 details['freq-nasal-zero'],
	) + details['freq (1-6)'] + (
	 details['bwidth-glottal-pole'],
	 details['bwidth-glottal-zero'],
	 details['bwidth-glottal-sine'],
	 details['bwidth-nasal-pole'],
	 details['bwidth-nasal-zero']
	) + details['bwidth (1-6)'] +
	details['formant-gain (2-6)'] + (
	 details['formant-bypass-gain'],
	 details['formant-cascade-gain'],
	 details['formant-parallel-gain'],
	 details['voicing-linear-gain'],
	 details['voicing-sine-gain'],
	 details['nominal-duration']
	)
	regions = tuple(details['regions'])
	
	IPA_PARAMETERS[ipa_character] = parameters
	IPA_REGIONS[ipa_character] = regions
	IPA_DATA[ipa_character] = (parameters, regions)
del _IPA_MAPPING


def screenIPAClusters(ipa_character, preceding_sounds, following_sounds):
	for ((head, tail), parameters) in _IPA_CLUSTERS:
		if head == ipa_character and following_sounds and following_sounds[0] == tail:
			return (True, parameters)
		elif tail == ipa_character and preceding_sounds and preceding_sounds[0] == head:
			return (True, None)
	return (False, None)
	