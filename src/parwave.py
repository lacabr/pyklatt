# -*- coding: utf-8 -*-
"""
Klatt CPSC 599 module: src.parwave

Purpose
=======
 Provides functionality for generating waveform samples from format parameter
 data.
 
Legal
=====
 All code, unless otherwise indicated, is original, and subject to the
 terms of the GPLv2, which is provided in COPYING.
 
 Core algorithms derived from the C implementation of the Klatt synthesizer by
 Jon Iles and Nick Ing-Simmons, with full attribution provided in
 ACKNOWLEDGEMENTS.
 
 (C) Neil Tallim, Sydni Bennie, 2009
"""
import math
import random

_DB_TO_AMP_MAP = (
 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 6.0, 7.0,
 8.0, 9.0, 10.0, 11.0, 13.0, 14.0, 16.0, 18.0, 20.0, 22.0, 25.0, 28.0, 32.0,
 35.0, 40.0, 45.0, 51.0, 57.0, 64.0, 71.0, 80.0, 90.0, 101.0, 114.0, 128.0,
 142.0, 159.0, 179.0, 202.0, 227.0, 256.0, 284.0, 318.0, 359.0, 405.0,
 455.0, 512.0, 568.0, 638.0, 719.0, 811.0, 911.0, 1024.0, 1137.0, 1276.0,
 1438.0, 1622.0, 1823.0, 2048.0, 2273.0, 2552.0, 2875.0, 3244.0, 3645.0, 
 4096.0, 4547.0, 5104.0, 5751.0, 6488.0, 7291.0, 8192.0, 9093.0, 10207.0, 
 11502.0, 12976.0, 14582.0, 16384.0, 18350.0, 20644.0, 23429.0,
 26214.0, 29491.0, 32767.0
)

class KlattSynthesizer(object):
	_minus_pi_t = None
	_n_mod = 0
	_n_open = 0
	_n_per = 0
	_r1p = None
	_rout = None
	_pulse_shape_a = 0.0
	_pulse_shape_b = 0.0
	_two_pi_t = None
	_t0 = 0
	_v_wave = 0.0
	
	def __init__(self, options):
		self._minus_pi_t = -math.pi / options.samplerate
		self._two_pi_t = -2.0 * self._minus_pi_t
		
		flp_hz = (950 * options.samplerate) / 10000
		blp_hz = (630 * options.samplerate) / 10000
		self._r1p = _Resonator(flp_hz, blp_hz, self._minus_pi_t, self._two_pi_t)
		self._rout = _Resonator(0.0, options.samplerate / 2, self._minus_pi_t, self._two_pi_t)
		
	def reset(self):
		self._n_mod = self._n_open = self._n_per = self._t0 = 0
		self._pulse_shape_a = self._pulse_shape_b = self._v_wave = 0.0
		
	def _frame_init(self, parameters, options):
		(fgp, fgz, fgs, fnp, fnz,
		 f1, f2, f3, f4, f5, f6,
		 bgp, bgz, bgs, bnp, bnz,
		 bw1, bw2, bw3, bw4, bw5, bw6,
		 a2, a3, a4, a5, a6,
		 ab, ah, af, av, avs,
		 duration) = parameters
		
		av_db = max(av - 7, 0) 
		amp_aspiration = self._dbToLin(ah) * 0.05
		amp_frication = self._dbToLin(af) * 0.25
		par_amp_voice = self._dbToLin(av)
		
		amp_par_fnp = self._dbToLin(avs) * 0.6
		amp_bypass = self._dbToLin(ab) * 0.05
		
		amp_gain_0 = 0.318 #dbToLin(47)
		
		cascade_resonators = []
		if options.cascade:
			cascade_resonators = [
			 _Resonator(f1, bw1, self._minus_pi_t, self._two_pi_t),
			 _Resonator(f2, bw2, self._minus_pi_t, self._two_pi_t),
			 _Resonator(f3, bw3, self._minus_pi_t, self._two_pi_t),
			 _Resonator(f4, bw4, self._minus_pi_t, self._two_pi_t)
			]
			if options.num_formants > 4:
				cascade_resonators.append(_Resonator(f5, bw5, self._minus_pi_t, self._two_pi_t))
			if options.num_formants > 5:
				cascade_resonators.append(_Resonator(f6, bw6, self._minus_pi_t, self._two_pi_t))
			if options.samplerate >= 16000:
				if options.num_formants > 6:
					cascade_resonators.append(_Resonator(6500, 500, self._minus_pi_t, self._two_pi_t))
				if options.num_formants > 7:
					cascade_resonators.append(_Resonator(7500, 600, self._minus_pi_t, self._two_pi_t))
		cascade_resonators = tuple(cascade_resonators)
		
		zero_resonator = _Resonator(fnz, bnz, self._minus_pi_t, self._two_pi_t)
		nasal_resonator = _Resonator(fnp, bnp, self._minus_pi_t, self._two_pi_t)
		
		parallel_nasal_resonator = _Resonator(fnp, bnp, self._minus_pi_t, self._two_pi_t)
		parallel_nasal_resonator.multiplyAmplitude(amp_par_fnp)
		
		parallel_resonators = (
			_Resonator(f1, bw1, self._minus_pi_t, self._two_pi_t),
			_Resonator(f2, bw2, self._minus_pi_t, self._two_pi_t),
			_Resonator(f3, bw3, self._minus_pi_t, self._two_pi_t),
			_Resonator(f4, bw4, self._minus_pi_t, self._two_pi_t),
			_Resonator(f5, bw5, self._minus_pi_t, self._two_pi_t),
			_Resonator(f6, bw6, self._minus_pi_t, self._two_pi_t)
		)
		parallel_resonators[0].multiplyAmplitude(self._dbToLin(av) * 0.4)
		parallel_resonators[1].multiplyAmplitude(self._dbToLin(a2) * 0.15)
		parallel_resonators[1].multiplyAmplitude(self._dbToLin(a3) * 0.06)
		parallel_resonators[1].multiplyAmplitude(self._dbToLin(a4) * 0.04)
		parallel_resonators[1].multiplyAmplitude(self._dbToLin(a5) * 0.022)
		parallel_resonators[1].multiplyAmplitude(self._dbToLin(a6) * 0.03)
		
		self._rout.reset()
		
		return (parallel_resonators, parallel_nasal_resonator, nasal_resonator, zero_resonator, cascade_resonators,
		 av_db, amp_aspiration, amp_frication, par_amp_voice, amp_bypass, amp_gain_0, duration)
		
	def _voiceNatural(self, options):
		if not self._t0 == 0:
			f_val = (float(self._n_per) / self._t0) * len(options.natural_samples)
			i_val = int(f_val)
			diff_val = f_val - i_val
			i_val %= 100
			
			current_value = options.natural_samples[i_val]
			next_value = options.natural_samples[i_val + 1]
			diff_value = (next_value - current_value) * diff_val
			
			return (current_value + diff_value) * options.sample_factor
		return 0
		
	def _voiceSimulated(self):
		if self._n_per < self._n_open:
			self._pulse_shape_a -= self._pulse_shape_b
			self._v_wave += self._pulse_shape_a
			return self._v_wave * 0.028
		else:
			self._v_wave = 0.0
			return 0.0
			
	def _pitchSynchParReset(self, parameters, options):
		self._t0 = 4
		self._n_mode = self._t0
		self._pulse_shape_a = 0.0
		self._pulse_shape_b = 0.0
		
		return (0.0, 0.0)
		
	def synthesize(self, parameters, options):
		(parallel_resonators, parallel_nasal_resonator, nasal_resonator, zero_resonator, cascade_resonators,
		 av_db, amp_aspiration, amp_frication, par_amp_voice, amp_bypass, amp_gain_0, duration) = self._frame_init(parameters, options)
		noise = voice = vlast = glottal_last = 0
		amp_voice = amp_breath = 0.0
		decay = 0.33
		onemd = 0.67
		voice = None
		
		sound = []
		for i in xrange(options.samples_per_frame * duration):
			applied_noise = noise = (noise / 2) + random.randint(-8191, 8191) #Add some noise to the signal.
			
			if self._n_per > self._n_mod: #Reduce noise if voicing present during second half of glottal period.
				applied_noise *= 0.5
				
			frication_noise = amp_frication * applied_noise
			
			#Compute voicing waveform. The glottal source is simulated at 4x the
			#normal sample rate to minimize quantation noise in the period of
			#female voices. (According to the C implementation, anyway)
			for j in xrange(4):
				if options.natural_voice:
					voice = self._voiceNatural(options)
				else:
					voice = self._voiceSimulated()
				voice = self._r1p.resonate(voice)
				
				if self._n_per >= self._t0:
					self._n_per = 0
					(amp_voice, amp_breath) = self._pitchSynchParReset(parameters, options)
					
				self._n_per += 1
				
			voice = voice * onemd + vlast * decay
			vlast = voice
			
			if self._n_per < self._n_open:
				voice += amp_breath * applied_noise
				
			#Set voicing amplitude.
			glottal_output = amp_voice * voice
			par_glottal_output = par_amp_voice * voice
			
			#Add aspiration amplitude.
			aspiration = amp_aspiration * applied_noise
			glottal_output += aspiration
			par_glottal_output += aspiration
			
			#Apply cascade resonance, if enabled.
			output = 0
			if options.cascade:
				output = zero_resonator.resonate(glottal_output)
				output = nasal_resonator.resonate(output)
				for resonator in reversed(cascade_resonators):
					output = resonator.resonate(output)
					
			#Voice waveform.
			output += self._r1p.resonate(par_glottal_output)
			output += parallel_nasal_resonator.resonate(par_glottal_output)
			
			source = frication_noise + par_glottal_output - glottal_last
			glottal_last = par_glottal_output
			
			for resonator in reversed(parallel_resonators):
				output = resonator.resonate(source) - output
			output = (amp_bypass * source) - output
			
			output = self._rout.resonate(output)
			
			#Express as a 16-bit integer.
			value = int(output * amp_gain_0)
			if value < -32768:
				value = -32768
			elif value > 32767:
				value = 32767
				
			sound.append(value)
			print value
		return tuple(sound)
		
	def _dbToLin(self, db):
		"""
		Converts decibel values into linear values, using a lookup table.
		
		@type db: int
		@param db: The decibel value to convert.
		
		@rtype: float
		@return: The linear scale value.
		"""
		if db < 0 or db > 87:
			return 0.0
		else:
			return _DB_TO_AMP_MAP[db] * 0.001
			
			
class _Resonator(object):
	_a = None
	_b = None
	_c = None
	_p1 = 0.0
	_p2 = 0.0
	
	def __init__(self, frequency, bandwidth, minus_pi_t, two_pi_t):
		"""
		Computes resonator co-efficients.
		"""
		r = math.e ** (minus_pi_t * bandwidth)
		self._c = -(r ** 2)
		self._b = r * math.cos(two_pi_t * frequency) * 2.0
		self._a = 1.0 - self._b - self._c
		
	def reset(self):
		self._p1 = self._p2 = 0.0
		
	def _resonate(self, input):
		output = self._a * input + self._b * self._p1 + self._c * self._p2
		self._p2 = self._p1
		return output
		
	def resonate(self, input):
		output = self._resonate(input)
		self._p1 = output
		return output
		
	def multiplyAmplitude(self, modifier):
		self._a *= modifier
		
class _AntiResonator(_Resonator):
	def __init__(self, frequency, bandwidth, minus_pi_t, two_pi_t):
		"""
		Computes resonator co-efficients, then converts them to anti-resonator
		co-efficients.
		"""
		_Resonator.__init__(self, min(-frequency, -1), bandwidth, minus_pi_t, two_pi_t)
		self._a = 1.0 / self._a
		self._b *= -self._a
		self._c = self._b
		
	def resonate(self, input):
		output = self._resonate(input)
		self._p1 = input
		return output
		