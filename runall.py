import DoEmail as email
from time import gmtime, strftime

t1 =  strftime("%Y-%m-%d %H:%M:%S", gmtime())

import make_cr_clean
import make_catalogs
import tweak_images
import hudf_drizzling

t2 =  strftime("%Y-%m-%d %H:%M:%S", gmtime())


fromaddr = 'avila@stsci.edu'
toaddr = ['robertojavila@gmail.com']
tosub = 'HUDF'
body = 'HUDF\nStarted: {}\nFinished: {}'.format(t1,t2)

email.SendEmail(fromaddr,toaddr,tosub,body)
