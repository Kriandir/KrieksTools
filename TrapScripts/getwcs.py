# Prints out the wcs coordinates easily for a specific fits
# (for more info email kriekvdmeulen@gmail.com)

import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from astropy.nddata.utils import Cutout2D
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.wcs import WCS
from astropy import wcs
import sys

if len(sys.argv) <1:
    print "please specify fits you wish to get wcs from"
    sys.exit()
else:
    filename = str(sys.argv[1])
    hdulist = fits.open(filename)
    w = WCS(hdulist[0].header)
    print w
    print w.wcs.cdelt
    print w.wcs.crval[1]
    print w.wcs.crpix[0]
    c = SkyCoord(w.wcs.crval[0],w.wcs.crval[1],frame = 'fk5',unit='deg')
    print "Position of image: " + c.to_string('hmsdms')
