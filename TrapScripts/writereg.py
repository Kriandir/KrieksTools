import numpy as np
from astropy.coordinates import SkyCoord
import os,sys


def WriteReg(timescale,possources,fluxsources):
    name = timescale + "_regions.reg"
    try:
         os.remove(name)
    except:
        pass
    f = open(name,'w')
    f.write('# Region file format: DS9 version 4.1 \n')
    f.write('global color=green dashlist=8 3 width=1 font="helvetica 10 normal roman" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1\n')
    f.write('fk5\n')
    for i in possources:
        d = i.c.to_string('hmsdms',sep=':',precision= 3).split(" ")
        f.write('circle('+ d[0] +","+ d[1]+',200\")\n')
        f.write('circle('+ d[0] +","+ d[1]+',20\")\n')

    f.write('global color=red dashlist=8 3 width=1 font="helvetica 10 normal roman" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1\n')
    f.write('fk5\n')
    for i in fluxsources:
        d = i.c.to_string('hmsdms',sep=':',precision= 3).split(" ")
        f.write('circle('+ d[0] +","+ d[1]+',200\")\n')
        f.write('circle('+ d[0] +","+ d[1]+',20\")\n')

