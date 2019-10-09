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
print('Gravity at time 0:', earth.gravitational_force(rocket.current_mass(0), earth.equator_radius))

'''
xs = [i for i in range(0, 50000)]

pressures = [earth.__pressure__(i) for i in xs]
temperatures = [earth.__airtemp__(i) for i in xs]
densities = [earth.atmosphere_density(i) for i in xs]

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
ax1.set_title('Pressures')
ax1.plot(xs, pressures)
ax2.set_title('Temps')
ax2.plot(xs, temperatures)
ax3.set_title('Density')
ax3.plot(xs, densities)
plt.show()

seconds = 11 * 60
'''
state.rk45(05e-4, num_iterations + 100)

#xs = [x for x in range(num_iterations + 1)]
xs = state.time_increments
print('End time:', xs[-1])

altitude = [(x - earth.equator_radius) for x in [y[1] for y in  state.current_state]] # only altitudes
speed = [x for x in [y[3] for y in state.current_state]]
drags = [x for x in [y[1] for y in state.drags]]
gravs = [x for x in [y[1] for y in state.gravities]]
forcesy = [x for x in [y[1] for y in state.forces]]
thrusts = [rocket.current_force(y) for y in xs]

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
    
    #points(ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9)
    #plt.axvline(x=rocket.stage_1_firing_time)
    #plt.axvline(x=(rocket.stage_1_firing_time + rocket.stage_2_firing_time))
    #plt.axvline(x=(rocket.stage_1_firing_time + rocket.stage_2_firing_time + rocket.stage_3_firing_time))
    plt.show()


def movie(xs, altitude):
    fig = plt.figure()
    ax = plt.axes(xlim=(-max(altitude), max(altitude)), ylim=(-2, max(altitude)))
    line, = ax.plot([], [], 'o-y', lw=2)
    line2, = ax.plot([], [], '_-b', lw=2)
    line3, = ax.plot([], [], '_-b', lw=2)

    # initialization function: plot the background of each frame
    def init():
        line.set_data([], [])
        line2.set_data([], [])
        line3.set_data([], [])
        return line, line2, line3

    # animation function.  This is called sequentially
    def animate(i):
        print('frame:', i, 'altitude:', altitude[i])
        x = xs[i]
        y = altitude[i]
        line.set_data(x, y)
        line2.set_data(0, earth.troposphere[1])
        line3.set_data(0, earth.lower_stratosphere[1])
        return line, line2, line3


    normal_speed = 10 # ms delay between frames
    double_speed = normal_speed / 2
    quad_speed = normal_speed / 4
    octa_speed = normal_speed / 8

    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(altitude), interval=1, blit=True)
    plt.show()

plots()
#movie(xs, altitude)

#for i in range(rocket.total_firing_time):
    #print(rocket.current_force(i))

