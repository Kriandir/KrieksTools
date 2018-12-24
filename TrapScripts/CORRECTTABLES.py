import pyrap.tables as pt
import os
import sys
import glob
import numpy as np

images = glob.glob(os.path.expanduser("*.ms"))
for msfile in images:
    t = pt.table(msfile,readonly=False)

    f = t.getcol("DD_PREDICT")
    d=t.getcol("DATA_DI_CORRECTED")

    desc= t.getcoldesc("DATA_DI_CORRECTED")
    desc['name']="DATA_SUB"
    t.addcols(desc)
    t.putcol('DATA_SUB',d-f)
