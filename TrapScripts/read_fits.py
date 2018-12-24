# Reads the metadata from fits images specified and prints them out in a semi-orderly fashion
# (for more info email kriekvdmeulen@gmail.com)

import pyfits
import glob
import os
import sys

if len(sys.argv) <2:
    print "\n please enter a .fits file you want to view the head of\n"
    sys.exit()
img = sys.argv[1]

hdulist=pyfits.open(img, mode='update')
prihdr=hdulist[0].header
del prihdr['BLANK']
print prihdr.keys
data = hdulist[0].data
print data
hdulist.flush()
