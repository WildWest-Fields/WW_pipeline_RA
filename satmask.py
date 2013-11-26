#! /usr/bin/env python

'''
ABOUT:
satmask.py  This program makes satellite masks.

DEPENDS:
drizzlepac
astropy
numpy
ds9
glob

AUTHOR:
Roberto J. Avila
Sara Ogaz

HISTORY:
October 2013: Original script (v0.1).

FUTURE IMPROVEMENTS:

USE:
python satmask.py

'''

__author__='Roberto J. Avila'
__version__= 0.1 

def make_single_sci(inputim,rootname):

    single_sci_name = rootname+'_single_sci.fits'

    adriz.AstroDrizzle(inputim,
          output = rootname,
          runfile = '',
          context = False,
          num_cores = 1,
          preserve = False,
          static = False,
          skysub = False,
          driz_separate = True,
          median = True,
          median_newmasks = False,
          combine_type = 'median',
          combine_nlow = 0,
          combine_nhigh = 0,
          blot = False,
          driz_cr = False,
          driz_combine = False)

    return single_sci_name


def make_mask(sci,x1,y1,x2,y2,width):


    if x1 == x2:
        vertical = True
    else:
        hwidth = width/2.
        dx = x2-x1
        dy = y2-y1
        m = dy/dx
        b = y1-m*x1
        delta_b = np.absolute(hwidth/math.sin(math.atan(dx/dy)))
        vertical = False
    
    top = sci.shape[0]
    bottom = 0

    for i in np.arange(sci.shape[1]):

        if vertical:
            sci[i-hwdith:i+hwdith,:] = 1
        else:
            upper = int(m*i+(b+delta_b))
            lower = int(m*i+(b-delta_b))
            if (upper>bottom)&(lower<bottom):  #Case 2 
                sci[0:upper,i] = 1       

            elif (upper>top)&(lower<top):  #Case 4
                sci[lower:top,i] = 1

            elif (upper>bottom)&(upper<=top)&(lower>=bottom)&(lower<top): #Case 3
                sci[lower:upper,i] = 1 

            else:
                pass  #Cases 1,5

    return sci


def blot_mask(inputim,rootname):

    adriz.AstroDrizzle(inputim,
          output = rootname,
          runfile = '',
          context = False,
          num_cores = 1,
          preserve = False,
          static = False,
          skysub = False,
          driz_separate = False,
          median = False,
          blot = True, 
          blot_interp = 'nearest',
          blot_addsky = False,
          driz_cr = False,
          driz_combine = False)

def doclean():

    medlist = glob.glob('*med.fits')
    single_masklist = glob.glob('*single_mask.fits')
    single_scilist = glob.glob('*single_sci.fits')
    single_whtlist = glob.glob('*single_wht.fits')

    for medim in medlist:
        os.remove(medim)
    for single_maskim in single_masklist:
        os.remove(single_maskim)
    for single_sciim in single_scilist:
        os.remove(single_sciim)
    for single_whtim in single_whtlist:
        os.remove(single_whtim)



##################################################
# BEGINNING OF MAIN CODE
##################################################

if __name__ == "__main__":

    from drizzlepac import astrodrizzle as adriz
    from astropy.io import fits as pf
    import numpy as np
    import ds9
    import glob
    import math
    import os

#STEP 1: Make list of images to process

    imlist = glob.glob('*fl?.fits')
    #imlist = ['jbp301fnq_flc.fits','ic5n2em9q_flt.fits'] #This line for testing

    display = ds9.ds9('satellitemarker')
    display.set('regions shape line')
    display.set('regions format ds9')

    for im in imlist:
        rootname = im[:-9]

#STEP 2: Make single_sci image

        single_sci_im = make_single_sci(im,rootname)

#STEP 3: Mark single_sci image

        medim = rootname+'_med.fits'    
        hdu = pf.open(medim,mode='update')
        sci = hdu[0].data
        maskok = False

        while maskok == False:

            display.set('frame 1')
            display.set('file '+single_sci_im)
            display.set('zoom to fit')
            display.set('scale log')
            display.set('scale zscale')
            numtrails = int(raw_input('How many trails are in the image? > '))
            if numtrails == 0 : break

            sci[:,:] = 0.
            for i in range(numtrails):
                print 'Trail {}'.format(i+1)
                print 'Mark endpoint 1 of trail'
                p1 = np.float32(display.get('imexam coordinate image').split())
                print 'Mark endpoint 2 of trail'
                p2 = np.float32(display.get('imexam coordinate image').split())
                x1 = p1[0]
                y1 = p1[1]
                x2 = p2[0]
                y2 = p2[1]

                regcommand = 'line({},{},{},{})#width=4'.format(p1[0],p1[1],p2[0],p2[1]) 
                display.set('regions command '+regcommand)
                width = int(raw_input('Enter line width > '))

                sci = make_mask(sci,x1,y1,x2,y2,width)

            hdu.close
            display.set('frame 2')
            display.set('file '+medim)
            display.set('zoom to fit')
            display.set('match frame image')
            isok = raw_input('Is mask ok? >')
            if isok == 'y' : maskok = True
                 
#STEP 4: Blot back mask to original distorted frame 

        blot_mask(im,rootname)
       
#STEP 5: Cleanup

    print 'Cleaning up'
    doclean()

    display.set('exit')
    print 'Finished'
