from scitools.std import *
from urllib2 import urlopen

#----------------------------------Picking out document number---------------------------

Doc = raw_input('Document number (0-9): ') #input filename
Doc = int(Doc)
Docs = ['0','67','133','200','267','333','400','467','533','600']
WhichDoc = Docs[Doc]

#----------------------------------Importing document----------------------------

url = 'http://folk.uio.no/frodekh/AST1100/lecture6/spectrum_day' + WhichDoc + '.txt'

#--------------Calculating length of columns and creating empty array-----------

length = sum(1 for line in urlopen(url))
data = zeros((length,2))
infile = urlopen(url)

#---------------------Splitting lines and inserting data to data-array---------------

i = 0
for line in infile:
	lambdaObs,Flux = line.split() 
	data[i][0] = float(lambdaObs)           #Assigning values from document to array
	data[i][1] = float(Flux)	  	#------------------""-------------------
	i+=1

#-------------Calculating Fmin and LambCent from data--------------------------------

Fmin = data[length/2.,1]          #Half way mark
Fmax = 1 			  #Always 1 for the starting point on y-axis
LambCent = data[length/2.,0]      #Half way mark
sigma = 0.02   			  #This measurement was done by eye, it is the same for all data

#----------------Defining ranges----------------------------------------------------

Fmins     = linspace(0.80*Fmin, 1.20*Fmin, 40)             #+-20% grid
sigmas    = linspace(0.80*sigma, 1.20*sigma, 40) 	   #+-20% grid
LambCents = linspace(LambCent - 0.10, 0.10 + LambCent, 40)	   

#--------------------Least square method to find best estimate---------------------

Grid = zeros((40**3 , 4)) #40*40*40 Grid for possible values for LambCent, Fmin and sigma
iterations = 0
for Fmin in Fmins:                         #Least square method
	for LambCent in LambCents:
		for sigma in sigmas:
			Fmod = Fmax + (Fmin - Fmax)*e**(-((data[:,0]-LambCent)**2.)/(2.*sigma**2.))
			delta = sum((data[:,1] - Fmod)**2)
			Grid[iterations] = [delta, LambCent, Fmin, sigma]
			iterations += 1

delta_min = argmin(Grid[:,0])		# We get the most accurate estimate with lowest delta
LambCent  = float(Grid[delta_min][1])	# Assigning values from list 
Fmin   	  = float(Grid[delta_min][2])				
sigma 	  = float(Grid[delta_min][3])			

#------------------Calculating best estimate for plot-------------------------------

Fmod = Fmax + (Fmin - Fmax)*e**(-((data[:,0] - LambCent)**2.)/(2.*sigma**2.))

#------------------Printing best values for LambCent, Fmin and sigma ---------------
print '-----------------------------------------------------------------------------'
print 'For the lowest delta we use LambCent = %.3f nm, Fmin = %.3f J/sm**2 and Sigma = %.3f nm' % (LambCent,Fmin,sigma)
print '-----------------------------------------------------------------------------'
#-------------------Plotting estimate and raw data----------------------------------

plot(data[:,0], data[:,1], '-b', data[:,0], Fmod, '-r')
xlabel('Wavelength [nm]')
ylabel('Flux [J/(sm**2)]')
legend('Raw data', 'Estimate')
savefig('spectrum_day' + WhichDoc + 'plot.png')
show()

