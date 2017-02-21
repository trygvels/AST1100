from scitools.std import *
from numpy.linalg import norm

G = 6.67428e-11
k = 1.6e-4
radius = 3.4e6
mars = 6.4*10**23 # kg
lander = 100.0 # kg
h = 100 # s
u0 = asarray([[-298e3 - radius, 0], [0.0, -4000], [-(G*mars)/abs(3698e3)**2, 0]])

def f(t,u):
	r = u[0]
	v = u[1]
	a = -k*v/lander - G*mars*r/(norm(r)**3)
	return asarray([v, a, zeros(2)])

u = zeros((6000, 3, 2))
u[0] = u0
for i in range(6000-1):
    t = i
    k0 = h*f(t, u[(i)])
    k1 = h*f(t + 0.5*h, u[(i)] + k0*0.5)
    k2 = h*f(t + 0.5*h, u[(i)] + k1*0.5)
    k3 = h*f(t + h, u[(i)] + k2)
    u[i+1] = u[i] + (1/6.0)*(k0 + 2*k1 + 2*k2 + k3)
    r = u[i+1]
    if norm(r) < 3400000:
        v = i
        break

x = u[:,0][:,0][:v]
y = u[:,0][:,1][:v]
plot(x, y)
raw_input()	
