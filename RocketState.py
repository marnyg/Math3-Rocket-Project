from SaturnV import SaturnV
from RungeKuttaFehlberg import RungeKuttaFehlberg54
import numpy as np
import math
import sys

class RocketState:
    def __init__(self, rocket, planet, initial_state, stepsize):
        xpos_start, ypos_start, xvel_start, yvel_start = initial_state
        self.planet = planet

        self.xpos_start = xpos_start 
        self.ypos_start = ypos_start
        self.xvel_start = xvel_start
        self.yvel_start = yvel_start
        
        self.xpos_current = xpos_start
        self.ypos_current = ypos_start
        self.xvel_current = xvel_start
        self.yvel_current = yvel_start
        self.time = 0
        self.start_state = [xpos_start, ypos_start, xvel_start, yvel_start]
        self.mystart_state = [1,xpos_start, ypos_start, xvel_start, yvel_start]

        self.current_state = [[xpos_start, ypos_start, xvel_start, yvel_start]]
        self.mycurrent_state = self.mystart_state
        self.stateLog=[self.mystart_state]
        self.time_increments = [0]
        self.forces = [(0, 0, 0)]
        self.masses = [rocket.total_loaded_mass]
        self.thrusts = [0]
        self.thrustAngles = [0]
        
        (working_force), (drag_force), (grav_force),(velocity) = rocket.total_working_force(self.time, self.planet, xpos_start, xvel_start, ypos_start, yvel_start)

        self.gravities = [(grav_force[0], grav_force[1],0)] #[(0, 0)]
        self.velocities=[(0,0,0)]
        self.drags = [(0, 0,0)]
        self.rocket = rocket
        self.stepsize = stepsize


    def delta_state(self, time, current_state): # Returns change in time from last step, and change in position and velocity with this timestep [x, y, xvel, yvel]
        previous_xpos, previous_ypos, previous_xvel, previous_yvel = current_state # last element in list
        
        prevous_time_value = self.time_increments[-1] # last element in list    
        
        # How far does time jump at each step
        time_increment = time - prevous_time_value
        
        # Find the sum of all forces working on the rocket at this time
        (working_force), (drag_force), (grav_force) = self.rocket.total_working_force(time, self.planet, previous_xpos, previous_xvel, previous_ypos, previous_yvel)

        
        current_mass = self.rocket.current_mass(time)
        
        delta_xvel = working_force[0] / current_mass
        delta_yvel = working_force[1] / current_mass

        newState=[previous_xvel,previous_yvel,delta_xvel,delta_yvel]

        return time_increment, newState

    def loggState(self,working_force,time,drag_force,grav_force,next_state,velocity):
        self.forces.append(working_force)
        self.masses.append(self.rocket.current_mass(time))
        self.drags.append(drag_force)
        self.gravities.append(grav_force)
        self.thrusts.append(self.rocket.current_force(time))

        self.stateLog.append(next_state)
        
        self.velocities.append(velocity)



    def mar_delta_state(self, current_state): # Returns change in time from last step, and change in position and velocity with this timestep [x, y, xvel, yvel]
        time, previous_xpos, previous_ypos, previous_xvel, previous_yvel = current_state # last element in list
        # Find the sum of all forces working on the rocket at this time
        #(working_force), (drag_force), (grav_force),(velocity) = self.rocket.total_working_force(time, self.planet, previous_xpos, previous_xvel, previous_ypos, previous_yvel)
        (forcex, forcey, thrustAngle), (dragx, dragy,dragAngle), (gravx, gravy,gravAngle),(velx,vely,velocity_angle) = self.rocket.total_working_force(time, self.planet, previous_xpos, previous_xvel, previous_ypos, previous_yvel)
        
        current_mass = self.rocket.current_mass(time)
        
        delta_xvel = forcex / current_mass
        delta_yvel = forcey / current_mass

        delta_state=[1,previous_xvel,previous_yvel,delta_xvel,delta_yvel]
        next_state= current_state+delta_state
        

        self.loggState((forcex, forcey, thrustAngle),time,(dragx, dragy, dragAngle), (gravx, gravy, gravAngle),next_state,(velx, vely, velocity_angle))

        return delta_state




