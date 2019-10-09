from Earth import Earth
from SaturnV import SaturnV
from RocketState import RocketState
import matplotlib.pyplot as plt
from matplotlib import animation, rc

earth = Earth()
rocket = SaturnV()
starting_state = (0, earth.equator_radius, 0, 0) # (time=1, xpos=0, ypos=earth.equator_radius, xvel=0, yvel=0)
state = RocketState(rocket, earth, starting_state, stepsize=1)



num_iterations =  (rocket.stage_1_firing_time + rocket.stage_2_firing_time + rocket.stage_3_firing_time)
print(rocket.total_firing_time)

seconds = 11 * 60

for i in range(num_iterations):
    state.rk45(tolerance=05e-14)

xs = [x for x in range(num_iterations + 1)]

altitude = [(x - earth.equator_radius) for x in [y[1] for y in  state.current_state]] # only altitudes
speed = [x for x in [y[3] for y in state.current_state]]
drags = [x for x in [y[1] for y in state.drags]]
gravs = [x for x in [y[1] for y in state.gravities]]
forcesy = [x for x in [y[1] for y in state.forces]]
thrusts = [x for x in [rocket.current_force(y) for y in xs]]

stage_1_end = rocket.stage_1_firing_time
stage_2_end = rocket.stage_1_firing_time + rocket.stage_2_firing_time
stage_3_end = rocket.stage_1_firing_time + rocket.stage_2_firing_time + rocket.stage_3_firing_time

def points(ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9):
    ax1.plot(stage_1_end, thrusts[stage_1_end], color='r', marker='o', linestyle='dashed', linewidth=2, markersize=4)
    ax1.plot(stage_2_end, thrusts[stage_2_end], color='m', marker='o', linestyle='dashed', linewidth=2, markersize=4)
    ax1.plot(stage_3_end, thrusts[stage_3_end], color='y', marker='o', linestyle='dashed', linewidth=2, markersize=4)
    ax2.plot(stage_1_end, drags[stage_1_end], color='r', marker='o', linestyle='dashed', linewidth=2, markersize=4)
    ax2.plot(stage_2_end, drags[stage_2_end], color='m', marker='o', linestyle='dashed', linewidth=2, markersize=4)
    ax2.plot(stage_3_end, drags[stage_3_end], color='y', marker='o', linestyle='dashed', linewidth=2, markersize=4)
    ax3.plot(stage_1_end, gravs[stage_1_end], color='r', marker='o', linestyle='dashed', linewidth=2, markersize=4)
    ax3.plot(stage_2_end, gravs[stage_2_end], color='m', marker='o', linestyle='dashed', linewidth=2, markersize=4)
    ax3.plot(stage_3_end, gravs[stage_3_end], color='y', marker='o', linestyle='dashed', linewidth=2, markersize=4)
    ax4.plot(stage_1_end, speed[stage_1_end], color='r', marker='o', linestyle='dashed', linewidth=2, markersize=4)
    ax4.plot(stage_2_end, speed[stage_2_end], color='m', marker='o', linestyle='dashed', linewidth=2, markersize=4)
    ax4.plot(stage_3_end, speed[stage_3_end], color='y', marker='o', linestyle='dashed', linewidth=2, markersize=4)
    ax5.plot(stage_1_end, altitude[stage_1_end], color='r', marker='o', linestyle='dashed', linewidth=2, markersize=4)
    ax5.plot(stage_2_end, altitude[stage_2_end], color='m', marker='o', linestyle='dashed', linewidth=2, markersize=4)
    ax5.plot(stage_3_end, altitude[stage_3_end], color='y', marker='o', linestyle='dashed', linewidth=2, markersize=4)
    ax6.plot(stage_1_end, state.masses[stage_1_end], color='r', marker='o', linestyle='dashed', linewidth=2, markersize=4)
    ax6.plot(stage_2_end, state.masses[stage_2_end], color='m', marker='o', linestyle='dashed', linewidth=2, markersize=4)
    ax6.plot(stage_3_end, state.masses[stage_3_end], color='y', marker='o', linestyle='dashed', linewidth=2, markersize=4)
    ax7.plot(stage_1_end, forcesy[stage_1_end], color='r', marker='o', linestyle='dashed', linewidth=2, markersize=4)
    ax7.plot(stage_2_end, forcesy[stage_2_end], color='m', marker='o', linestyle='dashed', linewidth=2, markersize=4)
    ax7.plot(stage_3_end, forcesy[stage_3_end], color='y', marker='o', linestyle='dashed', linewidth=2, markersize=4)

def plots():
    fig, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) = plt.subplots(3, 3)
    ax1.set_title('Thrust')
    ax1.plot(xs, thrusts)
    
    ax2.set_title('drag')
    ax2.plot(xs, drags)
    
    ax3.set_title('gravity')
    ax3.plot(xs, gravs)
    
    ax4.set_title('speed')
    ax4.plot(xs, speed)
   
    ax5.set_title('altitude')
    ax5.plot(xs, altitude)
    
    #ax5.fill_between(xs, 0, [earth.troposphere[1] for x in altitude])
    
    #ax5.plot(xs, [earth.troposphere[1] for x in altitude])
    #ax5.plot(xs, [earth.lower_stratosphere[1] for x in altitude])
    
    ax6.set_title('mass')
    ax6.plot(xs, state.masses)
    
    
    ax7.set_title('Sum of forces on rocket')
    ax7.plot(xs, forcesy)
    

    #plt.axvline(x=rocket.stage_1_firing_time)
    #plt.axvline(x=(rocket.stage_1_firing_time + rocket.stage_2_firing_time))
    #plt.axvline(x=(rocket.stage_1_firing_time + rocket.stage_2_firing_time + rocket.stage_3_firing_time))
    plt.show()


def movie(xs, altitude):
    fig = plt.figure()
    ax = plt.axes(xlim=(-max(altitude), max(altitude)), ylim=(-2, max(altitude)))
    line, = ax.plot([], [], 'o-y', lw=2)

    # initialization function: plot the background of each frame
    def init():
        line.set_data([], [])
        return line,

    # animation function.  This is called sequentially
    def animate(i):
        x = xs[i]
        y = altitude[i]
        line.set_data(x, y)
        return line,


    normal_speed = 1000 # ms delay between frames
    double_speed = normal_speed / 2
    quad_speed = normal_speed / 4
    octa_speed = normal_speed / 8

    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=num_iterations, interval=octa_speed, blit=True)
    plt.show()

plots()


#for i in range(rocket.total_firing_time):
    #print(rocket.current_force(i))

