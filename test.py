# 1.py
from numpy import asarray, linspace, cos, zeros, ones, sum, pi, argmin,\
average, amax, amin, absolute
from urllib2 import urlopen

# 1.py
from numpy import asarray, linspace, cos, zeros, ones, sum, pi, argmin, average, amax, amin, absolute
from urllib2 import urlopen
from matplotlib import rc
import matplotlib.pyplot as plt
# import raw data

url = 'http://folk.uio.no/frodekh/AST1100/lecture3/star4.txt'
infile = urlopen(url)
# set star mass, estimate t_0 and P by browsing raw data
M = 1.8
t_t = 5.18e5
P_t = 1.0365e6
# set constants
solarmass = 1.9891e30
c = 299792458
G = 6.67384e-11
# compute data size and reset url pointer
length = sum(asarray([1 for _ in infile]))
data = zeros((length,4))
infile = urlopen(url)
# parse data
i = 0
for line in infile:
    t, lambd, I = line.split()
    data[i][0] = float(t)
    data[i][1] = float(lambd)
    data[i][2] = float(I)
    i += 1
# transform variable lambda to variable radial velocity from raw data
data[:,3] = c*(data[:,1] - 656.3*ones(length))*(656.3)**(-1)
# compute peculiar velocity and correct precomputed velocity data
v_pec = average(data[:,3])
data[:,3] = data[:,3] - v_pec*ones(length)
# estimate v_r from raw data
i_t = argmin(absolute(data[:,0] - t_t*ones(length)))
v_t = average(data[:,3][i_t-5:i_t+5])
# make 20x20x20 grid of values for t_0, v_r and P with +-5% span
print  v_t
ts = linspace(0.95*t_t, 1.05*t_t, 20)
vs = linspace(0.95*v_t, 1.05*v_t, 20)
Ps = linspace(0.95*P_t, 1.05*P_t, 20)
# compute the least square to find best approximation
squares = zeros((20**3 , 4))
i = 0
for t_0 in ts:
    for v_r in vs:
        for P in Ps:
            s = sum((data[:,3] - v_r*cos(2*pi*(data[:,0] - t_0*ones(length))*P**(-1)))**2)
            squares[i] = [s, t_0, v_r, P]
            i += 1
"""
n = argmin(squares[:,0])
# compute planetary mass and star radial velocity model curve
t_0 = squares[n][1]
v_r = squares[n][2]
P = squares[n][3]
v = v_r*cos(2*pi*(data[:,0] - t_0*ones(length) )*P**(-1))
Mp = (M*solarmass)**(2/3.)*v_r*P**(1/3.)/(2*pi*G)**(1/3.)
# print planetary mass
print "Mass of the planet is M = %g kilograms" % (Mp)
# init figure for plot
fig = plt.figure()
ax = fig.add_subplot(111)
rc('mathtext', default='regular')
# plotting of raw data and model curve
ax.plot(data[:,0], data[:,3], lw=1, color='blue', label=r'Raw data')
ax.plot(data[:,0], v, lw=1.8, color='yellow', label=r'Modelled velocity')
# formating plot
ax.set_xlabel(r'$t$ [s]')
ax.set_ylabel(r'$v_r$ [m/s]')
# set title and enable legend
ax.set_title(r'Star radial velocity ($v_r$), aquired and modelled curves')
ax.legend()
plt.ylim((-400,500))
plt.xlim((0,2060000))
# show plot
plt.show()
raw_input()
"""
