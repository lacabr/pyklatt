# -*- coding: utf-8 -*-
"""
Klatt CPSC 599 module: src.transform

Purpose
=======
 Applies rules and generates synthetic speech, given IPA input.
 
Legal
=====
 All code, unless otherwise indicated, is original, and subject to the
 terms of the GPLv2, which is provided in COPYING.
 
 (C) Neil Tallim, Sydni Bennie, 2009
"""
import re

import ipa
import language_rules
import parwave
import universal_rules

_WORD_REGEXP = re.compile('([*"]*)(\w[\w<>]+[:,]?)([*".!?]*)')

_SENTENCE_QUESTION = 1
_SENTENCE_EXCLAMATION = 2

_WORD_QUOTED = 1
_WORD_EMPHASIZED = 2

def paragraphToSound(paragraph, options):
	tokens = paragraph.split()
	
	sentences = []
	while tokens:
		(sentence, tokens) = _extractSentence(tokens)
		sentences.append(sentence)
	if options.verbose:
		print "\tParagraph analyzed."
	if options.debug:
		print sentences
		
	silent_half_second = ((0,) * (options.samples_per_second / 2))
	sounds = []
	for (i, sentence) in enumerate(sentences): #Add the sentence, plus a half-second of silence.
		sounds.append(_sentenceToSound(sentence, i + 1, len(sentences) - i - 1, options))
		sounds.append(silent_half_second)
	return sounds
	
def _sentenceToSound(sentence, position, remaining_sentences, options):
	(words, markup) = sentence
	
	is_question = _SENTENCE_QUESTION in markup
	is_exclamation = _SENTENCE_EXCLAMATION in markup
	
	silent_sixth_second = ((0,) * (options.samples_per_second / 6))
	sounds = ()
	for (i, word) in enumerate(words): #Add the word, plus a sixth of a second of silence.
		sounds += _wordToSound(word, i + 1, len(words) - i - 1, sentence_position, remaining_sentences, is_question, is_exclamation, options)) + silent_sixth_second
	return sounds
	
def _wordToSound(word, position, remaining_words, sentence_position, remaining_sentences, is_question, is_exclamation, options):
	(token, markup) = word
	
	is_quoted = _WORD_QUOTED in markup
	is_emphasized = _WORD_EMPHASIZED in markup
	
	terminal_pause = ()
	if token.endswidth((',', ':')):
		terminal_pause = ((0,) * (options.samples_per_second / 6)) #A sixth of a second of silence.
		token = token[:-1]
		
	phonemes = []
	multiplier = 1.0
	subject = token[0]
	for i in token[1:]:
		if i == '>':
			multiplier *= 1.5
		elif i == '<':
			multiplier *= 0.5
		else:
			phonemes.append((subject, multiplier))
			subject = i
			multiplier = 1.0
	phonemes.append((subject, multiplier))
	
	if options.verbose:
		print "\tSynthesizing '%s'..." % (''.join([phoneme for (phoneme, multiplier) in phonemes]))
		
	sounds = ()
	for (i, phoneme) in enumerate(phonemes):
		sounds += _phonemeToSound(phoneme, [p for (p, d) in phonemes[:i]], [p for (p, d) in phonemes[i + 1:]], position, remaining_words, sentence_position, remaining_sentences, is_quoted, is_emphasized, is_question, is_exclamation, options)
	return sounds
	
def _phonemeToSound(phoneme, preceding_sounds, following_sounds, word_position, remaining_words, sentence_position, remaining_sentences, is_quoted, is_emphasized, is_question, is_exclamation, options):
	(ipa_character, duration_multiplier) = phoneme
	
	#Retrieve formant parameters for the IPA character.
	
	#Apply universal rules to the parameters.
	
	#Apply language-specific rules to the parameters.
	
	#Synthesize sound.
	
	#Return sound.
	
	"""
  icount=0;
  done_flag = FALSE;
  parwave_init(globals);
  frame_ptr = (long*) frame;

  while(done_flag == FALSE)
  {
    for (par_count = 0; par_count < NPAR; ++par_count)
    {
      value = 0;

#ifdef __BORLANDC__
      result = fscanf(infp,"%ld",&value);
#else
      result = fscanf(infp,"%i",(int*)&value);
#endif

      frame_ptr[par_count] = value;
    }
    
    if(result == EOF)
    {
      done_flag = TRUE;
    }
    else
    {
      parwave(globals,frame,iwave);

      if(globals->quiet_flag == FALSE)
      {
	printf("\rFrame %i",icount);
	fflush(stdout);
      }

      for (isam = 0; isam < globals->nspfr; ++ isam)
      { 
	if(raw_flag == TRUE)
	{
	  low_byte = iwave[isam] & 0xff;
	  high_byte = iwave[isam] >> 8;

	  if(raw_type==1)
	  {
	    fprintf(outfp,"%c%c",high_byte,low_byte);
	  }
	  else
	  {
	    fprintf(outfp,"%c%c",low_byte,high_byte);
	  }
	}
	else
	{
	  fprintf(outfp,"%i\n",iwave[isam]);
	}
      }
      icount++;
    }
  }
}
	"""

def _extractSentence(tokens):
	word_regexp = _WORD_REGEXP
	word_quoted = _WORD_QUOTED
	word_emphasized = _WORD_EMPHASIZED
	
	words = []
	markup = []
	
	quotation = False
	emphasis = False
	while tokens:
		token = tokens.pop(0)
		match = word_regexp.match(token)
		if not match:
			raise ValueError("Invalid token in IPA input: %s" % (token))
			
		if '"' in match.group(0):
			quotation = True
		if '*' in match.group(0):
			emphasis = True
			
		word_markup = []
		if quotation:
			word_markup.append(word_quoted)
		if emphasis:
			word_markup.append(word_emphasized)
		if word_markup:
			word_markup = tuple(word_markup)
		else:
			word_markup = None
		words.append((match.group(1), word_markup))
		
		if '"' in match.group(2):
			quotation = False
		if '*' in match.group(2):
			emphasis = False
			
		if '.' in match.group(2):
			break
		elif '?' in match.group(2):
			markup.append(_SENTENCE_QUESTION)
			if '!' in match.group(2):
				markup.append(_SENTENCE_EXCLAMATION)
			break
		elif '!' in match.group(2):
			if '?' in match.group(2):
				markup.append(_SENTENCE_QUESTION)
			markup.append(_SENTENCE_EXCLAMATION)
			break
			
	if markup:
		markup = tuple(markup)
	else:
		markup = None
	return ((words, markup), tokens)
	