def doclean():

    scilist = glob.glob('*sci*')
    whtlist = glob.glob('*wht*')
    medlist = glob.glob('*med*')
    for sci in scilist:
        os.remove(sci)
    for wht in whtlist:
        os.remove(wht) 
    for medim in medlist:
        os.remove(medim)

#########################################################
#########################################################

import glob
import os
from drizzlepac import astrodrizzle as adriz


asnlist = glob.glob('*asn.fits')

for asn in asnlist:

    print "workin on "+asn
    adriz.AstroDrizzle(asn,configobj='cr_clean.cfg')
    doclean()
    print "FINISHED ASN: "+ asn

print 'FINISHED ALL'
