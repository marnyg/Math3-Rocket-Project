import numpy as np
import RungeKuttaFehlberg as RKF
import numpy as np
import math as m 
import sys
import matplotlib.pyplot as plt
from matplotlib import animation, rc
import time
from numpy import sqrt



 #Jorda
diameter_ekvator = 12756.28 #km
poldiameter = 12713.56 #km
masse_Jorda = 5.9736*10**24 #kg
rotasjonsperiode_døgn = 0.997258 # døgn
rotasjonsperiode_timer = 23.934 #t
    
    #Månen
periapsis = 362570000 #m
apoapsis = 405410000 #m
store_halvakse = 384399 #km 0.003 AE
eksentrisitet =0.0549
omløpstid = 27.321582 #jorddøgn
gjennomsnittsfart = 1.022 # km/s
radius_ved_ekvator = 1738.14 # km
masse_Månen = 7.3477*10**22 # kg
    
G = 6.67428 * 10**-11


def F(Y):
    res=np.zeros(shape=(Y.shape))
    res[0] = 1
    res[1] = Y[2]
    res[2] = newton(Y[1],Y[1],Y[3])
    res[3] = Y[4]
    res[4] = newton(Y[3],Y[1],Y[3])
    return res;

def newton(top, x, y):
    return (-(G * masse_Jorda * top)/(x**2 + y**2)**(3/2))

def force(Y):
    return G*masse_Jorda*masse_Månen/(Y[2]**2 + Y[4]**2)**(1/2)
  
def length(Y):
    return sqrt(Y[1]**2+Y[3]**2) 

initial_values = np.array([1, 0, 970, apoapsis, 0 ])
W  = np.array([initial_values]);
h=1.0;
tol=(10**(-8)); ## skal være mindre men får ikke til å funke
rkf54 = RKF.RungeKuttaFehlberg54(F,5,h,tol)

for i in range(360):
    W_next, E_next = rkf54.safeStep(W[-1])
    W = np.append(W,[W_next], axis = 0)


dt = 1./30 # 30 frames per second
# The figure is set
fig = plt.figure()
axes = fig.add_subplot(111, aspect='equal', autoscale_on=False, xlim=(-480000000, 480000000), ylim=(-480000000, 480000000))

line1, = axes.plot([], [], 'o-y', lw=2) # A yellow moon
line2, = axes.plot([], [], 'o-g', lw=2) # A green earth
time_text = axes.text(0.02, 0.95, '', transform=axes.transAxes)
energy_text = axes.text(0.02, 0.90, '', transform=axes.transAxes)

def init():
    """initialize animation"""
    line1.set_data([], [])
    line2.set_data([], [])
    time_text.set_text('')
    energy_text.set_text('')
    return line1, line2, time_text, energy_text

def animate(i):
    """perform animation step"""
    line1.set_data(*(W[i][1],W[i][3]))
    line2.set_data([0.0,0.0])
    time_text.set_text('time = %.1f days'% (W[i][0]/86400))
    energy_text.set_text('length = %.3f' % length(W[i]))
    return line1,line2, time_text, energy_text

# choose the interval based on dt and the time to animate one step
# Take the time for one call of the animate.
t0 = time.time()
animate(0)
t1 = time.time()
print(t1-t0)
print( 8333.5 * dt - (t1 - t0))


#delay = 8300 * dt - (t1 - t0)
delay = 8333.5 * dt - (t1 - t0)

anim=animation.FuncAnimation(fig,        # figure to plot in
                        animate,    # function that is called on each frame
                        frames=100, # total number of frames 
                        interval=delay, # time to wait between each frame.
                        repeat=False,
                        blit=True, 
                        init_func=init # initialization
                        )

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
#anim.save('orbit.mp4', fps=30)
plt.show()
