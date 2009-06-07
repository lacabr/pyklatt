# -*- coding: utf-8 -*-
"""
Klatt CPSC 599 module: klatt

Purpose
=======
 Provides a convenient wrapper for writing waveform data.
 
Legal
=====
 All code, unless otherwise indicated, is original, and subject to the
 terms of the GPLv2, which is provided in COPYING.
 
 (C) Neil Tallim, 2009
"""

import struct
import wave

class WaveForm(object):
	_finalized = False #: True when this file has been closed.
	_wavefile = None #: The file into which wave data will be written.
	
	def __init__(self, filename, frequency):
		self._wavefile = wave.open(filename, 'wb')
		self._wavefile.setnchannels(1) #Mono.
		self._wavefile.setsampwidth(2) #16-bit.
		self._wavefile.setframerate(frequency)
		
	def addSamples(self, samples):
		if self._finalized:
			raise IOError("The waveform has already been finalized.")
		self._wavefile.writeframes(''.join([struct.pack('h', sample) for sample in samples]))
		
	def close(self):
		if not self._finalized:
			self._wavefile.close()
			self._finalized = True
			