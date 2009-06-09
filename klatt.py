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

def _main(input_file, options):
	synthesizer = parwave.Synthesizer()
  	wave_form = waveform.WaveForm("output.wav")
  	chomp_regexp = re.compile("\r?\n$")
	for paragraph in open(input_file):
		paragraph = chomp_regexp.sub("", paragraph)
		if not paragraph: #Skip blank lines.
			continue
		paragraph = paragraph.decode('utf-8')
		
		if options.verbose:
			print "Processing '%s'..." % (paragraph)
		for segment in transform.paragraphToSound(paragraph, options, synthesizer): #Convert and add the paragraph.
			wave_form.addSamples(segment)
		wave_form.addSamples(synthesizer.generateSilence(500)) #Add a half-second of silence.
	wave_form.close()
	
	
if __name__ == '__main__':
	parser = optparse.OptionParser(usage="%prog [options] <IPA script>", version="%s v%s" % ("Klatt CPSC 599", "pre-alpha"),
	 description="Renders IPA transcriptions as synthesized speech.")
	parser.add_option("-d", "--debug", dest="debug", help="Output statistical information", action="store_true", default=False)
	parser.add_option("-v", "--verbose", dest="verbose", help="Output intermediate state information", action="store_true", default=False)
	(options, arguments) = parser.parse_args()
	
	if not arguments:
		sys.stderr.write("No IPA input file specified.\n")
		sys.exit(1)
	del parser
	
	_main(arguments[0], options)
	