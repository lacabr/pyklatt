# -*- coding: utf-8 -*-
"""
CPSC 599 module: src.ipa

Purpose
=======
 Provides IPA-to-parameter lookup functions.
 
Limitations
===========
 At present, only the following IPA symbols are supported:
  mnŋpbtdɾkgfvθðszʃʒhɹjwl
  ieɛæaIəʊuoʌɔ
 
Legal
=====
 All code, unless otherwise indicated, is original, and subject to the
 terms of the GPLv2, which is provided in COPYING.
 
 This project borrows algorithms, ideas, and statistical data from other
 projects. Full attribution is provided in ACKNOWLEDGEMENTS.
 
 (C) Neil Tallim, Sydni Bennie, 2009
"""
#Enumerations of consonant positions.
LABIAL = 1 #: Identifies a consonant as labial.
CORONAL = 2 #: Identifies a consonant as coronal.
DORSAL = 3 #: Identifies a consonant as dorsal.
RADICAL = 4 #: Identifies a consonant as radical.
GLOTTAL = 5 #: Identifies a consonant as glottal.

#Enumerations of vowel positions.
FRONT = 1 #: Identifies a vowel as front-wards.
NEAR_FRONT = 2 #: Identifies a vowel as near-front.
CENTRAL = 3 #: Identifies a vowel as central.
NEAR_BACK = 4 #: Identifies a vowel as near-back.
BACK = 5 #: Identifies a vowel as back-wards.

_IPA_MAPPING = {
 u'm': {
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
  'nominal-duration': 75,
  'vowel': False,
  'nasal': True,
  'voice': True,
  'regions': [LABIAL]
 },
 u'n': {
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
  'nominal-duration': 75,
  'vowel': False,
  'nasal': True,
  'voice': True,
  'regions': [CORONAL]
 },
 u'\u014b': { #ŋ
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
  'nominal-duration': 75,
  'vowel': False,
  'nasal': True,
  'voice': True,
  'regions': [DORSAL]
 },
 u'p': {
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
  'nominal-duration': 50,
  'vowel': False,
  'nasal': False,
  'voice': False,
  'regions': [LABIAL]
 },
 u'b': {
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
  'nominal-duration': 50,
  'vowel': False,
  'nasal': False,
  'voice': True,
  'regions': [LABIAL]
 },
 u't': {
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
  'nominal-duration': 25,
  'vowel': False,
  'nasal': False,
  'voice': False,
  'regions': [CORONAL]
 },
 u'd': {
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
  'nominal-duration': 25,
  'vowel': False,
  'nasal': False,
  'voice': True,
  'regions': [CORONAL]
 },
 u'\u027e': { #ɾ
  'freq-glottal-pole': 0,
  'freq-glottal-zero': 1500,
  'freq-glottal-sine': 0,
  'freq-nasal-pole': 250,
  'freq-nasal-zero': 250,
  'freq (1-6)': (300, 1600, 2600, 3300, 3750, 4900),
  'bwidth-glottal-pole': 100,
  'bwidth-glottal-zero': 6000,
  'bwidth-glottal-sine': 100,
  'bwidth-nasal-pole': 100,
  'bwidth-nasal-zero': 100,
  'bwidth (1-6)': (160, 110, 210, 250, 200, 1000),
  'formant-gain (2-6)': (0, 19, 26, 30, 31),
  'formant-bypass-gain': 0,
  'formant-cascade-gain': 0,
  'formant-parallel-gain': 15,
  'voicing-linear-gain': 10,
  'voicing-sine-gain': 10,
  'nominal-duration': 25,
  'vowel': False,
  'nasal': False,
  'voice': True,
  'regions': [CORONAL]
 },
 u'k': {
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
  'nominal-duration': 25,
  'vowel': False,
  'nasal': False,
  'voice': False,
  'regions': [DORSAL]
 },
 u'g': {
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
  'nominal-duration': 25,
  'vowel': False,
  'nasal': False,
  'voice': True,
  'regions': [DORSAL]
 },
 u'f': {
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
  'nominal-duration': 50,
  'vowel': False,
  'nasal': False,
  'voice': False,
  'regions': [LABIAL]
 },
 u'v': {
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
  'nominal-duration': 50,
  'vowel': False,
  'nasal': False,
  'voice': True,
  'regions': [LABIAL]
 },
 u'\u03b8': { #θ
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
  'nominal-duration': 50,
  'vowel': False,
  'nasal': False,
  'voice': False,
  'regions': [CORONAL]
 },
 u'\xf0': { #ð
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
  'nominal-duration': 50,
  'vowel': False,
  'nasal': False,
  'voice': True,
  'regions': [CORONAL]
 },
 u's': {
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
  'nominal-duration': 50,
  'vowel': False,
  'nasal': False,
  'voice': False,
  'regions': [CORONAL]
 },
 u'z': {
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
  'nominal-duration': 65,
  'vowel': False,
  'nasal': False,
  'voice': True,
  'regions': [CORONAL]
 },
 u'\u0283': { #ʃ
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
  'nominal-duration': 75,
  'vowel': False,
  'nasal': False,
  'voice': False,
  'regions': [CORONAL]
 },
 u'\u0292': { #ʒ
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
  'nominal-duration': 75,
  'vowel': False,
  'nasal': False,
  'voice': True,
  'regions': [CORONAL]
 },
 u'h': {
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
  'nominal-duration': 50,
  'vowel': False,
  'nasal': False,
  'voice': False,
  'regions': [GLOTTAL]
 },
 u'\u0279': { #ɹ
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
  'nominal-duration': 100,
  'vowel': False,
  'nasal': False,
  'voice': True,
  'regions': [CORONAL]
 },
 u'j': {
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
  'nominal-duration': 50,
  'vowel': False,
  'nasal': False,
  'voice': True,
  'regions': [DORSAL]
 },
 u'l': {
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
  'nominal-duration': 100,
  'vowel': False,
  'nasal': False,
  'voice': True,
  'regions': [CORONAL]
 },
 u'w': {
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
  'nominal-duration': 65,
  'vowel': False,
  'nasal': False,
  'voice': True,
  'regions': [LABIAL, DORSAL]
 },
###############################################################################
 u'i': {
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
  'nominal-duration': 150,
  'vowel': True,
  'nasal': False,
  'voice': True,
  'regions': [FRONT]
 },
 u'e': {
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
  'nominal-duration': 150,
  'vowel': True,
  'nasal': False,
  'voice': True,
  'regions': [FRONT]
 },
 u'\u025b': { #ɛ
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
  'nominal-duration': 125,
  'vowel': True,
  'nasal': False,
  'voice': True,
  'regions': [NEAR_FRONT]
 },
 u'\xe6': { #æ
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
  'nominal-duration': 200,
  'vowel': True,
  'nasal': False,
  'voice': True,
  'regions': [NEAR_FRONT]
 },
 u'a': {
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
  'nominal-duration': 175,
  'vowel': True,
  'nasal': False,
  'voice': True,
  'regions': [CENTRAL]
 },
 u'I': {
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
  'nominal-duration': 150,
  'vowel': True,
  'nasal': False,
  'voice': True,
  'regions': [NEAR_FRONT]
 },
 u'\u0259': { #ə
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
  'nominal-duration': 125,
  'vowel': True,
  'nasal': False,
  'voice': True,
  'regions': [CENTRAL]
 },
 u'\u028a': { #ʊ
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
  'nominal-duration': 125,
  'vowel': True,
  'nasal': False,
  'voice': True,
  'regions': [NEAR_BACK]
 },
 u'u': {
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
  'nominal-duration': 150,
  'vowel': True,
  'nasal': False,
  'voice': True,
  'regions': [BACK]
 },
 u'o': {
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
  'nominal-duration': 150,
  'vowel': True,
  'nasal': False,
  'voice': True,
  'regions': [BACK]
 },
 u'\u028c': { #ʌ
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
  'nominal-duration': 100,
  'vowel': True,
  'nasal': False,
  'voice': True,
  'regions': [BACK]
 },
 u'\u0254': { #ɔ
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
  'nominal-duration': 150,
  'vowel': True,
  'nasal': False,
  'voice': True,
  'regions': [BACK]
 }
} #: A neatly organized dictionary to make it easier for linguists to alter parameters.

_IPA_CLUSTERS = (
 (('d', '\u0292'), ( #dʒ
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
  100 #Nominal duration.
 )), 
 (('t', '\u0283'), ( #tʃ
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
  100 #Nominal duration.
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
  150 #Nominal duration.
 )),
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
  150 #Nominal duration.
 )),
 (('\u0254', 'j'), ( #ɔj
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
  150 #Nominal duration.
 ))
) #: An arbitrary mapping of multi-character IPA symbols that need to be reduced during phoneme pre-processing.

#Reduce IPA data to efficient structures.
VOWELS = tuple([ipa_character for (ipa_character, details) in _IPA_MAPPING.iteritems() if details['vowel']]) #: A list of all vowel phonemes.
NASALS = tuple([ipa_character for (ipa_character, details) in _IPA_MAPPING.iteritems() if details['nasal']]) #: A list of all nasal phonemes.
VOICED = tuple([ipa_character for (ipa_character, details) in _IPA_MAPPING.iteritems() if details['voice']]) #: A list of all voiced phonemes.
IPA_PARAMETERS = {} #: A collection of synthesizing parameter tuples, keyed by corresponding IPA character.
IPA_REGIONS = {} #: A collection of phoneme regions, keyed by corresponding IPA character.
IPA_DATA = {} #: A collection of both parameters and regions, in a tuple, keyed by corresponding IPA character.
for (ipa_character, details) in _IPA_MAPPING.iteritems():
	#Extract an ordered tuple of data from the dictionary.
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
	) + details['bwidth (1-6)'] +	details['formant-gain (2-6)'] + (
	 details['formant-bypass-gain'],
	 details['formant-cascade-gain'],
	 details['formant-parallel-gain'],
	 details['voicing-linear-gain'],
	 details['voicing-sine-gain'],
	 details['nominal-duration']
	)
	regions = tuple(details['regions']) #Extract region data.
	
	#Place extracted data into more efficient indexes.
	IPA_PARAMETERS[ipa_character] = parameters
	IPA_REGIONS[ipa_character] = regions
	IPA_DATA[ipa_character] = (parameters, regions)
del _IPA_MAPPING


def screenIPAClusters(ipa_character, preceding_phonemes, following_phonemes):
	"""
	Determines whether the given IPA character is part of a multi-character
	sequence, and returns appropriate parameters or dismisses the character
	accordingly.
	
	The first character in such a sequence is ignored so that markup and
	rule-processing may be applied to the second character, which is more
	intuitive from a data-entry perspective.
	
	@type ipa_character: unicode
	@param ipa_character: The character, representative of a phoneme, being
	    processed.
	@type preceding_phonemes: sequence
	@param preceding_phonemes: A collection of all phonemes, in order, that
	    precede the current IPA character in the current word.
	@type following_phonemes: sequence
	@param following_phonemes: A collection of all phonemes, in order, that
	    follow the current IPA character in the current word.
	
	@rtype: tuple(2)
	@return: (False, None) if no processing needs to be applied; (True, None) if
	    the current character should be ignored; (True, parameters) if specific
	    parameters should be used instead of those normally associated with the
	    current character, where parameters are presented in the same format as
	    found in L{IPA_PARAMETERS}.
	"""
	for ((head, tail), parameters) in _IPA_CLUSTERS:
		if head == ipa_character and following_phonemes and following_phonemes[0] == tail:
			return (True, None)
		elif tail == ipa_character and preceding_phonemes and preceding_phonemes[0] == head:
			return (True, parameters)
	return (False, None)
	