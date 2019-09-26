
from numpy import sqrt
import time

import numpy as np
import scipy.integrate as integrate

import matplotlib.pyplot as plot
import matplotlib.animation as animation
import RungeKuttaFehlberg as RFK

class Orbit:
    """
    
    Orbit Class

    init_state is [t0,x0,vx0,y0,vx0],
    where (x0,y0) is the initial position
    , (vx0,vy0) is the initial velocity
    and t0 is the initial time
    """
    def __init__(self,
                 init_state = [0, 0, 1, 1, 0],
                 h=1./30,
                 G=1,
                 m1=1,
                 m2=3,
                 simSpeed=5e-5):
        print(m2)
        self.GravConst = G
        self.mMane = m1
        self.mJord = m2
        self.state = np.asarray(init_state, dtype='float')
        self.rfk= RFK.RungeKuttaFehlberg54(self.ydot,5,h,simSpeed)

    
    def position(self):
        """compute the current x,y positions of the pendulum arms"""
        x = self.state[1]
        y = self.state[3]
        return (x, y)
    
    def energy(self):
        x = self.state[1]
        y = self.state[3]
        vx = self.state[2]
        vy = self.state[4]
        m1 = self.mMane
        m2 = self.mJord
        G = self.GravConst
        U=-G*m1*m2/sqrt(x**2+y**2)
        K= m1*(vx**2+vy**2)/2
        return K+U

    def time_elapsed(self):
        return self.state[0]

    def step(self, h):
        x=self.state
        self.state,E=self.rfk.safeStep(x)
    
    def ydot(self,x):
        G=self.GravConst
        m2=self.mJord
        Gm2=G*m2;
        
        px2=0;py2=0;
        px1=x[1];py1=x[3];vx1=x[2];vy1=x[4];
        dist=sqrt((px2-px1)**2+(py2-py1)**2);
        z=np.zeros(5);
        z[0]=1
        z[1]=vx1
        z[2]=(Gm2*(px2-px1))/(dist**3)
        z[3]=vy1
        z[4]=(Gm2*(py2-py1))/(dist**3)
        return z

class Moon:
    mass=7.3477e22
    velocity=[1020*10000000,0]#[x,y] the x component here is waaaay wrong, had to multiply it with 10000000 to get an orbit
    position=[0,405510]#[x,y]
    def getAsArray(): return [Moon.position[0],Moon.velocity[0],Moon.position[1],Moon.velocity[1]]

class Earth:
    mass=5.9736e24

# make an Orbit instance
dt = 1./30# 30 frames per second
simulationSpeed=5e-8
startTime=[0]

orbit = Orbit(
    np.concatenate([startTime,Moon.getAsArray()]),
    dt ,
    9.81,
    Moon.mass,
    Earth.mass,
    simulationSpeed)

# The figure is set
fig = plot.figure()
circle1 = plot.Circle((0, 0), 12756, color='g')
axes = fig.add_subplot(111, aspect='equal', autoscale_on=True,
                     xlim=(-5e5, 5e5), ylim=(-5e5,5e5))

line1, = axes.plot([], [], 'o-b', lw=2) # A green planet
#line2, = axes.plot([], [], 'o-y', lw=2) # A yellow sun
axes.add_artist(circle1)
time_text = axes.text(0.02, 0.95, '', transform=axes.transAxes)
energy_text = axes.text(0.02, 0.90, '', transform=axes.transAxes)
position_text = axes.text(0.02, 0.85, '', transform=axes.transAxes)
velocity_text= axes.text(0.02, 0.80, '', transform=axes.transAxes)

def init():
    """initialize animation"""
    line1.set_data([], [])
#    line2.set_data([], [])
    time_text.set_text('')
    energy_text.set_text('')
    position_text.set_text('')
    velocity_text.set_text('')
    return line1, time_text, energy_text

def animate(i):
    """perform animation step"""
    global orbit, dt
    orbit.step(dt*100)
    line1.set_data(*orbit.position())
#    line2.set_data([0.0,0.0])
    time_text.set_text('time = %.1f' % orbit.time_elapsed())
    energy_text.set_text('energy = %.3f J' % orbit.energy())
    position_text.set_text('position = %.3f x %.3f y' % (orbit.position()))
    velocity_text.set_text('velocity = %.3f x %.3f y' % (orbit.state[2],orbit.state[4]))
    return line1, time_text, energy_text, position_text, velocity_text

# choose the interval based on dt and the time to animate one step
# Take the time for one call of the animate.
t0 = time.time()
animate(0)
t1 = time.time()

delay = 1000 * dt - (t1 - t0)

anim=animation.FuncAnimation(fig,        # figure to plot in
                        animate,    # function that is called on each frame
                        frames=300, # total number of frames 
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
#anim.save('orbit.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plot.show()
