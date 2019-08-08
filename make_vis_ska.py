#==========================================================================================#
#                         Script to simulate visbility (CASA MS)                 
#==========================================================================================#
'''
# Developed by Ruta Kale (NCRA-TIFR) and her student Deepak Deo .
# Start: Mar 4, 2016, Last update: Apl 12, 2017
 
# We assume analysis utilities have been already installed in your casa
	if not, follow https://casaguides.nrao.edu/index.php?title=Analysis_Utilities .
# Check the inputs section before running the code.
# Make sure you have the model image/s before running this script. 
'''
#==========================================================================================#

import numpy as np
from math import *
import sys
import os
import re
from simutil import simutil

#======================
# Give inputs below	 
#======================

z = [0.05, 0.1, 0.13, 0.15, 0.17, 0.2 , 0.3, 0.4, 0.5, 0.6, 0.8, 0.9, 1.0] # z is redshift at which images are to be made 

# selecting reference image and naming visibility corresponding to it
entry1 = 1             # give 1 for extended source, 2 for point and 3 for extended and point source
name_img = 'modelimg'  # partial name of reference image
entry2 = 1             # give 1 for extended source(E), 2 for point(P) and 3 for extended and point source(EnP)
name_vis = 'modelvis'  # partial name of model visibility

cfgfile = 'ska_mid133.cfg'   # telescope configuration files are in your casa-release-..../data/alma/simmos/
alpha = -1.6           # spectral index
chan = 1               # no. of channels
delta_f = 50.0        # resolution of each channel in MHz
int_time = '1s'       # integration time

RT = '56839.0d' # 2014/06/30/22:33:42', rise time(yyyy/mm/dd/hh:mm:ss) of source in UTC, convert the local rise time of source in UTC, CASA prompt: me.epoch('UTC','2014/06/30/22:33:42') = 56838.94006944444d
nscans = 1             # no. of scans
ST = 1.0               # ST = Start Time of first scan in seconds
dT = 900.0	       # each scan duration in seconds
sg = 0.0               # scan gap: time gap between two consecutive scans in seconds

start = 12	       # setting the starting range for visibility function
end = 13	               # setting the end range

#path = '/home/deepak/CASA/casa-release-4.5.1-el6/lib/python2.7/simutil.py' # path of simutil.py, it is in your casa install folder
#util=simutil()

#================== END Inputs, below no changes required =================


#===========================================================
# specifying reference image and corresponding visibilities
#===========================================================

imageref=[] # list of reference images from which visibility is to be made
def imgref(e1):	
	if e1 == 1:
		for x in range(0,len(z)):
			imageref.append(name_img+"E_"+str(z[x])+".im")
			#imageref.append("modelskyE_"+str(z[x])+"_scaled350.im")
	elif e1 == 2:
		for x in range(0,len(z)):
			imageref.append(name_img+"P_"+str(z[x])+".im")
	elif e1 == 3:
		for x in range(0,len(z)):
			imageref.append(name_img+"EnP_"+str(z[x])+".im")

imgref(entry1)

myvis =[]  # name of visibilities to the corresponding reference images
def visib(e2):
	if e2 == 1:
		for x in range(0,len(z)):
			myvis.append(name_vis+"E_"+str(z[x])+".ms") 
	elif e2 == 2:
		for x in range(0,len(z)):
			myvis.append(name_vis+"P_"+str(z[x]+".ms")) 
	elif e2 == 3:
		for x in range(0,len(z)):
			myvis.append(name_vis+"EnP_"+str(z[x])+".ms") 

visib(entry2)


#=====================================================
# scaling flux density of image, follows power law
#=====================================================

def sclimg(imageref,fratio,fvalue,fvalue2):
	imagein = imageref
	ia.open(imagein) # opens the input image
	#temp=imhead(imagename=imagein, mode='get', hdkey='crval4')
	#print 'opening image at...', temp, 'for scaling pixel at..', str(fvalue2)+'GHz'

	beam=ia.getchunk() # gets all the pixel details from the opened image
	myflag=0
	if fratio > 1 and fvalue2 > fvalue or fratio < 1 and fvalue2 < fvalue:
		myflag=1
	if fratio > 1 and fvalue2 < fvalue or fratio < 1 and fvalue2 > fvalue:
		myflag=2

	if myflag==1:
		beam=(1.0/fratio)*beam # scaling each pixel value by the spectral index, power law
	if myflag==2:		
		beam=fratio*beam
		
	ia.putchunk(beam) # putting back new pixel details in the image	
	ia.done()
	#ia.close()
	imhead(imagename = imagein, mode = 'put', hdkey = 'restfreq', hdvalue = str(fvalue2)+'GHz') # setting the rest freq
	imhead(imagename = imagein, mode = 'put', hdkey = 'crval4', hdvalue = str(fvalue2)+'GHz') # setting the centralfreq
	#imhead(imagename = imagein, mode = 'put', hdkey = 'cdelt4', hdvalue = '0.001GHz') # setting the freq increment
	flux=imstat(imagename = imagein)
	print 'Total flux density at', fvalue2, '=', flux['sum'], 'Jy'
	return imagein
	#os.system('cp -r '+imagein+' '+imagein+str(fvalue2[v])) # uncomment if output image required


#================================================
# RA and DEC conversion: arcsec to standard form
#================================================

def RAs(ra_value): # it takes entry as RA in arcsec and returns RA in strings like 04h04m04.04s
		RAhr=ra_value/3600.0/15.0
		hrs=int(RAhr)
		t1=60.*(RAhr-hrs) # t1 = temporary value 1
		mnts=int(t1)
		sec_float=60.*(t1-mnts)
		sec=float("{0:.2f}".format(sec_float))
		return str(hrs)+'h'+str(mnts)+'m'+str(sec)+'s'

def DECl(dec_value): # it takes entry as DEC in arcsec and returns DEC in strings like +/- 60d40m40.04s
		DECdeg=dec_value/(3600.0)
		if DECdeg<0.0:
			deg=int(abs(DECdeg))
			t2=60.*(DECdeg+deg)
			arcmin=int(abs(t2))
			arcsec_float=abs(60.*(t2+arcmin))
			arcsec=float("{0:.2f}".format(arcsec_float))
			return str(-deg)+'d'+str(arcmin)+'m'+str(arcsec)+'s'
		else:
			deg=int(DECdeg)
			t2=60.*(DECdeg-deg)
			arcmin=int(t2)
			arcsec_float=60.*(t2-arcmin)
			arcsec=float("{0:.2f}".format(arcsec_float))
			return '+'+str(deg)+'d'+str(arcmin)+'m'+str(arcsec)+'s'


#===================================
# Function to simulate visibility 
#===================================

def visibility(cfgfile,myvis,imageref,alpha,chan,delta_f,int_time,RT,nscans,ST,dT,sg):
	
	col=simutil().readantenna(antab=cfgfile)
	xx=col[0]           # X coordinate of the antenna position
	yy=col[1]	    # Y coordinate of the antenna position	
	zz=col[2]	    # Z coordinate of the antenna position
	diam=col[3]	    # diameter of the antenna
	antnames=col[4]	    # name of the antenna
	telescope=col[6]    # name of observatory

	mounttype = 'alt-az'
	if telescope in ['DRAO', 'WSRT']:  # Add ASKAP here if it also has equatorial mount
		mounttype = 'EQUATORIAL'
	coordsys='global'                  # CASA suggests taking global for all .cfg files

	# prerequisite for function sclimg()
	frequency = imhead(imagename=imageref, mode ='get', hdkey='crval4')
	funit = frequency['unit']
	fvalue=frequency['value']

	#print 'Reference image is at', frequency['value'], funit
	
	if funit == 'Hz':
		fvalue = fvalue*(10**(-9)) # Hz to GHz
		print 'fvalue in GHz=', fvalue
	if funit == 'MHz':
		fvalue = fvalue*(10**(-3)) # MHz to GHz
		print 'fvalue in GHz=', fvalue

	fvalue2=[] # list of the frquencies corresponding to each channel
	for i in range(0,chan):
		fvalue2.append(fvalue + (i)*delta_f)
	
	fvalue3=[fvalue]
	for i in range(0,chan-1):
		fvalue3.append(fvalue + (i)*delta_f)
	
	fratio=[] # ratio of scaling frequency to original frequency with spectral index as power
	for i in range(0,chan):
		fratio.append((fvalue3[i]/fvalue2[i])**alpha)
	

	# finding source direction or phasecenter of the image
	ra= imhead(imagename= imageref, mode='get', hdkey='crval1')
	ra_value = ra['value']*206264.81   # in arcsec
	dec= imhead(imagename= imageref, mode='get', hdkey='crval2')
	dec_value = dec['value']*206264.81 # in arcsec

	# ra dec conversion	
	RA= RAs(ra_value)	
	DEC = DECl(dec_value)

	if telescope == 'SKA_Mid':
		telescope = telescope.replace(telescope,'MeerKAT') # SKA_Mid is recognized by MeerKAT location (April 2017)

	# visibility simulation syntax
	sm.open(myvis) # open a new file

	posant = me.observatory(telescope) # location of telescope read from CASA
	sm.setconfig(telescopename=telescope, x=xx, y=yy, z=zz, dishdiameter=diam,  
        	     mount=mounttype, antname=antnames,  
                     coordsystem=coordsys, referencelocation=posant)

	sm.setspwindow(spwname=telescope, freq=str(fvalue)+'GHz', deltafreq=str(delta_f)+'GHz', 
			freqresolution=str(delta_f)+'GHz', nchannels=chan, stokes='RR LL')
	
	# Set autocorrelation weight
	sm.setauto(0.0)
	sm.setfield(sourcename='MODEL',sourcedirection=['J2000',RA,DEC]) # source direction is taken as pointing center from image file

	# define the feed
	sm.setfeed(mode='perfect R L',pol=[''])
	sm.setlimits(shadowlimit=0.001, elevationlimit='17.0deg') 

	sm.settimes(integrationtime=int_time, usehourangle=True, referencetime=me.epoch('UTC',RT)) # source rise time(in IST) on 2014/07/01 from GMRT location is 04:03:42 which when converted to UTC(IST-5:30:00) becomes 2014/06/30/22:33:42

	for i in range(0,nscans):
		ET = ST+dT-1
		sm.observe(sourcename='MODEL',spwname=telescope, starttime=str(ST)+'s', stoptime=str(ET)+'s')
		ST = ET+sg+1
	
	# if you use usehourangle=True, you can't control starttime
	# On CASA prompt running me.epoch('utc','2014/07/02/00:00:00.1') will give 56840.00000115741d (-> MJD: Mean Julian Day)
	
	sm.setdata(fieldid=0);

	noise = '0.0Jy'      # add some noise. Use '0.0Jy' if no noise wanted
	#sm.setnoise(mode='simplenoise', simplenoise=noise)
	#sm.corrupt();

	for v in range(0,chan):
		inp_img = sclimg(imageref,fratio[v],fvalue,fvalue2[v])
		sm.predict(imagename=inp_img,incremental=True)

	sm.close()
#==================================================================

#====================================
# Execution of visibility function
#====================================

for i in range(start,end):
	visibility(cfgfile,myvis[i],imageref[i],alpha,chan,delta_f,int_time,RT,nscans,ST,dT,sg)
	print 'Successfully made new measurement set named.... %s' %(myvis[i])

