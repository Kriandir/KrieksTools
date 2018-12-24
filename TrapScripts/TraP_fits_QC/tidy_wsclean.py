# Corrects the metadata from wsclean images in the working folder so that TraP can read them and recognise them as LOFAR fits images

import pyfits
import glob
import os

images= glob.glob(os.path.expanduser("*image*.fits"))

for img in images:
    hdulist=pyfits.open(img, mode='update')
    prihdr=hdulist[0].header
    del prihdr['BLANK']
    frq = hdulist[0].header['CRVAL3']
    prihdr.update('RESTFRQ',frq)
    prihdr.update('RESTFREQ',frq)
    prihdr.update('SPECSYS', 'LSRK    ')
    prihdr.update('TELESCOP', 'LOFAR Survey')
#    prihdr.rename_key('EPOCH','EQUINOX')
#    prihdr.update('CUNIT1','deg     ')
#    prihdr.update('CUNIT2','deg     ')
#    prihdr.update('CUNIT3','        ')
#    prihdr.update('CUNIT4','m/s     ')
#    prihdr.update('ANTENNA','        ')
    hdulist.flush()
