import numpy as np
import pandas as pd
import sys,os
import astropy.io.fits as pyfits
import argparse
import glob

def Reader(name):

    return pd.read_csv('asu.tsv', sep=';',header=44)
