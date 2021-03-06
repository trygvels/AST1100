from scitools.std import *
from urllib2 import urlopen

#------------------------------------Defining constants---------------------------

Doc = raw_input('Document number: ') #input filename
Masses = [0.8, 2.8, 0.5, 0.5, 1.8, 0.7, 1.6, 2.1, 7, 8]
M = Masses[int(Doc)]

c= 3*10**8
G= 6.67*10**(-11)
sun_M = 1.988*10**30

#----------------------------------Importing document----------------------------

url = 'http://folk.uio.no/frodekh/AST1100/lecture3/star' + Doc +'.txt'

#--------------Calculating length of columns and creating empty array-----------

length = sum(1 for line in urlopen(url))
data = zeros((length,4))
infile = urlopen(url)

#---------------------Splitting lines and inserting data to array---------------

i = 0
for line in infile:
	t, lambdaObs, flux = line.split() 
	data[i][0] = float(t)             #Assigning values from document to array
	data[i][1] = float(lambdaObs)	  #------------------""-------------------
	data[i][2] = float(flux)
	i += 1

#plot(data[:,0],data[:,2])  #Flux plot for checking by-eye if extrasolar planet exists
#title('Flux')
data[:,3] = c*(data[:,1] - 656.3)/656.3 #Calculating radial velocity with doppler formula

#--------------Calculating peculiar velocity and subtracting from radial---------

v_pec = sum(data[:,3])/len(data[:,3])
data[:,3] = data[:,3] - v_pec

#-------------Calculating max points for V_rad and the corresponding t-----------

vr_max = max(data[:,3])                  #Max point data[:,2]
vr_min = min(data[:,3])                  #Min point data[:,2]
#position of vr_max in data[:,2]
x_max = int(where(data[:,3]==vr_max)[0]) 
x_min = int(where(data[:,3]==vr_min)[0]) #position of vr_min in data[:,2]
t_0 = data[x_max,0]                      #time at vr_max

#Finding period
n = length/2
flux_min =min(data[:n,2]) #finding minimum flux in first half of flux-time plot
flux_min1=min(data[n:,2]) #finding minimum flux in second half of flux-time plot
xf_min= int(where(data[:,2]==flux_min)[0]) #which point is flux_min in data[:,2]
xf1_min = int(where(data[:,2]==flux_min1)[0])
P = abs(data[xf_min,0]-data[xf1_min,0])  #Period, measured between drops in flux

#----------------Defining range of max V_rad, corresponding t and Period--------

t_0 = linspace(0.90*t_0, 1.10*t_0, 20)     #+-10% grid
vr_max = linspace(0.80*vr_max, vr_max, 20) #Using max value, so no value above this
P = linspace(0.90*P, 1.10*P, 20)	   #+-10% grid

#--------------------Least square method to find best estimate----------------

Grid = zeros((20**3 , 4))
iterations = 0
for i in t_0:
	for j in vr_max:
		for k in P:
			vr_mod = j*cos(2*pi*(data[:,0] - i)/k)
			sum_ = sum((data[:,3] - vr_mod)**2)
			Grid[iterations] = [sum_, i, j, k]
			iterations += 1

n     = argmin(Grid[:,0])			# Most accurate estimate with lowest sum_
print n
t_0   = Grid[n][1]				# Assigning values from list 
v_rad = Grid[n][2]				# ----------""-------------
P     = Grid[n][3]				# ----------""-------------
v_est = v_rad*cos(2*pi*(data[:,0] - t_0)/P)

#------------------Calculating mass of the planet-----------------------

Mass_Planet = (M*sun_M)**(2./3)*v_rad*P**(1./3)/((2*pi*G)**(1./3))
print '------------------------------------------------------------------------------'
print 'The mass of the planet orbiting the star is: %.e kg' % Mass_Planet
print 'If estimate is clearly not matching raw data, discard this value and conclude:'
print 'There is no extrasolar planet.'
print '------------------------------------------------------------------------------'

#-------------------Plotting estimate and raw data----------------------

plot(data[:,0], data[:,3], '-b', data[:,0], v_est, '-r')
legend('Raw data', 'Estimate')
title('Velocity for extrasolar planet with estimate')
savefig('star'+Doc+'plot.png')
show()

"""
[trygvels@vor Ast1100 Obliger]$ python Oblig2.py
Document number: 3
------------------------------------------------------------------------------
The mass of the planet orbiting the star is: 6e+27 kg
If estimate is clearly not matching raw data, discard this value and conclude:
There is no extrasolar planet.
------------------------------------------------------------------------------
Could not find/open font when opening font "arial", using internal non-scalable font
Could not find/open font when opening font "arial", using internal non-scalable font
"""

