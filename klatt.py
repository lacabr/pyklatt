# -*- coding: utf-8 -*-
"""
Klatt CPSC 599 module: klatt

Purpose
=======
 Provides a user interface for this Klatt synthesizer implementation.
 
Legal
=====
 All code, unless otherwise indicated, is original, and subject to the
 terms of the GPLv2, which is provided in COPYING.
 
 Core algorithms derived from the C implementation of the Klatt synthesizer by
 Jon Iles and Nick Ing-Simmons, with full attribution provided in
 ACKNOWLEDGEMENTS.
 
 (C) Neil Tallim, Sydni Bennie, 2009
"""
import optparse
import re
import sys

import src.parwave as parwave
import src.transform as transform
import src.waveform as waveform

#/* for default sampled glottal excitation waveform */
_NATURAL_SAMPLES = (
 -310, -400, 530, 356, 224, 89, 23, -10, -58, -16,
 461, 599, 536, 701, 770, 605, 497, 461, 560, 404,
 110, 224, 131, 104, -97, 155, 278, -154, -1165, -598,
 737, 125, -592, 41, 11, -247, -10, 65, 92, 80,
 -304, 71, 167, -1, 122, 233, 161, -43, 278, 479,
 485, 407, 266, 650, 134, 80, 236, 68, 260, 269,
 179, 53, 140, 275, 293, 296, 104, 257, 152, 311,
 182, 263, 245, 125, 314, 140, 44, 203, 230, -235,
 -286, 23, 107, 92, -91, 38, 464, 443, 176, 98,
 -784, -2449, -1891, -1045, -1600, -1462, -1384, -1261, -949, -730
) #100 values for simulating natural voice, taken from the C implementation.
_SAMPLE_FACTOR = 0.00001

def _main(input_file, options):
	if options.natural_voice:
		options.natural_samples = _NATURAL_SAMPLES
		options.sample_factor = _SAMPLE_FACTOR
		if options.voice_samples:
			if options.verbose:
				print "Loading natural voicing samples from '%s'..." % (options.voice_samples)
			try:
				voice_samples = open(options.voice_samples)
				sample_factor = float(re.match("(\d+(?:\.\d+)?)(?:\r?\n)?", voice_samples.readline()).group(1))
				
				value_regexp = re.compile("(-?\d+)(?:\r?\n)?")
				samples = []
				for line in voice_samples:
					match = value_regexp.match(line)
					if match:
						samples.append(int(match.group(1)))
						
				if options.verbose:
					print "Natural voicing samples loaded: %i samples at a factor of %f." % (len(natural_samples), sample_factor)
				options.natural_samples = tuple(samples)
				options.sample_factor = sample_factor
			except Exception, e:
				sys.stderr.write("Unable to load specified voice samples: %s\n\tUsing defaults.\n" % (e))
	else:
		options.natural_samples = options.sample_factor = None
		
	synthesizer = parwave.KlattSynthesizer(options)
  	wave_form = waveform.WaveForm("output.wav", options.samplerate)
  	chomp_regexp = re.compile("\r?\n$")
	for paragraph in open(input_file):
		paragraph = comp_regexp.sub("", paragraph)
		if not paragraph: #Skip blank lines.
			continue
			
		if options.verbose:
			print "Processing '%s'..." % (paragraph)
		for segment in transform.paragraphToSound(paragraph, options, synthesizer): #Convert and add the paragraph.
			wave_form.addSamples(segment)
		wave_form.addSamples((0,) * (options.samples_per_frame / 2)) #Add a half-second of silence.
	wave_form.close()
	
	
if __name__ == '__main__':
	parser = optparse.OptionParser(usage="%prog [options] <IPA script>", version="%s v%s" % ("Klatt CPSC 599", "pre-alpha"),
	 description="Renders IPA transcriptions as synthesized speech.")
	parser.add_option("-d", "--debug", dest="debug", help="Output statistical information", action="store_true", default=False)
	parser.add_option("-f", "--frame_rate", dest="framerate", help="Set the number of milliseconds per frame", type="int", default=5)
	parser.add_option("-n", "--formant_count", dest="num_formants", help="Set the number of formants in the cascade branch", type="int", default=5)
	parser.add_option("-o", "--simulate_voice", dest="natural_voice", help="Disables natural voicing samples", action="store_false", default=True)
	parser.add_option("-O", "--voice_samples", dest="voice_samples", help="Override default natural voicing samples", type="string", default=None)
	parser.add_option("-p", "--parallel", dest="cascade", help="Disable cascade-parallel behaviour", action="store_false", default=True)
	parser.add_option("-s", "--sample_rate", dest="samplerate", help="Set the sample rate", type="int", default=16000)
	parser.add_option("-v", "--verbose", dest="verbose", help="Output intermediate state information", action="store_true", default=False)
	(options, arguments) = parser.parse_args()
	
	if not arguments:
		sys.stderr.write("No IPA input file specified.\n")
		sys.exit(1)
	del parser
	
	options.samples_per_frame = (options.samplerate * options.framerate) / 1000
	_main(arguments[0], options)
	