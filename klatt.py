#!
# -*- coding: utf-8 -*-
"""
CPSC 599 module: klatt

Purpose
=======
 Provides a user interface for this Klatt synthesizer implementation.
 
Legal
=====
 All code, unless otherwise indicated, is original, and subject to the
 terms of the GPLv2, which is provided in COPYING.
 
 This project borrows algorithms, ideas, and statistical data from other
 projects. Full attribution is provided in ACKNOWLEDGEMENTS.
 
 (C) Neil Tallim, Sydni Bennie, 2009
"""
import optparse
import re
import sys

import src.parwave as parwave
import src.transform as transform
import src.waveform as waveform

def main(input_file, options):
	"""
	Renders the IPA found in input_file, producing a wavefile containing
	approximate synthetic speech.
	
	@type input_file: basestring
	@param input_file: A file containing synthesizable IPA.
	@type options: optparse.Values
	@param options: The options with which synthesis should occur.
	"""
	synthesizer = parwave.Synthesizer() #The synthesizer that will render speech.
  	wave_form = waveform.WaveForm(options.output) #The wavefile interface to which data will be dumped.
  	chomp_regexp = re.compile("\r?\n$") #A regular expression that cuts newlines off the ends of strings.
  	silent_half_second = synthesizer.generateSilence(500) #Half of a second of silence.
	for paragraph in open(input_file):
		paragraph = chomp_regexp.sub("", paragraph)
		if not paragraph: #Skip blank lines.
			continue
		paragraph = paragraph.decode('utf-8')
		
		for segment in transform.paragraphToSound(paragraph, options, synthesizer): #Convert and add the paragraph.
			wave_form.addSamples(segment)
		wave_form.addSamples(silent_half_second) #Add a half-second of silence.
	wave_form.close()
	
	
if __name__ == '__main__':
	parser = optparse.OptionParser(usage="%prog [options] <IPA script>", version="%s v%s" % ("Klatt CPSC 599", "June 13, 2009"),
	 description="Renders IPA transcriptions as synthesized speech.")
	parser.add_option("-d", "--debug", dest="debug", help="Output statistical information", action="store_true", default=False)
	parser.add_option("-v", "--verbose", dest="verbose", help="Output intermediate state information", action="store_true", default=False)
	parser.add_option("-o", "--output", dest = "output", help="Specify an alternate output wavefile (default: output.wav)", type="string", default="output.wav")
	(options, arguments) = parser.parse_args()
	
	if not arguments:
		parser.print_help()
		sys.exit(1)
	del parser
	
	main(arguments[0], options)
	