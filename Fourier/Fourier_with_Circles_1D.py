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
from scipy import signal

from obspy import *
from obspy.clients.fdsn import Client

Nframes = 10000000
Rad = 50

WIDTH = 500
HEIGHT = 200
LEFT_CENTER = [WIDTH/(3*2), HEIGHT/2]

N = 20

#boxcar function
t_ = np.linspace(0, 50, 500, endpoint=False)
Function = signal.square(0.04*2*np.pi*t_)

#random distribution
#np.random.seed(6)
#y = 0
#Function = []
#for i in range(200):
#    Function.append(y)
#    y += np.random.normal(scale=1)

#sawtooth function
#Function = []
#for i in range(200):
#    Function.append(-1 + i/100) 


#test it with earthquake data
#client = Client("BGR")
#t1 = UTCDateTime("2011-03-11T05:58:50.000")
#st = client.get_waveforms("GR", "WET", "", "BHZ", t1, t1 + 0.01 * 60 * 60, 
#                          attach_response = True)
#st.remove_response(output="VEL")
#st.detrend('linear')
#st.detrend('demean')
#st.taper(10)
#Function = st[0].data
#plt.plot(Function)
#plt.show()


LENGTH = len(Function)

# gets Fourie Coefficients of Function
FT = fft(Function)
Amplitudes = np.absolute(FT)
#normalize Amplitudes
Amplitudes /= np.max(Amplitudes)
#Rescale with Radius setting
Amplitudes *= Rad 
Phases = np.arctan2(np.real(FT),np.imag(FT))

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure(figsize=(WIDTH/30,HEIGHT/30))
ax = plt.axes()
ax.set_ylim(0,HEIGHT)
ax.set_xlim(0,WIDTH)


""" Initiallize the circeling circls"""
Circles = []
Circle_Centers = []
Circle_Lines = []
# Initiallize all circles on the left side
c = np.copy(LEFT_CENTER)
cprev = np.copy(c)
for i in range(N):
    Radius = Amplitudes[i]
    
    circ = plt.Circle((c[0], c[1]), radius=Radius, facecolor="None", edgecolor='k', lw=1)
    c[0] = c[0] + Radius * np.cos(0 + Phases[i])
    c[1] = c[1] + Radius * np.sin(0 + Phases[i])
    
    Circles.append(circ)
    Circle_Centers.append(c)
    ax.add_patch(circ)
    
    line, = ax.plot([cprev[0],c[0]], [cprev[1], c[1]], color = "k", lw = 0.5) 
    Circle_Lines.append(line)
    
    cprev = np.copy(c)
    
    
""" Initiallize the output """

values, = ax.plot([],[],color = "k")
X = []
Y = []
X_r = []
Y_r = []
# line to connect circles and plot
con, = ax.plot([],[], color = "k", lw = 0.5)

real, = ax.plot([],[], color = "g", lw = 1)


def init():
    return tuple(Circles),values, con, tuple(Circle_Lines), real

def animate(i):
    
    dt = 2*np.pi * (i/LENGTH)
    
    c = np.copy(LEFT_CENTER)
    cprev = np.copy(c)
    for j, circ in enumerate(Circles):
        Radius = Amplitudes[j]
        
        circ.center = c[0], c[1]
        c[0] = c[0] + Radius * np.cos(dt*j + Phases[j])
        c[1] = c[1] + Radius * np.sin(dt*j + Phases[j])
        
        Circle_Lines[j].set_xdata([cprev[0], c[0]]) 
        Circle_Lines[j].set_ydata([cprev[1], c[1]])
        
        cprev = np.copy(c)
        
    
    X.append(WIDTH/3+i*(100/LENGTH))
    Y.insert(0,c[1])
    values.set_xdata(X)
    values.set_ydata(Y)
    
    con.set_xdata([c[0], WIDTH/3])
    con.set_ydata([c[1], c[1]])
    
    X_r.append(WIDTH/3+i*(100/LENGTH))
    Y_r.insert(0, LEFT_CENTER[1] + (-1*Function[i%LENGTH])*Rad )
    real.set_xdata(X_r)
    real.set_ydata(Y_r)
    
    if len(X)*(100/LENGTH) > (2*WIDTH/3)-5:
        X.pop()
        Y.pop()
        
    if len(X_r)*(100/LENGTH) > (2*WIDTH/3)-5:
        X_r.pop()
        Y_r.pop()
    
    return tuple(Circles),values, con, tuple(Circle_Lines)


anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=Nframes, interval=10)





















