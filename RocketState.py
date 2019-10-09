from SaturnV import SaturnV
from RungeKuttaFehlberg import RungeKuttaFehlberg54
import numpy as np
import math

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

        self.current_state = [[xpos_start, ypos_start, xvel_start, yvel_start]]
        self.time_increments = [0]
        self.forces = [(0, 0)]
        self.masses = [rocket.total_loaded_mass]
        self.thrusts = [0]
        
        (working_force), (drag_force), (grav_force) = rocket.total_working_force(self.time, self.planet, xpos_start, xvel_start, ypos_start, yvel_start)

        self.gravities = [(grav_force[0], grav_force[1])] #[(0, 0)]
        self.drags = [(0, 0)]
        self.rocket = rocket
        self.stepsize = stepsize

    def delta_state(self, time, current_state): # Returns change in time from last step, and change in position and velocity with this timestep [x, y, xvel, yvel]
        previous_xpos, previous_ypos, previous_xvel, previous_yvel = current_state[-1] # last element in list
        
        prevous_time_value = self.time_increments[-1] # last element in list    
        
        # How far does time jump at each step
        time_increment = time - prevous_time_value

        # The next (x, y) will be (current_x, current_y) + (current_xvel, current_yvel)
        delta_xpos = previous_xvel
        delta_ypos = previous_yvel
        
        # Find the sum of all forces working on the rocket at this time
        (working_force), (drag_force), (grav_force) = self.rocket.total_working_force(time, self.planet, previous_xpos, previous_xvel, previous_ypos, previous_yvel)
        '''
        self.forces.append(working_force)
        self.masses.append(self.rocket.current_mass(time))
        self.drags.append(drag_force)
        self.gravities.append(grav_force)
        '''
        # The next velocity (next_xvel, next_yvel) will be 
        # the force currently acting on the rocket, divided by the current mass of the rocket
        # Both values are dependant on the time
        # V = dist/time, V' = V/time = acceleration (a), F = ma -> a = F / m
        current_mass = self.rocket.current_mass(time)
        
        delta_xvel = working_force[0] / current_mass
        delta_yvel = working_force[1] / current_mass

        #print("Working force at time " + str(time) + " is: ", working_force)
        #print("Mass at time " + str(time) + " is: ", self.rocket.current_mass(time))
        #return time_increment, [delta_xpos, delta_ypos, delta_xvel, delta_yvel]

        # F(time, )
        return time_increment, [delta_xpos, delta_ypos, delta_xvel, delta_yvel]

    def increment(self, end_time):    
        if len(self.time_increments) == 0:
            self.time_increments.append(0)

        '''
        next_time = self.time_increments[-1] + self.stepsize
        time_increment, delta_state = self.delta_state(next_time)
        # next_state = self.current_state[-1] + stepsize * delta_state

        
        # Euler method start
        next_state = []
        for i in range(len(self.current_state[-1])):
            next_state.append(self.current_state[-1][i] + stepsize * delta_state[i])
        # Euler method end
        '''
        '''
        state = np.array([self.time] + self.start_state);
        tolerance = 05e-14;
        
        rkf54 = RungeKuttaFehlberg54( self.rkf45_translate, 5, self.stepsize, tolerance)
        counter = 0
        while( state[0] < end_time):
            #print(counter + 1)
            counter += 1
            state, E = rkf54.safeStep(state)
            self.time_increments.append(state[0])
            self.current_state.append(state[1:])
            
        rkf54.setStepLength( end_time - state[0] )
        state, E = rkf54.step(state)
        self.time_increments.append(state[0])
        self.current_state.append(state[1:])


        #self.current_state.append(next_state)
        #self.time_increments.append(next_time)
        #print(self.current_state[-1])
        '''

    def rkf45_translate(self, last_step):
        time_change = self.stepsize

        current_time = last_step[0] + time_change
        time_increment, delta_change = self.delta_state(current_time, self.current_state[-1])

        return [time_change] + delta_change
        #next_time = self.time_increments[-1] + self.stepsize
        #time_increment, delta_state = self.delta_state(next_time)

    def best_step_size(self, tolerance, current_step_size, zn, wn):
        s = ((tolerance * current_step_size) / (2 * abs(zn - wn)))**(1/4)
        return s * current_step_size

    def rk45(self, tolerance):
        k1 = self.stepsize * self.delta_state(self.time_increments[-1], self.current_state)

        k2w = []
        for i in range(len(self.current_state[-1])):
            k2w.append(self.current_state[-1][i] + 1/4 * k1[1][i])

        k2 = self.delta_state(self.time_increments[-1] + 1/4 * self.stepsize, [k2w])

        k3w = []
        for i in range(len(self.current_state[-1])):
            k3w.append(self.current_state[-1][i] + 3/32 * k1[1][i] + 9/32 * k2[1][i])

        k3 = self.delta_state(self.time_increments[-1] + 3/8 * self.stepsize, [k3w])

        k4w = []
        for i in range(len(self.current_state[-1])):
            k4w.append(self.current_state[-1][i] + 1932/2197 * k1[1][i] - 7200/2197 * k2[1][i] + 7296/2197 * k3[1][i])

        k4 = self.delta_state(self.time_increments[-1] + 12/13 * self.stepsize, [k4w])

        k5w = []
        for i in range(len(self.current_state[-1])):
            k5w.append(self.current_state[-1][i] + 439/216 * k1[1][i] - 8 * k2[1][i] + 3680/513 * k3[1][i] - 845/4104 * k4[1][i])

        k5 = self.delta_state(self.time_increments[-1] + self.stepsize, [k5w])


        k6w = []
        for i in range(len(self.current_state[-1])):
            k6w.append(self.current_state[-1][i] - 8/27 * k1[1][i] + 2 * k2[1][i] - 3544/2565 * k3[1][i] - 1859/4104 * k4[1][i] - 11/40 * k5[1][i])

        k6 = self.delta_state(self.time_increments[-1] + 1/2 * self.stepsize, [k6w])

        
        next_state = []
        zn = []
        for i in range(len(self.current_state[-1])):
            state_value = self.current_state[-1][i]
            next_state.append(state_value + self.stepsize * (25/216 * k1[1][i] + 1408/2565 * k3[1][i] + 2197/4104 * k4[1][i] - 1/5 * k5[1][i]))
            zn.append(state_value + self.stepsize * (16/135 * k1[1][i] + 6656/12825 * k3[1][i] + 28561/56430 * k4[1][i] - 9/50 * k5[1][i] + 2/55 * k6[1][i]))

        subtraced = self.subtract_vectors(zn, next_state)
        optimal_step_size = (tolerance * self.stepsize) / (2 * self.absoulte_value(subtraced)) 
        print(optimal_step_size)

        en = []
        for i in range(len(next_state)):
            en.append(abs(zn[i] - next_state[i]))
            
        (working_force), (drag_force), (grav_force) = self.rocket.total_working_force(self.time_increments[-1], self.planet, next_state[0], next_state[2], next_state[1], next_state[3])
        
        self.forces.append(working_force)
        self.masses.append(self.rocket.current_mass(self.time_increments[-1]))
        self.drags.append(drag_force)
        self.gravities.append(grav_force)
        self.thrusts.append(self.rocket.current_force(self.time_increments[-1]))
        self.current_state.append(next_state)
        self.time_increments.append(self.time_increments[-1])
        
    def absoulte_value(self, vector):
        squared_sum = 0
        for i in vector:
            squared_sum += i**2

        return math.sqrt(squared_sum)

    def subtract_vectors(self, vector_a, vector_b):
        result = []
        if len(vector_a) == len(vector_b):
            for i in range(len(vector_a)):
                result.append(vector_a[i] - vector_b[i])
            return result
        else:
            print('Vectors does not have same size')