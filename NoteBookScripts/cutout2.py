import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from astropy.nddata.utils import Cutout2D
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.wcs import WCS


imagefile = "../IMAGES/December/26_8192_4asec_all_1hr/1hr_allband_autothresh-t0004-image-pb.fits"

def PlotterFunction(image_data,c,wcss,ids,size,database):
    print c
    print wcss
    print size
    print image_data
    # GET CUTOUT AND PLOT IT
    plt.figure(figsize = (10,10))
    cutout1 = Cutout2D(image_data, c,size,wcs=wcss)
    plt.imshow(cutout1.data, origin='lower')
    plt.colorbar()
    plt.savefig(str(ids)+"cutout_"+database+".png")
    plt.show()

def GetCutout(imagefile,ra,dec,ids,pixels,database = 'own'):

    # READ IN FITS FILE
    hdu_list = fits.open(imagefile)
    print imagefile
    print hdu_list[0].data
    image_data = hdu_list[0].data
    w = WCS(hdu_list[0].header)
    print np.shape(image_data)

    # GET LOCATION OF SOURCE AND SIZE OF PICTURE
    size = u.Quantity(pixels, u.pixel)
    c = SkyCoord(ra, dec, frame='fk5', unit='deg')
    print size

    # DEFINE WCS COORDINATE SYSTEM FROM FITS FILE
    wcss = WCS(naxis=2)
    wcss.wcs.ctype = ['RA---SIN','DEC--SIN']
    wcss.wcs.crval = [w.wcs.crval[0],w.wcs.crval[1]]
    wcss.wcs.crpix = [ w.wcs.crpix[0],w.wcs.crpix[1]]

    try:
        # FIRST TRY CDELT
        wcss.wcs.cd = [w.wcs.cd[0],w.wcs.cd[1]]


    except:
        wcss.wcs.cdelt = [w.wcs.cdelt[0],w.wcs.cdelt[1]]

    print wcss
    print size
    print w
    print database
    if database =='vlsrr':
        print 'hoi'
        shape = (image_data.shape)
        image_data2 = np.reshape(image_data,((shape[2],shape[3])))
    print np.shape(image_data)
    print np.shape(image_data2)
    print 'hoi'
    
    PlotterFunction(image_data,c,wcss,size,ids,database)

    hdu_list.close()
