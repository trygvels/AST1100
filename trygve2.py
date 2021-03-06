from scitools.std import *
from numpy.linalg import norm

G = 6.67428e-11
k = 1.6e-4
radius = 3.4e6
mars = 6.4*10**23 # kg
lander = 100.0 # kg
dt = 1 # s
u0 = asarray([[-298e3 - radius, 0], [0.0, -4000], [-(G*mars)/abs(3698e3)**2, 0]])

def f(u, t):
	r = u[0]
	v = u[1]
	a = -k*v/lander - G*mars*r/(norm(r)**3)
	return asarray([v, a, zeros(2)])

u = zeros((70000, 3, 2))
u[0] = u0
for i in range(70000-1):
	t = i + 1
	u[i+1] = u[i] + dt*f(u[i], 0)
	r = u[i+1]
	if norm(r) < 3400e3:
		v = i
		break

x = u[:,0][:,0][:v]
y = u[:,0][:,1][:v]
plot(x, y)
raw_input()
