#!/usr/bin/env python
__author__ = 'Jon Stratton'
import sys, getopt, brion_pysin_lib

###############
# Global Vars #
###############

in_string  = ''
frag_type  = 'word'
min_chunk  = 1
max_chunk  = 3
randomness = 75

##############
# Parse Args #
##############

myopts, args = getopt.getopt(sys.argv[1:],'s:m:x:t:r:')
for o, a in myopts:
   if o == '-s':
      in_string  = a
   elif o == '-m':
      min_chunk  = int(a)
   elif o == '-x':
      max_chunk  = int(a)
   elif o == '-r':
      randomness = int(a)
   elif o == '-t':
      frag_type  = a

def main():
   cutup_text = brion_pysin_lib.traditional_cutup( in_string, frag_type, min_chunk, max_chunk, randomness )
   print( '%s' % cutup_text )
   return 0

main()
