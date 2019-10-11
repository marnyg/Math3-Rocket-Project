from Earth import Earth
from SaturnV import SaturnV
from RocketState import RocketState
import matplotlib.pyplot as plt
from matplotlib import animation, rc
import RungeKuttaFehlberg as RKF
import ploter


earth = Earth()
rocket = SaturnV()
starting_state = (0, earth.equator_radius, 0, 0)
state = RocketState(rocket, earth, starting_state, stepsize=1)


def doRungeKuttaRivertz():
    dimension = 5
    h = 1 / 4
    tol = 5e-18
    tEnd = 1022
    function=state.mar_delta_state

    rkf = RKF.RungeKuttaFehlberg54(function, dimension, h, tol)
    while state.mycurrent_state[0] < tEnd:
        state.mycurrent_state, Error = rkf.safeStep(state.mycurrent_state)
    #rkf.setStepLength(tEnd - state.mycurrent_state[0])
    #state.mycurrent_state, Error = rkf.safeStep(state.mycurrent_state)



def doPlots(data=False,animation=False):
    xs = [x[0] for x in state.stateLog]

    altitude = [(x[2] - earth.equator_radius) for x in [y for y in state.stateLog]]
    speed = [y[4] for y in state.stateLog]
    drags = [x for x in [y[1] for y in state.drags]]
    gravs = [x for x in [y[1] for y in state.gravities]]
    forcesy = [x for x in [y[1] for y in state.forces]]
    thrusts = [rocket.current_force(y) for y in xs]


    if data:
        ploter.plots([(xs, thrusts,"Thrust"), (xs, drags,"Drag"), (xs, gravs,"Grav"),
                  (xs, altitude,"Altitude"), (xs, state.masses,"Mass"), (xs, speed,"Speed")], rocket)
    if animation:
        ploter.movie(xs, altitude,earth)
    ploter.show()


doRungeKuttaRivertz()
doPlots(data=True,animation=True)

