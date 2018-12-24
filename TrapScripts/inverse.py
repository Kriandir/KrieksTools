# Script for inverting and storing in seperate folder inverted images.
# (for more info email kriekvdmeulen@gmail.com)


import os
import sys
import argparse
import glob
import numpy as np
import astropy.io.fits as pyfits
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

################################
# Edit this setting to invert other named fits 
imagestofetch = "*image-pb.fits"
################################
global imglist
imglist = []
imagestosave = imagestofetch[1:]

# the inversing step
def ImgInv(hdu1,name,path):

    hdu1[0].data = -1* hdu1[0].data
    dirimage = path
    try:
	    hdu1.writeto(name)
	    imglist.append(dirimage+"/"+name)
    except:
	    os.remove(name)
	    hdu1.writeto(name)
	    imglist.append(dirimage+"/"+name)
    return dirimage

# making directories
path = os.getcwd()
directory = path+"/inv"+imagestosave[:-5]
try:
    os.mkdir(directory)
except:
    pass

#reading in data and opening 
images= glob.glob(os.path.expanduser(imagestofetch))
for i in range(len(images)):
    inhdulist1 = pyfits.open(images[i])
    os.chdir(directory)
    dirimage = ImgInv(inhdulist1,name = images[i].replace(imagestosave,"-inversed-"+imagestosave),path=directory)
    os.chdir(path)
    inhdulist1.close()

#make a new images_to process
os.chdir(dirimage)
try:
    os.remove('images_to_process.py')
except:
    pass
f = open('images_to_process.py', 'w')
f.write('images = ')
f.write('[')
f.writelines(["'%s',\n" % a for a in imglist])
f.write(']\n')
f.write('''#Just for show:
#print "******** IMAGES: ********"
#for f in images:
#    print f
#print "*************************"
''')
f.close()

