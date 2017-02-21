from scitools.all import *

#Defining constants
N      = 1000
dt     = 0.01
Vshell = 0.993
Gshell = 1/sqrt(1-Vshell**2)
theta  = 167.*pi/180
rm     = 20.
Lm     =  38.
Em     =  8.03

#Creating empty arrays
r    = zeros(N, float)
phi  = zeros(N, float)
r[0] = rm

#Calculating positions in polar coordinates
for i in range(N):
	if abs(r[i]) < 2:
		n = i
		break
	dr      =  -sqrt(Em**2 - (1 + (Lm/abs(r[i]))**2)*(1 - 2./abs(r[i])))*dt
	dphi    =  (Lm/r[i]**2)*dt
	r[i+1]  =  r[i] + dr
	phi[i+1]=  phi[i] + dphi

#Creating the event horizon for the plot
rS   = zeros(100, float)
rS  += 2
phiS = linspace(0,2*pi,100)

#Converting to cartesian coordinates
xS = rS*cos(phiS)
yS = rS*sin(phiS)
x  = r*cos(phi)
y  = r*sin(phi)

#Plotting rocket and event horizon
plot(x[:n], y[:n], 'ob', xS, yS, '-r')
legend('Rocket trajectory', 'Event Horizon')
title('Rocket flying towards a black hole')
axis([-2.5,20,-7,7])
savefig('Oblig9.png')

finalphi = phi[n]*180/pi
print 'Final angular coordinate: %.2f degrees' %finalphi
