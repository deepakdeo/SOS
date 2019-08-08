#==========================================================================================#
#                         Script to make source model image                 
#==========================================================================================#
'''
# Developed by Ruta Kale (NCRA-TIFR) and her student Deepak Deo .
# Start: Feb 4, 2016, Last update: Mar 27, 2017
 
# We assume analysis utilities have been already installed in your casa
	if not, follow https://casaguides.nrao.edu/index.php?title=Analysis_Utilities .
# Check the inputs section before running the code.
# Make sure you have the model image/s before running this script. 
'''
#==========================================================================================#

from math import *      # needed for carrying out mathematical expressions
import random           # for generating random numbers

#======================
# Give inputs below	 
#======================

z = [0.05, 0.1, 0.13, 0.15, 0.17, 0.2 , 0.3, 0.4, 0.5, 0.6, 0.8, 0.9, 1.0] # z is redshift at which images are to be made 

entry1 = 1               # to store the print outputs in a text file, use 1 for extended source(E), 2 for point(P) and 3 for extended and point source (EnP)

entry2 = 1              # specify naming of source image based on image type, give 1 for E, 2 for P and 3 for EnP
name_img = 'modelimg'   # partial name of model source image

entry3 = 1              # specify source image type, 1 for E, 2 for P, 3 for EnP

L = 0.5                   # in Mpc, Linear size of source
F1= 0.6                 # in Jy, we take an expected flux density at initial z and calculate the later ones using it
refRA = [4,0,0.]        # 04h00m00.0s, reference RA for imagecenter
refDEC = [-20,0,0.]      # +10d00m00.0s, refernce DEC
ref_freq = '9.2GHz'   # frequency at which image is to be made
cellsiz = '0.01arcsec'     # cellsize -> size of each pixel in the image
imsiz = 7200            # Image size in units of cellsize, taken bigger than primary beam of GMRT at observed frequency
start = 12	        # setting the starting range for making the model image. 0 => image corresponding to z[0]
end = 13		        # setting the end range

#-----------fixed values, need not be touched--------------------
c = 299792.458 # velocity of light in km/s
H = 67.8; w = 0.308 # Hubble constant (in km/s/Mpc)and matter density parameter from Planck 2015 results (http://arxiv.org/pdf/1502.01589.pdf).. (following lamda-CDM (Cold Dark Matter) cosmology)
#-----------------------------------------------------------------

#================== END Inputs, below no changes required =================


# opening a logbook to store printed values
def logbk(entry1):
	if entry1 == 1:
		lb=open('logbookE.txt','w')
	elif entry1 == 2:
		lb=open('logbookP.txt','w')
	elif entry1 == 3:
		lb=open('logbookEnP.txt','w')
	return lb

lb = logbk(entry1)

print >> lb, 'redshift taken:\n', z   # printing redshift in the logbook

#==============================================
# obtaining values of angular diameter distance
#==============================================

angDiaDist = []

for x in z:
	aDD = (c*2*(w*x+(w-2)*(sqrt(1+w*x)-1)))/(H*(w*(1+x))**2)  # expression taken from the book 'extragalactic astronomy and cosmology by P. Schneider - section 4.3.3' 
	angDiaDist.append(aDD)
print >> lb, '\nvalues of angular diameter distance in Mpc:\n', angDiaDist


#=======================================================================================================
# obtaining values of angular diameter in arcmin i.e angular size of radio halos here (extended sources)
# angular diameter(theta)=(Linear size (L)/angular diameter distance (angDiaDist)) in radians
#=======================================================================================================

theta1, theta2, theta3 = [], [], [] #thetas in arcmin, different size of thetas at a partcular L varying with z

for x in angDiaDist:
	theta = (3437.75*L)/x # in arcmin, 1radian = 3437.75 arcmin
	theta1.append(theta)
	theta2.append(theta/2.0) #theta with different starting value, varying with z
	theta3.append(theta/3.0)
print >> lb, '\nvalues of theta1 in arcmin:\n', theta1
print >> lb, '\nvalues of theta2 in arcmin:\n', theta2
print >> lb, '\nvalues of theta3 in arcmin:\n', theta3


#======================================================================
# obtaining the values of total flux density of the radio halos w.r.t z
#======================================================================

myflux1, myflux2, myflux3 = [], [], [] # total flux density in Jy

for x in range(0,len(z)):
	fd = F1*((1+z[0])/(1+z[x]))**4*(angDiaDist[0]/angDiaDist[x])**2
	myflux1.append(fd)
	myflux2.append(2.0*fd)
	myflux3.append(3.0*fd)
print >> lb, '\nvalues of flux1 in Jy:\n', myflux1 # corresponding to theta1
print >> lb, '\nvalues of flux2 in Jy:\n', myflux2
print >> lb, '\nvalues of flux3 in Jy:\n', myflux3

#=====================================================
# Generalizing RA and DEC i.e, position of the sources
#=====================================================

RA_s = str(refRA[0])+'h'+str(refRA[1])+'m'+str(refRA[2])+'s' # reference RA in strings
DEC_s = str(refDEC[0])+'d'+str(refDEC[1])+'m'+str(refDEC[2])+'s' # reference DEC in strings

refpos = 'J2000 '+RA_s+' '+DEC_s # reference position in Julian coordinate system

print >> lb, '\nreference position: ', refpos

refRA_as = 15.*60.*60.*refRA[0]+60.*refRA[1]+refRA[2] # converting refRA in arcsec to use it further, 1sec=15arcsec
print >> lb, '\nReference RA in arcsec: ', refRA_as # refernece RA in arcsec

def decref(refDEC): # returns reference DEC in arcsec
	if refDEC[0] < 0.0:	# if 1st entry of the list refDEC<0
		refDEC_as=60.*60.*refDEC[0]-60.*refDEC[1]-refDEC[2]
	else:
		refDEC_as=60.*60.*refDEC[0]+60.*refDEC[1]+refDEC[2]
	return refDEC_as # reference DEC in arcsec
print >> lb, '\nReference DEC in arcsec: ', decref(refDEC)


#********** following lines not required if point sources not needed **********#
#=====================================================
# following codes are for incorporating point sources
#=====================================================

#------------------
# we want most of the point sources within the halo. From above calculations size of largest halo at nearest z is 16.79 (~16) arcmin, i.e from reference position max deltaRA would be 32 sec and deltaDEC would be 8 arcmin (480 arcsec)
# 1 sec = 15 arcsec
# for an isosceles right triangle sqrt(2(x**2))=32 sec => x=22.624 sec ~ 22 sec=330 arcsec
# therefore to keep the point sources within the halo choose dRA and dDEC(in sec) such that their sum is less than 2*x i.e, 44sec

dRA=[] # delta RA
dDEC=[] # delta DEC

#******--------------------------*****
# if random values of dRA n dDEC is not needed in every run, comment next 4 lines (i.e don't run the following for loop)
# and give the list of dRA and dDEC manually.
#******--------------------------*****

for x in xrange(5):
	r = random.randrange(1,47) # to have 'possibility' of some source even outside the halo, take 44 if wanted only inside
	dRA.append(r) # $$$$$ everytime the code is run, a different random set of RA n DEC will be made $$$$$
	dDEC.append(15.0*(47.0-dRA[x])) # take 44 instead of 47 (0r > 44) if wanted only inside, in arcsec (1sec=15arcsec)

print >> lb, '\ndelta RA:\n', dRA    
print >> lb, '\ndelta DEC:\n', dDEC

posn1 = [(a,b) for a, b in zip(dRA,dDEC)] # positions in all the four quadrants having 'refpos' as the origin
posn2 = [(a,-b) for a, b in zip(dRA,dDEC)]
posn3 = [(-a,-b) for a, b in zip(dRA,dDEC)]
posn4 = [(-a,b) for a, b in zip(dRA,dDEC)]
posns = posn1+posn2+posn3+posn4 # concatenating all lists into a single list, it is actually a list of tupules

print >> lb, '\nall positions from reference position:\n', posns

def RA(refRA_as): # it takes entry as RA in arcsec and returns RA in strings like 04h04m04.04s
	RAhr=refRA_as/3600.0/15.0
	hrs=int(RAhr)
	t1=60.*(RAhr-hrs) # t1 = temporary value 1
	mnts=int(t1)
	sec_float=60.*(t1-mnts)
	sec=float("{0:.2f}".format(sec_float))
	return str(hrs)+'h'+str(mnts)+'m'+str(sec)+'s'

ra=[] # list of all RA w.r.t refRA in string
for x in range(0,len(posns)):
	t2=RA(posns[x][0]*15+refRA_as) # taking 1st value(i.e RA) of each tupule, multiplying it by 15 (1sec=15arcsec) and +refRA_as 
	ra.append(t2)
print >> lb, '\nRight Ascension:\n', ra

def DEC(decref): # it takes entry as DEC in arcsec and returns DEC in strings like +/- 60d40m40.04s
	DECdeg=decref/(3600.0)
	if DECdeg<0.0:
		deg=int(abs(DECdeg))
		t3=60.*(DECdeg+deg)
		arcmin=int(abs(t3))
		arcsec_float=abs(60.*(t3+arcmin))
		arcsec=float("{0:.2f}".format(arcsec_float))
		return str(-deg)+'d'+str(arcmin)+'m'+str(arcsec)+'s'
	else:
		deg=int(DECdeg)
		t3=60.*(DECdeg-deg)
		arcmin=int(t3)
		arcsec_float=60.*(t3-arcmin)
		arcsec=float("{0:.2f}".format(arcsec_float))
		return '+'+str(deg)+'d'+str(arcmin)+'m'+str(arcsec)+'s'

dec=[] # list of all DEC w.r.t refDEC in string
for x in range(0,len(posns)):
	t4=DEC(posns[x][1]+decref(refDEC))
	dec.append(t4)
print >> lb, '\nDeclination:\n', dec

posnJ=['J2000 '+str(a)+' '+str(b) for a,b in zip(ra,dec)] # positions in Julian coordinate
print >> lb, '\nPosition of sources:\n', posnJ

coords=random.sample(posnJ,5) # chooses 5 positions randomly from posnJ
print >> lb, '\ncoordinates of the point sources\:n', coords

#------------------------
# if don't want random selection for each run, then comment above two lines and uncomment following two lines
#------------------------

#coords=posnJ[0::6] # starting from 0th element to the last with step=6
#print >> lb, '\nevery 6th element from 0th in above source position list:\n', coords

#*********=========== End of point sources definition==========***********#
#************* Ignore above codes if point sources not required ************#


#=============================
# defining the name of images
#=============================

outim =[]

def imgnm(e2):
	if e2 == 1:
		for i in range(0,len(z)):
			outim.append(name_img+"E_"+str(z[i])) #list of output images, one for each z
		print >> lb, '\nname of the images:\n', outim
	elif e2 == 2:
		for i in range(0,len(z)):
			outim.append(name_img+"P_"+str(z[i])) #list of output images, one for each z
		print >> lb, '\nname of the images:\n', outim	
	elif e2 == 3:
		for i in range(0,len(z)):
			outim.append(name_img+"EnP_"+str(z[i])) #list of output images, one for each z
		print >> lb, '\nname of the images:\n', outim
imgnm(entry2)

lb.close() # closing the logbook

#=======================================================	
# characterizing the image layout and source properties
#=======================================================

def mkmodelsky(outimgname,flux1,flux2,flux3,theta1,theta2,theta3,coords,refpos,entry2,frequency,cellsiz,imsiz,RA_s,DEC_s):
	cl.done() # removes previous component before going into the next loop, comment it if addition of previous flux required in next one
	
	# specifying source properties
	if entry3 == 1:
		# defining model halo (extended source)
		cl.addcomponent(dir=str(refpos), flux=flux1, fluxunit='Jy', freq=frequency, shape="Gaussian", majoraxis=str(theta1)+'arcmin', minoraxis=str(theta1)+'arcmin', positionangle='45.0deg') # spectrumtype='spectral index', index=-1.6)
		#cl.addcomponent(dir=str(refpos), flux=flux2, fluxunit='Jy', freq='0.610GHz', shape="Gaussian", majoraxis=str(theta2)+'arcmin', minoraxis=str(theta2)+'arcmin', positionangle='45.0deg')
		#cl.addcomponent(dir=str(refpos), flux=flux3, fluxunit='Jy', freq='0.610GHz', shape="Gaussian", majoraxis=str(theta3)+'arcmin', minoraxis=str(theta3)+'arcmin', positionangle='45.0deg')

	elif entry3 == 2:
		# defining point sources
		for i in range(0,len(coords)):
			cl.addcomponent(dir=str(coords[i]), flux=0.1+0.1*float(i), fluxunit='Jy', freq=frequency, shape="Gaussian", majoraxis=str(3.0)+'arcsec', minoraxis=str(3.0)+'arcsec', positionangle='45.0deg')

	elif entry3 == 3:
		# defining extended and point sources both
		cl.addcomponent(dir=str(refpos), flux=flux1, fluxunit='Jy', freq=frequency, shape="Gaussian", majoraxis=str(theta1)+'arcmin', minoraxis=str(theta1)+'arcmin', positionangle='45.0deg')
		cl.addcomponent(dir=str(refpos), flux=flux2, fluxunit='Jy', freq=frequency, shape="Gaussian", majoraxis=str(theta2)+'arcmin', minoraxis=str(theta2)+'arcmin', positionangle='45.0deg')
		cl.addcomponent(dir=str(refpos), flux=flux3, fluxunit='Jy', freq=frequency, shape="Gaussian", majoraxis=str(theta3)+'arcmin', minoraxis=str(theta3)+'arcmin', positionangle='45.0deg')
		for i in range(0,len(coords)):
			cl.addcomponent(dir=str(coords[i]), flux=0.1+0.1*float(i), fluxunit='Jy', freq=frequency, shape="Gaussian", majoraxis=str(3.0)+'arcsec', minoraxis=str(3.0)+'arcsec', positionangle='45.0deg')

	# specifying the layout of the image, check CASA toolkit reference manual for explanation of following codes
	ia.fromshape(str(outimgname)+".im",[imsiz,imsiz,1,1],overwrite=True) # 
	cs=ia.coordsys()
	cs.setunits(['rad','rad','','GHz'])
	cell_rad=qa.convert(qa.quantity(cellsiz),"rad")['value']
	cs.setincrement([-cell_rad,cell_rad],'direction')
	cs.setreferencevalue([qa.convert(RA_s,'rad')['value'],qa.convert(DEC_s,'rad')['value']],type="direction")
	cs.setreferencevalue(frequency,'spectral')
	cs.setrestfrequency(value=qa.quantity(frequency,'GHz'))
	cs.setincrement('0.5GHz','spectral')# earlier 0.001 GHz, for ska take 0.5GHz
	ia.setcoordsys(cs.torecord())
	ia.setbrightnessunit("Jy/pixel")
	ia.modify(cl.torecord(),subtract=False)
	ia.done()
	#exportfits(imagename=str(outimgname)+".im",fitsimage=str(outimgname)+".fits",overwrite=True) # uncomment if fits img wanted

#======================================
# using the above function to create the image
#======================================

for i in range(start,end):
	mkmodelsky(outim[i],myflux1[i],myflux2[i],myflux3[i],theta1[i],theta2[i],theta3[i],coords,refpos,entry2,ref_freq,cellsiz,imsiz,RA_s,DEC_s)
	print '\nImage made...%s' %(outim[i])
print 'Check images on Viewer.'

