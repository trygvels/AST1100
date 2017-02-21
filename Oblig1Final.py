from scitools.all import *
import numpy as np

# 2 is sattelite, 1 is Mars
x1 = zeros(n, float)
y1 = zeros(n, float)
x2 = zeros(n, float)
y2 = zeros(n, float)

vx_1 = zeros(n,float)
vy_1 = zeros(n,float)
vx_2 = zeros(n,float)
vy_2 = zeros(n,float)

x_1[0] = 0
y_1[0] = 0
x_2[0] = -298-3400 #km
y_2[0] = 0

m = 100

# Dont need z, because there are no forces acting in this direction
#v1(vec) = -4000j (jvector)

k = 0.00016
dt = 1 #s
def gravity(x1,x2,y1,y2):
    a = abs(x2-x1) #Length to y axis
    b = abs(y2-y1) #Length to x axis
    theta = arctan(float(b)/a) # angle between x-axis and position of sattelite
    r = abs(b/sin(theta)) #Distance between the two objects
    F = (G*m1*m2)/(r^2) #Total grav. force on objects
    if x1<x2:
        Fx_1 = F*cos(theta)
        Fx_2 = -F*cos(theta)
    else:
        Fx_1 = -F*cos(theta)
        Fx_2 = F*cos(theta)

   if y1<y2:
        Fy_1 = F*sin(theta)
        Fy_2 = -F*sin(theta)
    else:
        Fy_1 = -F*sin(theta)
        Fy_2 = F*sin(theta)
    return Fx_1, Fx_2, Fy_1, Fx_2

def f(vx_2,vy_2): #Drag on Beagle
    v = sqrt(vx_2^2+vy_2^2)
    f = -k*v
    theta = arctan(float(vy_2)/vx_2)
    f_x = abs(f*cos(theta))
    f_y = abs(f*sin(theta))
    if vx_2 > 0:
        f_x = -f_x
    if vy_2 > 0:
        f_y = -f_y
    return f_x, f_y


    
