# Corrects the metadata from wsclean images in the working folder so that TraP can read them and recognise them as LOFAR fits images
# moves deep image up to time as specified in the initial requirements if script is called with move deep images True
# Also moves bad images as made from the image rms to folder badimages
# (for more info email kriekvdmeulen@gmail.com)

import pyfits
import glob
import os
import sys

from datetime import datetime
from datetime import timedelta
path = os.getcwd()
sys.path.insert(0, path)
try:
    from images_to_process import images
    imageproc = True
except:
    imageproc = False


#----------------------------------------------------------#
"""
#If you want to put a deep image in front be sure to edit
#the deep variable into a piece of string that is exclusive to
#your deep image.
#For example, my deepimages are the only images that have 8hr
#in their name thats why I put deep on 8hr
"""
#------------------------------------------------------------#
if len(sys.argv) >1:
    if sys.argv[1].lower() != "n":
        movedeep = True
        deep = sys.argv[1]
    elif sys.argv[1].lower() == "n":
        movedeep = False
    else:
        print "please specify if you don't want to put a deep image in front (n = no)"
        print "or if you do want to put a deep image in front put a piece of string that is exclusive to your deep image here"
        sys.exit()
else:
    print "please specify if you don't want to put a deep image in front (n = no)"
    print "or if you do want to put a deep image in front put a piece of string that is exclusive to your deep image here"
    sys.exit()

#make a bad image folder
directory = path+"/badimages"
try:
    os.mkdir(directory)
except:
    pass
imagez= glob.glob(os.path.expanduser("*image-pb.fits"))
for img in imagez:
    hdulist=pyfits.open(img, mode='update')
    prihdr=hdulist[0].header
    del prihdr['BLANK']
# check if we are moving deep image in front
    if movedeep:
        words = prihdr['HISTORY']
        for word in words:
            # making sure the deep images are put in first
            if deep in word:
                z = datetime.strptime(prihdr['DATE-OBS'][:-2],'%Y-%m-%dT%H:%M:%S')
                d = z - timedelta(seconds=10)
                prihdr['DATE-OBS'] = d.strftime("%Y-%m-%dT%H:%M:%S.0")



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

#   check if there are bad images and move them into bad image folder
    if imageproc:
        if any(str(img) in s for s in images):
            continue
        else:
            oldir = path +"/"+str(img)
            newdir = directory +"/" + str(img)
            os.rename(oldir,newdir)

# if there is no images_to_process create one
if not imageproc:
    f = open('images_to_process.py', 'w')
    f.write('images = ')
    f.write('[')
    f.writelines(["\'"+path+"/"+"%s',\n" % a for a in imagez])
    f.write(']\n')
    f.write('''#Just for show:
    #print "******** IMAGES: ********"
    #for f in images:
    #    print f
    #print "*************************"
    ''')
    f.close()
print 'done'
