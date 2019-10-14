from Earth import Earth
from SaturnV import SaturnV
from RocketState import RocketState
import matplotlib.pyplot as plt
from matplotlib import animation, rc
import RungeKuttaFehlberg as RKF
import ploter
import numpy as np
import math


earth = Earth()
rocket = SaturnV()
starting_state = (1e-5, earth.equator_radius,  0.1,1)
state = RocketState(rocket, earth, starting_state, stepsize=1)


def doRungeKuttaRivertz():
    dimension = 5
    h = 1 / 4
    tol = 5e-20
    tEnd = 1000
    function=state.mar_delta_state

    rkf = RKF.RungeKuttaFehlberg54(function, dimension, h, tol)
    while state.mycurrent_state[0] < tEnd:
        print(state.mycurrent_state[0])
        state.mycurrent_state, Error = rkf.safeStep(state.mycurrent_state)
    #rkf.setStepLength(tEnd - state.mycurrent_state[0])
    #state.mycurrent_state, Error = rkf.safeStep(state.mycurrent_state)



def doPlots(data=False,animation=False,vectors=False):
    xs = [x[0] for x in state.stateLog]

    altitude = [(x[2] - earth.equator_radius) for x in [y for y in state.stateLog]]
    xpos = [(x[1] ) for x in [y for y in state.stateLog]]
    ypos = [(x[2] ) for x in [y for y in state.stateLog]]
    xvel = [(x[3] ) for x in [y for y in state.stateLog]]
    yvel = [(x[4] ) for x in [y for y in state.stateLog]]
    dragy = [x for x in [y[1] for y in state.drags]]
    dragx = [x for x in [y[0] for y in state.drags]]
    gravy = [x for x in [y[1] for y in state.gravities]]
    gravx = [x for x in [y[0] for y in state.gravities]]
    forcesy = [x for x in [y[1] for y in state.forces]]
    forcesx = [x for x in [y[0] for y in state.forces]]
    thrusts = [rocket.current_force(y) for y in xs]


    if data:
        ploter.plots([(xs, thrusts,"Thrust"),(xs, dragx,"Drag x"), (xs, dragy,"Drag y"), (xs, gravx,"Grav x"),(xs, gravy,"Grav y"), (xs, yvel,"yvel"),(xs, xvel,"xvel"),(xs, ypos,"ypos"), (xs, xpos,"xpos"), (xs, state.masses,"Mass")], rocket)
    if animation:
        ploter.movie(xs,earth,xpos,ypos)
    if vectors:

        gravAngels=([x[2] for x in state.gravities],'b','grav angle')
        dragAngels=([x[2] for x in state.drags],'r','drag angle')
        velocity=([x[2] for x in state.velocities],'y','velocity angle')

        ploter.plotVector(xs,
                          [
                            gravAngels,
                           dragAngels,
                           velocity
                           ])
    ploter.show()


doRungeKuttaRivertz()
doPlots(animation=True,vectors=True,data=True)

