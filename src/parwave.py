# -*- coding: utf-8 -*-
"""
CPSC 599 module: src.parwave

Purpose
=======
 Provides functionality for generating waveform samples from format parameter
 data.
 
Legal
=====
 All code, unless otherwise indicated, is original, and subject to the
 terms of the GPLv2, which is provided in COPYING.
 
 This project borrows algorithms, ideas, and statistical data from other
 projects. Full attribution is provided in ACKNOWLEDGEMENTS.
 
 (C) Neil Tallim, Sydni Bennie, 2009
"""
import math
import random

FREQUENCY = 10 #: A number that indicates the frequency of synthesized speech, as a multiple of 1000Hz.
_ANTI_POP_CYCLES = 15 #: The number of cycles to clip from the front of a sound to avoid popping.

class Synthesizer(object):
	"""
	Enables synthesis of sounds based on parameter values, as described in the
	referenced papers.
	"""
	_noise = 0.0 #: The last-generated random noise value, needed for echoing.
	
	def generateSilence(self, milliseconds):
		"""
		Generates a period of silence and resets the noise value.
		
		@type milliseconds: int
		@param milliseconds: The number of milliseconds of silence to be
		    generated.
		
		@rtype: tuple
		@return: A collection of 0s, equal in length to milliseconds * 10.
		"""
		self._noise = 0.0
		return (0,) * int(milliseconds * FREQUENCY)
		
	def synthesize(self, parameters, f0=160):
		"""
		Renders the given parameters in a sinewave pattern, with period being
		defined based on the given formant frequencies and an f0 pulse, and
		amplitude being a function of bandwidth, base amplitude values, white
		noise, and resonance.
		
		@type parameters: sequence(33)
		@param parameters: A collection of synthesis parameters, as described in
		    L{ipa._IPA_MAPPING} and L{ipa._IPA_CLUSTERS}.
		@type f0: int
		@param f0: The period pulse value, also called the primary frequency and
		    the flutter value. This controls the period and contour of sounds in
		    general.
		
		@rtype: tuple
		@return: A collection of integers between -32768 and 32767 that represent
		    synthetic speech.
		"""
		anti_pop_cycles = _ANTI_POP_CYCLES #Cache value locally for speed.
		
		#Initialize parameters required for synthesis.
		half_f0 = f0 / 2.0
		(fgp, fgz, fgs, fnp, fnz,
		 f1, f2, f3, f4, f5, f6,
		 bgp, bgz, bgs, bnp, bnz,
		 bw1, bw2, bw3, bw4, bw5, bw6,
		 a2, a3, a4, a5, a6,
		 ab, ah, af, av, avs,
		 milliseconds) = parameters
		
		#Prepare all resonators.
		(cascade_resonators, parallel_resonators,
		 glottal_pole_resonator, glottal_sine_resonator,
		 nasal_pole_resonator, glottal_antiresonator,
		 nasal_antiresonator) = self._initSynthesizers(
		  (fgp, fgz, fgs, fnp, fnz, f1, f2, f3, f4, f5, f6),
		  (bgp, bgz, bgs, bnp, bnz, bw1, bw2, bw3, bw4, bw5, bw6)
		 )
		
		#Set loop variables.
		sounds = []
		last_result = 0
		period_index = f0
		for t in xrange(int(milliseconds * FREQUENCY) + anti_pop_cycles): #Run for the specified number of milliseconds, plus cycles for the anti-pop algorithm.
			noise = self._getNoise()
			
			#Apply linear f0 approximation.
			pulse = 0.0
			if period_index >= f0:
				pulse = 1.0
				period_index = 0
			else:
				period_index += 2
				
			#Compute cascade value.
			source = glottal_pole_resonator.resonate(pulse)
			source = (glottal_antiresonator.resonate(source) * av) + (glottal_sine_resonator.resonate(source) * avs)
			source += noise * ah
			source = nasal_pole_resonator.resonate(source)
			source = nasal_antiresonator.resonate(source)
			
			frication = noise * af
			
			result = frication * ab #Seed parallel value.
			for ((cascade_resonator, parallel_resonator), amplitude) in reversed(zip(zip(cascade_resonators[1:], parallel_resonators), (a2, a3, a4, a5, a6))):
				source = cascade_resonator.resonate(source) #Update cascade value.
				result += parallel_resonator.resonate(frication * amplitude) #Update parallel value.
			result += cascade_resonators[0].resonate(source) #: Add final cascade value to final parallel value.
			
			output = result - last_result #Subtract last result from new result to introduce a micro-period into the waveform so it's audible to humans.
			last_result = result
			if t >= anti_pop_cycles: #Skip the first several values to avoid popping.
				output = int(output * 32767.0) #Convert the result to an integer on an appropriate scale.
				if output > 16383: #Constrain the output range, by clipping if necessary.
					output = 16383
				elif output < -16383:
					output = -16383
				sounds.append(output)
		return tuple(sounds)
		
	def _initSynthesizers(self, frequencies, bandwidths):
		"""
		Constructs a number of _Synthesizers for use in rendering sound from
		parameter values.
		
		@type frequencies: sequence(11)
		@param frequencies: (fgp, fgz, fgs, fnp, fnz, f1, f2, f3, f4, f5, f6)
		    from the input parameters.
		@type bandwidths: sequence(11)
		@param bandwidths: (bgp, bgz, bgs, bnp, bnz, bw1, bw2, bw3, bw4, bw5, bw6)
		    from the input parameters.
		
		@rtype: tuple(7)
		@return: A tuple of six cascade resonators, 1-6, a tuple of five parallel
		    resonators, 2-6, a glottal pole resonator, a glottal sine resonator,
		    a nasal pole resonator, and both a glottal and nasal antiresonator.
		"""
		#I don't know the significance of this math, unfortunately.
		pi_neg_div = math.pi * -0.0001
		pi_2_div = 2.0 * math.pi * 0.0001
		pi_neg_2_div = -pi_2_div
		
		b = (bgp, bgz, bgs, bnp, bnz, b1, b2, b3, b4, b5, b6) = [n * m for (n, m) in zip([math.cos(pi_2_div * f) for f in frequencies], [2 * math.e ** (pi_neg_div * bw) for bw in bandwidths])]
		c = (cgp, cgz, cgs, cnp, cnz, c1, c2, c3, c4, c5, c6) = [-math.e ** (pi_neg_2_div * bw) for bw in bandwidths]
		(agp, agz, ags, anp, anz, a1, a2, a3, a4, a5, a6) = [1 - b_v - c_v for (b_v, c_v) in zip(b, c)]
		
		return (
		 (
		  _Resonator(a1, b1, c1),
		  _Resonator(a2, b2, c2),
		  _Resonator(a3, b3, c3),
		  _Resonator(a4, b4, c4),
		  _Resonator(a5, b5, c5),
		  _Resonator(a6, b6, c6)
		 ),
		 (
		  _Resonator(a2, b2, c2),
		  _Resonator(a3, b3, c3),
		  _Resonator(a4, b4, c4),
		  _Resonator(a5, b5, c5),
		  _Resonator(a6, b6, c6)
		 ),
		 _Resonator(agp, bgp, cgp),
		 _Resonator(ags, bgs, cgs),
		 _Resonator(anp, bnp, cnp),
		 _AntiResonator(agz, bgz, cgz),
		 _AntiResonator(anz, bnz, cnz)
		)
		
	def _getNoise(self):
		"""
		Generates a random number and adds it to the last-generated random value.
		
		@rtype: float
		@return: A random value, half of which is echoed.
		"""
		self._noise = random.uniform(-0.00001, 0.00001) + self._noise
		return self._noise
		
		
class _Resonator(object):
	_a = None #: I don't know enough about Klatt's math to describe this.
	_b = None #: I don't know enough about Klatt's math to describe this.
	_c = None #: I don't know enough about Klatt's math to describe this.
	_delay_1 = 0.0 #: The last-stored value for use in successive resonance.
	_delay_2 = 0.0 #: The second-last-stored value for use in successive resonance.
	
	def __init__(self, a, b, c):
		self._a = a
		self._b = b
		self._c = c
		
	def resonate(self, input):
		"""
		Resonates the input value, producing output.
		
		The output value is stored for use in successive resonance.
		
		@type input: number
		@param input: The value to be resonated.
		
		@rtype: float
		@return: The result of resonance.
		"""
		output = self._resonate(input)
		self._delay_1 = output
		return output
		
	def _resonate(self, input):
		"""
		Employs two-tier echoing to resonate the input value as though it were
		passing through a chamber.
		
		@type input: number
		@param input: The value to be resonated.
		
		@rtype: float
		@return: The result of resonance.
		"""
		output = self._a * input + self._b * self._delay_1 + self._c * self._delay_2
		self._delay_2 = self._delay_1
		return output
		
class _AntiResonator(_Resonator):
	"""
	A variant on the resonator that generates inverse harmonics.
	"""
	def __init__(self, a, b, c):
		a = 1.0 / a
		_Resonator.__init__(self, a, -b * a, -c * a)
		
	def resonate(self, input):
		"""
		Resonates the input value, producing output.
		
		The input value is stored for use in successive resonance.
		
		@type input: number
		@param input: The value to be resonated.
		
		@rtype: float
		@return: The result of resonance.
		"""
		output = self._resonate(input)
		self._delay_1 = input
		return output
		