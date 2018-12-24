# Removes bad images from the output of wsclean and puts the 8hr image in front also corrects for wsclean so it can be read into Trap
# (for more info email kriekvdmeulen@gmail.com)

import pyfits
import glob
import os
import numpy as np

pictobeputinfront = "8hr"
time = '2014-06-28T12:59:00.0'
images= glob.glob(os.path.expanduser("*image*.fits"))
for img in images:
    hdulist=pyfits.open(img, mode='update')
    prihdr=hdulist[0].header
    data = hdulist[0].data
    if not np.isnan([data]).any():

        del prihdr['BLANK']
        words = prihdr['HISTORY']
#        for word in words:
 #           if pictobeputinfront in word:
  #              prihdr['DATE-OBS'] = time
        frq = hdulist[0].header['CRVAL3']
        prihdr.update('RESTFRQ',frq)
        prihdr.update('RESTFREQ',frq)
        prihdr.update('SPECSYS', 'LSRK    ')
        prihdr.update('TELESCOP', 'LOFAR Survey')
    else:
        print "Bad data detected, removing image: " + str(img)
#        os.remove(str(img))
#    prihdr.rename_key('EPOCH','EQUINOX')
#    prihdr.update('CUNIT1','deg     ')
#    prihdr.update('CUNIT2','deg     ')
#    prihdr.update('CUNIT3','        ')
#    prihdr.update('CUNIT4','m/s     ')
#    prihdr.update('ANTENNA','        ')
    hdulist.flush()
