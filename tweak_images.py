from drizzlepac import tweakreg as tweak
from stsci.tools import teal
import numpy as np
import glob

filelist = 'catfile.list'

imlist = np.loadtxt(filelist,usecols=(0,),dtype=str)
np.savetxt('tweaklist',zip(imlist),fmt='%s')
print imlist

teal.unlearn('tweakreg')
tweak.TweakReg('@tweaklist',configobj='tweak_images.cfg')

print 'Finished'

