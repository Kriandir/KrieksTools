import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from astropy.wcs import WCS
from astropy.nddata.utils import Cutout2D
from astropy import units as u
from astropy.coordinates import SkyCoord

# READ IN FITS
def Imager(imagefile,ra,dec):
    hdu_list = fits.open(imagefile)
    hdu_list.info()
    image_data = hdu_list[0].data
    # grab wcs from imageslice
    w = WCS(hdu_list[0].header)
    size = u.Quantity((120, 120), u.pixel)
    c = SkyCoord(ra, dec, frame='fk5', unit='deg')
    # RESHAPE DATA FOR PROPER FORMAT
    shape = (image_data.shape)
    image_data = np.reshape(image_data,(shape[2],shape[3]))
    hdu_list.close()

    # make wcss frame like in cutout
    wcss = WCS(naxis=2)
    wcss.wcs.ctype = ['RA---SIN','DEC--SIN']

    wcss.wcs.crval = [w.wcs.crval[0],w.wcs.crval[1]]
    wcss.wcs.crpix = [ w.wcs.crpix[0],w.wcs.crpix[1]]
    wcss.wcs.cdelt = [w.wcs.cdelt[0],w.wcs.cdelt[1]]

    # plot and save the data
    try:
        plt.figure(figsize=(10,10))
        cutout1 = Cutout2D(image_data, c,size,wcs=wcss)
        plt.imshow(cutout1.data, origin='lower')
    except:
        # plot and save the data
        print 'failed centering'
        plt.figure(figsize=(10,10))
        plt.imshow(image_data, origin='lower')
    plt.colorbar()
    plt.savefig(imagefile.replace(".fits",".png"))
    plt.show()
