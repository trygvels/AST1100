from scitools.std import *
from urllib2 import urlopen

url = 'http://folk.uio.no/frodekh/AST1100/lecture5/galaxies.txt'

length = sum(1 for line in urlopen(url))     #Length of one column
data = zeros((length,5))                     #Creating empty data array
infile = urlopen(url)                        #Fetching file


c= 3*10**8               #Speed of light	
G= 6.67*10**(-11)	 #Gravitational constant
lambda0 = .212 # 21.2cm

i = 0
for line in infile: 
	Xang, Yang, dist, lambObs= line.split() 
	data[i][0] = float(Xang)             # Assigning values from document to array
	data[i][1] = float(Yang)	  	
	data[i][2] = float(dist)
	data[i][3] = float(lambObs)	
	i += 1

v_gal = c*(data[:,3] - lambda0)/lambda0 # v_gal from doppler effect
v_clus = sum(v_gal)/length              # v_clus peculiar
v_rel = v_gal - v_clus                  # v_rel


#------------------------Oppgave B----------------------------------
plot(data[:,0],data[:,1],'o')                #Plotting position of galaxies with o's
title('Cluster as seen from telescope')
xlabel('x-axis [arcminutes]')
ylabel('y-axis [arcminutes]')
savefig('ClusterFromTelescope.png')
#------------------------Oppgave A----------------------------------
print '-----------------------------------------------------------------'
print 'The radial velocity of the cluster with respect to us is %.2e m/s.' % v_clus

#------------------------Oppgave C------------------------------------
Cfactor = 3437.74677078               # Conversion factor from Arcmin to radians
Mpc = 3.08567758*10**22               # 1 MegaParsec in meters 
data[:,0] = data[:,0]/Cfactor         # x in rad
data[:,1] = data[:,1]/Cfactor         # y in rad
data[:,2] = data[:,2]*Mpc             # dist in meters

x = sin(data[:,0])*data[:,2]          # x-coordinate from trigonometry
y = sin(data[:,1])*data[:,2]          # y-coordinate from trigonometry
z = data[:,2] - sum(data[:,2])/length # z-coordinate as distance array

#m =(vi**2)/(G*1/rij)
mNumerator = sum(v_rel**2)           # Calculating the numerator of the equation from problem 3
mDenominator = 0.0	             # defining the empty sum of the denominator

for i in xrange(length-1):           # j>i so last galaxy is not included
	for j in xrange(i+1,length): # starting at i+1, never getting i=j, i<j<length
		mDenominator += 1./linalg.norm(array([x[i],y[i],z[i]]) - array([x[j],y[j],z[j]]))
				#This is equal to the sqrt expression of 1/rij

mass = mNumerator/(G*mDenominator)

print 'Estimate of total mass of a galaxy in the cluster = %.2e kg.' % mass
print 'For an estimate of a galaxy with 200 million stars with the mass of the sun'
print 'we expect a luminous mass of 4e43 kg, we have more than double that, which means'
print 'that half of the galaxy contains "dark matter".' 



"""
python oblig7.py
Could not find/open font when opening font "arial", using internal non-scalable font
Could not find/open font when opening font "arial", using internal non-scalable font
-----------------------------------------------------------------
The radial velocity of the cluster with respect to us is 1.24e+06 m/s.
Estimate of total mass of a galaxy in the cluster = 8.71e+41 kg.
For an estimate of a galaxy with 200 million stars with the mass of the sun
we expect a luminous mass of 4e43 kg, we have more than double that, which means
that half of the galaxy contains "dark matter".
"""
