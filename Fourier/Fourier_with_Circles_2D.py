"""
This code is mostly based on this video by Coding Train:
https://www.youtube.com/watch?v=Mm2eYfj0SgA&t=1464s
"""

# If you want to use it in a Jupyter Notebook enable:
#%matplotlib nbagg


import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from scipy.fftpack import fft
from scipy.signal import resample
from Drawing import drawing

Nframes = 10000000
Rad = 20

WIDTH = 400
HEIGHT = 200
LEFT_CENTER = [WIDTH/(4), HEIGHT/4]
TOP_CENTER =[2*WIDTH/(4), 3*HEIGHT/4]

N = 200

# prepare the data
drawing = np.array(drawing)

function_x = np.take(drawing,0,1)
function_y = np.take(drawing,1,1)

LENGTH = len(function_x)

# gets Fourie Coefficients of Function
FT_x = fft(function_x)
Amplitudes_x = np.absolute(FT_x)
FT_y = fft(function_y)
Amplitudes_y = np.absolute(FT_y)
#normalize Amplitudes
Amplitudes_x /= np.max(Amplitudes_x)
Amplitudes_y /= np.max(Amplitudes_y)
#Rescale with Radius setting
Amplitudes_x *= Rad 
Phases_x = np.arctan2(np.real(FT_x),np.imag(FT_x))
Amplitudes_y *= Rad 
Phases_y = np.arctan2(np.real(FT_y),np.imag(FT_y))



# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure(figsize=(WIDTH/30,HEIGHT/30))
ax = plt.axes()
ax.set_ylim(0,HEIGHT)
ax.set_xlim(0,WIDTH)


""" Initiallize the circeling circls"""

# Initiallize all circles on the left side

L_Circles = []
L_Circle_Centers = []
L_Circle_Lines = []

c = np.copy(LEFT_CENTER)
cprev = np.copy(c)
for i in range(N):
    Radius = Amplitudes_y[i]
    
    circ = plt.Circle((c[0], c[1]), radius=Radius, facecolor="None", edgecolor='k', lw=1)
    
    c[0] = c[0] + Radius * np.cos(0 + Phases_y[i])
    c[1] = c[1] + Radius * np.sin(0 + Phases_y[i]+np.pi)
    
    L_Circles.append(circ)
    L_Circle_Centers.append(c)
    ax.add_patch(circ)
    
    line, = ax.plot([cprev[0],c[0]], [cprev[1], c[1]], color = "k", lw = 0.5) 
    L_Circle_Lines.append(line)
    
    cprev = np.copy(c)
    
# Initiallize the circles on the top

T_Circles = []
T_Circle_Centers = []
T_Circle_Lines = []
    
c = np.copy(TOP_CENTER)
cprev = np.copy(c)
for i in range(N):
    Radius = Amplitudes_x[i]
    
    circ = plt.Circle((c[0], c[1]), radius=Radius, facecolor="None", edgecolor='k', lw=1)
    c[0] = c[0] + Radius * np.sin(0 + Phases_x[i])
    c[1] = c[1] + Radius * np.cos(0 + Phases_x[i])
    
    T_Circles.append(circ)
    T_Circle_Centers.append(c)
    ax.add_patch(circ)
    
    line, = ax.plot([cprev[0],c[0]], [cprev[1], c[1]], color = "k", lw = 0.5) 
    T_Circle_Lines.append(line)
    
    cprev = np.copy(c)
    
    
""" Initiallize the output """

values, = ax.plot([1,2,100],[2,3,200],color = "k")
X = []
Y = []

# line to connect circles and plot
con, = ax.plot([],[], color = "k", lw = 0.5)


def init():
    tuple(L_Circles), tuple(T_Circles),values, con, tuple(L_Circle_Lines), tuple(T_Circle_Lines)

def animate(i):
    
    dt = 2*np.pi * (i/(LENGTH)) *10
    
    L_c = np.copy(LEFT_CENTER)
    L_cprev = np.copy(L_c)
    
    for j, circ in enumerate(L_Circles):
        Radius = Amplitudes_y[j]
        
        circ.center = L_c[0], L_c[1]
        L_c[0] = L_c[0] + Radius * np.cos(dt*j + Phases_y[j])
        L_c[1] = L_c[1] + Radius * np.sin(dt*j + Phases_y[j] + np.pi)
        
        L_Circle_Lines[j].set_xdata([L_cprev[0], L_c[0]]) 
        L_Circle_Lines[j].set_ydata([L_cprev[1], L_c[1]])
        
        L_cprev = np.copy(L_c)
      
    
    T_c = np.copy(TOP_CENTER)
    T_cprev = np.copy(T_c)  
    for j, circ in enumerate(T_Circles):
        Radius = Amplitudes_x[j]
        
        circ.center = T_c[0], T_c[1]
        T_c[0] = T_c[0] + Radius * np.sin(dt*j + Phases_x[j])
        T_c[1] = T_c[1] + Radius * np.cos(dt*j + Phases_x[j])
        
        T_Circle_Lines[j].set_xdata([T_cprev[0], T_c[0]]) 
        T_Circle_Lines[j].set_ydata([T_cprev[1], T_c[1]])
        
        T_cprev = np.copy(T_c)
        
    
    X.insert(0, T_c[0])
    Y.insert(0, L_c[1])
    values.set_xdata(X)
    values.set_ydata(Y)
    
    con.set_xdata([L_c[0], T_c[0], T_c[0]])
    con.set_ydata([L_c[1], L_c[1], T_c[1]])
    
    
#    if len(X)*(100/LENGTH) > (2*WIDTH/3)-5:
#        X.pop()
#        Y.pop()
    
    
    return tuple(L_Circles), tuple(T_Circles),values, con, tuple(L_Circle_Lines), tuple(T_Circle_Lines)


anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=Nframes, interval= 100)












