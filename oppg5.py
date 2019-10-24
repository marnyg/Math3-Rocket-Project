from Earth import Earth
from SaturnV import SaturnV
from RocketState import RocketState
import matplotlib.pyplot as plt
from matplotlib import animation, rc
import RungeKuttaFehlberg as RKF
import ploter
import numpy as np
import math



def thrust_angle(self, time,angle_to_origin):
        return math.pi/2


earth = Earth()
firingTime=800
rocket = SaturnV(thrust_angle,firingTime)
starting_state = (1e-5, earth.equator_radius, 0.1,1)
state = RocketState(rocket, earth, starting_state, stepsize=1)


def doRungeKuttaRivertz():
    dimension = 5
    h = 1 / 4
    tol = 5e-20
    tEnd =5000
    function=state.mar_delta_state

    rkf = RKF.RungeKuttaFehlberg54(function, dimension, h, tol)
    while state.mycurrent_state[0] < tEnd:
        if (math.floor(state.mycurrent_state[0])%10==0):
            print("Time: %4.0d / %4.0d seconds" % (state.mycurrent_state[0],tEnd))
        state.mycurrent_state, Error = rkf.safeStep(state.mycurrent_state)

    print("Prepering plots")



def doPlots(data=False,animation=False,vectors=False):
    xs = [x[0] for x in state.stateLog]

    altitude = [(math.sqrt(x[2]**2 + x[1]**2) - earth.equator_radius) for x in [y for y in state.stateLog]]
    atmo_alt = [x for x in range(0, earth.upper_stratosphere[1] + 10000)]
    atmo_density = [earth.atmosphere_density(altitude) for altitude in atmo_alt]
    atmo_temp = [earth.__airtemp__(altitude) for altitude in atmo_alt]
    atmo_pressure = [earth.__pressure__(altitude) for altitude in atmo_alt]
    xpos = [(x[1] ) for x in [y for y in state.stateLog]]
    ypos = [(x[2] ) for x in [y for y in state.stateLog]]
    vel = [(math.sqrt(x[3]**2 + x[4]**2)) for x in [y for y in state.stateLog]]
    
    drag = [(math.sqrt(x[1]**2 + x[0]**2)) for x in [y for y in state.drags]]
    grav = [math.sqrt(y[1]**2 + y[0]**2) for y in state.gravities]
    forces = [math.sqrt(y[1]**2 + y[0]**2) for y in state.forces]
    thrusts = [rocket.current_force(y) for y in xs]


    if data:
        ploter.plots([
            (xs, thrusts,"Thrust"),
            (xs, drag,"Drag"), 
            (xs, grav,"Grav"),
            (xs, vel, "vel"),
            (xs, forces, "forces"),
            (xs, altitude, 'Altitude'),
            #(atmo_alt, atmo_density, 'Atmo density for given altitude (x-axis)'),
            #(atmo_alt, atmo_pressure, 'Atmo pressure'),
            #(atmo_alt, atmo_temp, 'Atmo temp')],
            (xs, state.masses,"Mass")], 
            rocket)
    if animation:
        ploter.movie(xs,earth,xpos,ypos)
    if vectors:
        gravAngels=([x[2] for x in state.gravities],'b','grav angle')
        dragAngels=([x[2] for x in state.drags],'r','drag angle')
        velocity=([x[2] for x in state.velocities],'y','velocity angle')
        thrustAngles = ([x[2] for x in state.forces], 'g', 'thrust angle')

        ploter.plotVector(xs,
                          [
                            gravAngels,
                           dragAngels,
                           velocity,
                           thrustAngles
                           ])
    ploter.show()


doRungeKuttaRivertz()
doPlots(animation=True,vectors=True,data=True)

