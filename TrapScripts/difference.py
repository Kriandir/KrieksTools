import os
import sys
import argparse
import glob
import numpy as np
import astropy.io.fits as pyfits
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd


imagestofetch = "*image-pb.fits"
global deep
global imglist
imglist = []
deep = '8hr'
imagestosave = imagestofetch[1:]
if len(sys.argv) == 1:
    sys.exit("Usage: add a procedure: 0 = normal diff, 1 = averaging diff ")
    exit()
elif len(sys.argv) == 2:
    differ = sys.argv[1]
    cor0 = False
elif len(sys.argv) ==3:
    differ = sys.argv[1]
    if sys.argv[2].lower() == 'true':
        cor0 = True
    elif sys.argv[2].lower() == 'false':
        cor0 = False
    else:
        sys.exit("please specify true or false properly as second argument")
        exit()
else:
    sys.exit("Usage: add a procedure: 0 = normal diff, 1 = averaging diff ")
    exit()

# the diveraging step
def ImgDiff(hdu1,hdu2,name,cor0,path):
    if cor0:
        name = name.replace(imagestosave,"-cor0-"+imagestosave)
        hdu1[0].data = hdu1[0].data.clip(min=0)
        hdu2[0].data = hdu2[0].data.clip(min=0)
        dirimage = path+"/correct0"
        try:
            os.mkdir(dirimage)
        except:
            pass
        os.chdir(dirimage)
        hdu1[0].data =  hdu1[0].data - hdu2[0].data
        try:
            hdu1.writeto(name)
            imglist.append(dirimage+"/"+name)
    	except:
    	    os.remove(name)
    	    hdu1.writeto(name)
    	    imglist.append(dirimage+"/"+name)
            os.chdir(path)

    else:
        hdu1[0].data =  hdu1[0].data - hdu2[0].data
        dirimage = path
        try:
    	    hdu1.writeto(name)
    	    imglist.append(dirimage+"/"+name)
    	except:
    	    os.remove(name)
    	    hdu1.writeto(name)
    	    imglist.append(dirimage+"/"+name)
    return dirimage

# the averaging step
def ImgAvg(hdu1,hdu2,hdu3,hdu4):
    hdu2[0].data = (hdu2[0].data+hdu4[0].data)/2
    hdu1[0].data = (hdu1[0].data + hdu3[0].data)/2
    return hdu1,hdu2

# selects which differ method we want to use.. either the simple take two images diff,
# the harder take 4 average alternating and diff or take 2 sets of 4 average alternating and take diff of combined values.
def Diffselector(differ,cor0):

    if differ == 0:
        path = os.getcwd()
        directory = path+"/diff"+imagestosave[:-5]
        try:
            os.mkdir(directory)
        except:
            pass
        images= glob.glob(os.path.expanduser(imagestofetch))
        deepimg = [images.pop(a) for a in range(len(images)) if deep in images[a]]
        images.sort()
        im2 = images[1::2]
        im1 = images[0::2]
	print im1
	print im2
	im1.sort()
	print im1
        maxlength = min(len(im1),len(im2))
        while True:
            if len(im2)>maxlength:
                im2 = im2[:-1]
            elif len(im1)>maxlength:
                im1 = im1[:-1]
            else:
                break

        for i in range(maxlength):
            inhdulist1 = pyfits.open(im1[i])
            inhdulist2 = pyfits.open(im2[i])
            os.chdir(directory)
            dirimage = ImgDiff(inhdulist1,inhdulist2,name = im1[i].replace(imagestosave,"-differated-"+imagestosave),cor0=cor0,path=directory)
            os.chdir(path)
            inhdulist1.close()
            inhdulist2.close()

    if differ == 1 or differ == 2:
        images= glob.glob(os.path.expanduser(imagestofetch))
        deepimg=[images.pop(a) for a in range(len(images)) if deep in images[a]]
        im2 = images[1::4]
        im1 = images[0::4]
        im3 = images[2::4]
        im4 = images[3::4]
        maxlength = min([len(im1),len(im2),len(im3),len(im4)])
        print maxlength
        while True:
            if len(im2)>maxlength:
                im2 = im2[:-1]
            elif len(im1)>maxlength:
                im1 = im1[:-1]
            elif len(im3)>maxlength:
                im3 = im3[:-1]
            elif len(im4)>maxlength:
                im4 = im4[:-1]
            else:
                break

        if differ == 1:
            path = os.getcwd()
            directory = path+"/diffandavg"+imagestosave[:-5]
            try:
                os.mkdir(directory)
            except:
                pass
            for i in range(maxlength):
                inhdulist1 = pyfits.open(im1[i])
                inhdulist2 = pyfits.open(im2[i])
                inhdulist3 = pyfits.open(im3[i])
                inhdulist4 = pyfits.open(im4[i])
                hdu1,hdu2 = ImgAvg(inhdulist1,inhdulist2,inhdulist3,inhdulist4)
                os.chdir(directory)
                dirimage = ImgDiff(hdu1,hdu2,name = im1[i].replace(imagestosave,"-differatedandavg-"+imagestosave),cor0=cor0,path=directory)
                os.chdir(path)
                inhdulist1.close()
                inhdulist2.close()
                inhdulist3.close()
                inhdulist4.close()
        if differ == 2:
            path = os.getcwd()
            directory = path+"/diffandavgmulti"+imagestosave[:-5]
            try:
                os.mkdir(directory)
            except:
                pass
            for i in range(maxlength-1):
                inhdulist1 = pyfits.open(im1[i])
                inhdulist2 = pyfits.open(im2[i])
                inhdulist3 = pyfits.open(im3[i])
                inhdulist4 = pyfits.open(im4[i])
                inhdulist5 = pyfits.open(im1[i+1])
                inhdulist6 = pyfits.open(im2[i+1])
                inhdulist7 = pyfits.open(im3[i+1])
                inhdulist8 = pyfits.open(im4[i+1])
                hdu1,hdu2 = ImgAvg(inhdulist1,inhdulist2,inhdulist3,inhdulist4)
                hdu3,hdu4 = ImgAvg(inhdulist5,inhdulist6,inhdulist7,inhdulist8)
                hdu5,hdu6 = ImgAvg(hdu1,hdu2,hdu3,hdu4)
                os.chdir(directory)
                dirimage = ImgDiff(hdu5,hdu6,name = im1[i].replace(imagestosave,"-differatedandavgmulti-"+imagestosave),cor0=cor0,path=directory)
                os.chdir(path)
                inhdulist1.close()
                inhdulist2.close()
                inhdulist3.close()
                inhdulist4.close()
                inhdulist5.close()
                inhdulist6.close()
                inhdulist7.close()
                inhdulist8.close()
    try:
        return deepimg[0],dirimage
    except:
        return None,dirimage


#TODO FIX THE DIRECTORY IF I CANT FIX IT SHORTLY NOW
# IT IS THE DIRECTORY WHERE THE IMAGE TO PROCESS GETES READIN AND REPLACED WE NEED TO FIX THAT.


deepimg,dirimage = Diffselector(int(differ),cor0)
if deepimg:
    imglist.append(deepimg)

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


# # Provide information to the argparse routine if we need it
# parser= argparse.ArgumentParser(description = 'Display a fits image')
#
# # Test for command line arguments

# Open the fits file and create an hdulist
# inhdulist = pyfits.open(infits)
#
# # pyfits.writeto('yolo.fits',inhdulist)
# # Assign the input header in case it is needed later
# inhdr = inhdulist[0].header
# print inhdr
#
# # Assign image data to a numpy array
# image_data =  inhdulist[0].data
# print image_data
# # a = np.zeros(np.shape(image_data))
# # print a
# # inhdulist[0].data = a
# # inhdulist[0].data = image_data
# inhdulist.writeto('random2.fits')



#
#
# # Necessary for imaging
#
# # Print information about the image
# print 'Size: ', image_data.size
# print 'Shape: ', image_data.shape
# # print image_data[:,0]
# # print 'hoi'
# # print image_data[:,0][0]
# # print 'hoi'
# # print image_data[:,0][0][0]
# # print 'hoi'
# # print image_data[:,0][0][0][0]
#
#
# image_data = image_data.reshape(4096,4096)
#
# print 'Shape: ', image_data.shape
# # Show the image
# new_image_data = lingray(image_data,-0.5,0.5)
# new_image_min = -0.5
# new_image_max = 0.5
# # matplotlib.pyplot.imshow(new_image_data, vmin = new_image_min, vmax = new_image_max, cmap ='gray')
# # matplotlib.pyplot.show()
#
# # Close the input image file and exit
# inhdulist.close()
# exit ()
