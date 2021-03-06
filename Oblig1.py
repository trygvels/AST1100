
from scitools.std import *
from numpy import append, zeros, array
from math import sqrt
n = 1000
# 2 is sattelite, 1 is Mars
x1 = zeros(n, float)
y1 = zeros(n, float)
x2 = zeros(n, float)
y2 = zeros(n, float)

vx_1 = zeros(n,float)
vy_1 = zeros(n,float)
vx_2 = zeros(n,float)
vy_2 = zeros(n,float)

x1[0] = 0
y1[0] = 0
x2[0] = -298-3400 #km
y2[0] = 0
vy_2[0] = -4000

G = 6.67*10**-11
m = 100.0
M = 6.4*10**23
# Dont need z, because there are no forces acting in this direction


def gravity(x1,x2,y1,y2):
    a = abs(x2-x1)                #Length to y axis
    b = abs(y2-y1)                #Length to x axis
    theta = arctan(float(b)/a)    #angle between x-axis and position of sattelite
    r = sqrt(a**2+b**2)      #Distance between the two objects 
    F = (G*m*M)/(r**2)            #Total grav. force on objects

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
    return Fx_1, Fx_2, Fy_1, Fy_2

def f(vx_2,vy_2): #Drag on Beagle
    v = sqrt(vx_2**2+vy_2**2)
    k = float(0.00016)
    f = -k*v
    theta = arctan(float(vy_2)/vx_2)
    f_x = abs(f*cos(theta))
    f_y = abs(f*sin(theta))
    if vx_2 > 0:
        f_x = -f_x
    if vy_2 > 0:
        f_y = -f_y
    return f_x, f_y


dt = 1 #s
i = 0
land = 'no'
while land =='no' and i<(n-2):
    Fx_1, Fx_2, Fy_1, Fy_2 = gravity(x1[i],x2[i],y1[i],y2[i])
    f_x, f_y = f(vx_2[i], vy_2[i])
    vx_1[i+1]= vx_1[i] + (Fx_1/M)*dt
    vx_2[i+1]= vx_2[i] + ((Fx_2+f_x)/m)*dt
    vy_1[i+1]= vy_1[i] + (Fy_1/M)*dt
    vy_2[i+1]= vy_2[i] + ((Fy_2+f_y)/m)*dt

#Calculate the new position by standard kinematics
    x1[i+1] = x1[i] + (vx_1[i]*dt)
    x2[i+1] = x2[i] + (vx_2[i]*dt)
    y1[i+1] = y1[i] + (vy_1[i]*dt)
    y2[i+1] = y2[i] + (vy_2[i]*dt)


#Check if the spaceship has landed
    radius = 3400
    if sqrt(x2[i]**2+y2[i]**2)<radius:
        land = 'yes'
    i = i + 1
"""
HVOR BLIR DET AV FRIKSJONEN?!?!?!?!?!!?!?
"""
#Plotcommands
x_1 = array(x1)
x_2 = array(x2)
y_1 = array(y1)
y_2 = array(y2)
print x_2, y_2
plot(x_2,y_2,"-r")
