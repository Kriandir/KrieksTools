#!/usr/bin/python
#
#
# Author: Antonia Rowlinson
# Co-Author: Kriek van der Meulen (bootstrap/plot)
# E-mail: b.a.rowlinson@uva.nl
# E-mail: kriekvdmeulen@gmail.com
#
from scipy.stats import norm
from scipy.optimize import leastsq
import scipy.stats as ss
import numpy as np
import scipy as sp
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def fit_hist(data, sigma, xlabel, pltname, freq,boot=False):
# fit a Gaussian distribution to the input data, output a plot and threshold for a given sigma
    if len(data) > 100 or boot == True:
        p=guess_p(data)
        mean, rms, threshold = plothist(data, xlabel, pltname, sigma,freq, p)
        return mean, rms, threshold
    else:
        return bootstraps(data,sigma,xlabel,pltname,freq)


def bootstraps(data,sigma,xlabel,pltname,freq):
    """
    If our list of image's is below 100 entries we bootstrap additional data.
    This so we can cutoff at a properly binominal data distribution
    """
    n = np.shape(data)
    steps = n * np.square(np.log(n)**2)
    steps = int(math.ceil(steps))
    databoot= []
    for i in range(steps):
	bootstrapped = []
        index = np.random.choice(np.arange(len(data)),size=n,replace = True)
        for g in index:
            bootstrapped.append(data[g])
        databoot.append(np.mean(np.array(bootstrapped)))
    data = np.append(data,databoot)
    return fit_hist(data,sigma,xlabel,pltname,freq)

def mean_confidence_interval(data,confidence = 0.95):
    a = np.array(data)
    n = len(a)
    m = np.mean(a)
    se =  ss.sem(a)
    h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
    print m,h
    return m, m-h,m+h

def res(p, y, x):
# calculate residuals between data and Gaussian model
  m1, sd1, a = p
#  if m1<min(x):
#      return 1000.
#  else:
  y_fit = a*norm2(x, m1, sd1)
  err = y - y_fit
  return err

def guess_p(x):
# estimate the mean and rms as initial inputs to the Gaussian fitting
    median = np.median(x)
    temp=[n*n-(median*median) for n in x]
    rms = math.sqrt((abs(sum(temp))/len(x)))
    return [median, rms, math.sqrt(len(x))]

def norm2(x, mean, sd):
# creates a normal distribution in a simple array for plotting
    normdist = []
    for i in range(len(x)):
        normdist += [1.0/(sd*np.sqrt(2*np.pi))*np.exp(-(x[i] - mean)**2/(2*sd**2))]
    return np.array(normdist)

def plothist(x, name,filename,sigma,freq,p):
#
# Create a histogram of the data and fit a Gaussian distribution to it
#
    hist_x=np.histogram(x,bins=50) # histogram of data
    range_x=[hist_x[1][n]+(hist_x[1][n+1]-hist_x[1][n])/2. for n in range(len(hist_x[1])-1)]
    plt.hist(x,bins=50,histtype='stepfilled')
    plsq = leastsq(res, p, args = (hist_x[0], range_x)) # fit Gaussian to data
    fit2 = plsq[0][2]*norm2(range_x, plsq[0][0], plsq[0][1]) # create Gaussian distribution for plotting on graph
    plt.plot(range_x,fit2, 'r-', linewidth=3)
    sigcut=plsq[0][0]+plsq[0][1]*sigma # max threshold defined as (mean + RMS * sigma)
    sigcut2=plsq[0][0]-plsq[0][1]*sigma # min threshold defined as (mean - RMS * sigma)
    plt.axvline(x=sigcut, linewidth=2, color='k',linestyle='--')
    plt.axvline(x=sigcut2, linewidth=2, color='k', linestyle='--')
    plt.axvline(x=plsq[0][0],linewidth=1.5,color='k',linestyle='-') # add a solid line for mean
    xvals=np.linspace(min(range_x),max(range_x)+0.1*max(range_x),7) # amount of ticks
    xvals = np.round(xvals,2)
    #xvals = np.append(xvals,plsq[0][0]) #add a tick for the mean
    xlabs=[str(np.round(10.**a,2)) for a in xvals]
    plt.xticks(xvals,xlabs)
    plt.xlabel(name)
    plt.ylabel('Number of images')
    plt.savefig(filename+'_'+str(freq)+'MHz.png')
    plt.close()
    return plsq[0][0], plsq[0][1], sigcut
