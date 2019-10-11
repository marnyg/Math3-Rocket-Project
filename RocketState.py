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
        self.forces = [(0, 0)]
        self.masses = [rocket.total_loaded_mass]
        self.thrusts = [0]
        
        (working_force), (drag_force), (grav_force) = rocket.total_working_force(self.time, self.planet, xpos_start, xvel_start, ypos_start, yvel_start)

        self.gravities = [(grav_force[0], grav_force[1])] #[(0, 0)]
        self.drags = [(0, 0)]
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

    def loggState(self,working_force,time,drag_force,grav_force,next_state):
        self.forces.append(working_force)
        self.masses.append(self.rocket.current_mass(time))
        self.drags.append(drag_force)
        self.gravities.append(grav_force)
        self.thrusts.append(self.rocket.current_force(time))
        self.stateLog.append(next_state)



    def mar_delta_state(self, current_state): # Returns change in time from last step, and change in position and velocity with this timestep [x, y, xvel, yvel]
        time, previous_xpos, previous_ypos, previous_xvel, previous_yvel = current_state # last element in list
        # Find the sum of all forces working on the rocket at this time
        (working_force), (drag_force), (grav_force) = self.rocket.total_working_force(time, self.planet, previous_xpos, previous_xvel, previous_ypos, previous_yvel)

        
        current_mass = self.rocket.current_mass(time)
        
        delta_xvel = working_force[0] / current_mass
        delta_yvel = working_force[1] / current_mass

        delta_state=[1,previous_xvel,previous_yvel,delta_xvel,delta_yvel]
        next_state= current_state+delta_state

        self.loggState(working_force,time,drag_force,grav_force,next_state)

        return delta_state







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

    def step(self):
        current_time = self.time_increments[-1]
        current_state = self.current_state[-1]
        last_time_increment = self.time_increments[-1]
        
        delta_time, delta_state = self.delta_state(current_time, current_state)
        
        k1 = [] # k1 = h * f(tk, yk) 
        for i in range(len(current_state)):
            k1.append(self.stepsize * delta_state[i])
        
        k2w = []
        for i in range(len(current_state)):
            k2w.append(current_state[i] + 1/4 * k1[i])
        
        
        k2 = self.mult_vector_by_scalar(self.delta_state(last_time_increment + 1/4 * self.stepsize, k2w)[-1], self.stepsize)

        k3w = []
        for i in range(len(current_state)):
            k3w.append(current_state[i] + 3/32 * k1[i] + 9/32 * k2[i])

        k3 = self.mult_vector_by_scalar(self.delta_state(last_time_increment + 3/8 * self.stepsize, k3w)[-1], self.stepsize)

        k4w = []
        for i in range(len(current_state)):
            k4w.append(current_state[i] + 1932/2197 * k1[i] - 7200/2197 * k2[i] + 7296/2197 * k3[i])

        k4 = self.mult_vector_by_scalar(self.delta_state(last_time_increment + 12/13 * self.stepsize, k4w)[-1], self.stepsize)

        k5w = []
        for i in range(len(current_state)):
            k5w.append(current_state[i] + 439/216 * k1[i] - 8 * k2[i] + 3680/513 * k3[i] - 845/4104 * k4[i])

        k5 = self.mult_vector_by_scalar(self.delta_state(last_time_increment + self.stepsize, k5w)[-1], self.stepsize)


        k6w = []
        for i in range(len(current_state)):
            k6w.append(current_state[i] - 8/27 * k1[i] + 2 * k2[i] - 3544/2565 * k3[i] - 1859/4104 * k4[i] - 11/40 * k5[i])

        k6 = self.mult_vector_by_scalar(self.delta_state(last_time_increment + 1/2 * self.stepsize, k6w)[-1], self.stepsize)

        
        next_state = []
        zn = []
        for i in range(len(current_state)):
            state_value = current_state[i]
            next_state.append(state_value + self.stepsize * (25/216 * k1[i] + 1408/2565 * k3[i] + 2197/4104 * k4[i] - 1/5 * k5[i]))
            zn.append(state_value + self.stepsize * (16/135 * k1[i] + 6656/12825 * k3[i] + 28561/56430 * k4[i] - 9/50 * k5[i] + 2/55 * k6[i]))
        
        #print('Next_state from step at time ' + str(current_time), next_state)
        return next_state, zn

    def mult_vector_by_scalar(self, vec, scalar):
        result = []
        for i in vec:
            result.append(i * scalar)
        return result

    def rk45(self, tolerance, end_time):
        while(self.time_increments[-1] < end_time):
            # Do a step with current stepsize and returns next_step (fourt order RK solution) and zn (more accurate fifth order RK solution)
            next_state, zn = self.step() 
            
            # Calculate error, see method comments for more explanation
            error = self.calculate_error(next_state, zn)

            if self.error_tolerated(error, tolerance): 
                # Calculate a better stepsize, based on current error and stepsize, and update the stepsize
                stepsize_change_factor = None
                if error == 0:
                    stepsize_change_factor = 2
                else:
                    stepsize_change_factor = (tolerance * self.stepsize) / (2 * error)
                self.stepsize = stepsize_change_factor * self.stepsize
            
            
            max_num_stepsize_changes = 20 # To avoid infinite loop
            num_stepsize_changes = 0 # Current number of stepsize changes

            # While the current error is not tolerated, take current step again, but with half the stepsize.
            # Do this for a maximum of 10 times, only to avoid infinite loop

            
            while(not self.error_tolerated(error, tolerance)):
                self.stepsize = self.stepsize * 0.1 # Halve the current stepsize and calculate next_step and zn again
                next_state, zn = self.step()
                error = self.calculate_error(next_state, zn)
                print('Error: ' + str(error) + ' not tolerated, halving')
                num_stepsize_changes += 1
                #if(num_stepsize_changes >= max_num_stepsize_changes):
                    #print('Could not find applicable stepsize, exiting...')
                    #sys.exit(-1) # Exit with error, could not get an accurate enough stepsize. Impossible to find solution numerically?
            
            (working_force), (drag_force), (grav_force) = self.rocket.total_working_force(self.time_increments[-1], self.planet, next_state[0], next_state[2], next_state[1], next_state[3])
            #print('next_time:', self.time_increments[-1] + self.stepsize)
            
            self.forces.append(working_force)
            self.masses.append(self.rocket.current_mass(self.time_increments[-1]))
            self.drags.append(drag_force)
            self.gravities.append(grav_force)
            self.thrusts.append(self.rocket.current_force(self.time_increments[-1]))
            self.current_state.append(next_state)
            self.time_increments.append(self.time_increments[-1] + self.stepsize)
        
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

    def error_tolerated(self, error, tolerance):
        return error < tolerance

    def calculate_error(self, fourth_order_solution, fifth_order_solution):
        # Error in next_step is found by subtraction next_step (fourt order) from zn (more accurate fifth order), 
        # and taking the absolute value (length) of the resulting vector.
        subtraced = self.subtract_vectors(fifth_order_solution, fourth_order_solution) # Partial calculation, not important
        error = self.absoulte_value(subtraced) # Error at this step
        return error
