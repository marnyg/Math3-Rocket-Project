import math

class SaturnV:
    def __init__(self):
        # Stage 1 variables
        self.stage_1_loaded_mass = 2290000 # kg
        self.stage_1_empty_mass = 130000 # kg
        self.stage_1_force = 35100 * 1000 # Newton
        self.stage_1_firing_time = 168 # seconds
        self.stage_1_fuel_consumption = (self.stage_1_loaded_mass - self.stage_1_empty_mass) / self.stage_1_firing_time # kg fuel pr. second, delta_m stage 1
        
        # Stage 2 variables
        self.stage_2_loaded_mass = 496200 # kg
        self.stage_2_empty_mass = 40100 # kg
        self.stage_2_force = 5141 * 1000 # Newton
        self.stage_2_firing_time = 360 # seconds
        self.stage_2_fuel_consumption = (self.stage_2_loaded_mass - self.stage_2_empty_mass) / self.stage_2_firing_time # kg fuel pr. second, delta_m stage 2

        # Stage 3 variables
        self.stage_3_loaded_mass = 123000 # kg
        self.stage_3_empty_mass = 13500 # kg
        self.stage_3_force = 1033.1 * 1000 # Newton
        self.stage_3_firing_time = 165 + 335 # seconds, two burns
        self.stage_3_fuel_consumption = (self.stage_3_loaded_mass - self.stage_3_empty_mass) / self.stage_3_firing_time # kg fuel pr. second, delta_m stage 3

        self.module_empty_mass = 4280 # kg standard load, 4920 kg extended load
        self.module_loaded_mass = 15200 # kg standard load, 16400 kg extended load

        self.total_loaded_mass = self.stage_1_loaded_mass + self.stage_2_loaded_mass + self.stage_3_loaded_mass + self.module_loaded_mass
        self.total_empty_mass = self.stage_1_empty_mass + self.stage_2_empty_mass + self.stage_3_empty_mass + self.module_empty_mass
        self.total_firing_time = self.stage_1_firing_time + self.stage_2_firing_time + self.stage_3_firing_time
        self.drag_coefficient = 0.515

    def current_force(self, time):
        if time <= self.stage_1_firing_time:
            # stage 1 is firing
            #print('stage 1, time: ' + str(time) + " force: ", self.stage_1_force)
            return self.stage_1_force
        elif time <= self.stage_1_firing_time + self.stage_2_firing_time:
            # stage 2 is firing
            #print('stage 2, time: ' + str(time) + " force: ", self.stage_2_force)
            return self.stage_2_force
        elif time <= self.stage_1_firing_time + self.stage_2_firing_time + self.stage_3_firing_time:
            # stage 3 is firing
            #print('stage 3, time: ' + str(time) + " force: ", self.stage_3_force)
            return self.stage_3_force
        else: 
            #print('No more fuel at time=', time)
            return 0 # no more fuel

    def exaust_gass_velocity(self, time):
        if time < self.total_firing_time:
            if time <= self.stage_1_firing_time:
                # stage 1 is firing
                return self.stage_1_force / ( -1 * self.stage_1_fuel_consumption )
            elif time <= self.stage_2_firing_time:
                # stage 2 is firing
                return self.stage_2_force / ( -1 * self.stage_2_fuel_consumption )
            else:
                # stage 3 is firing
                return self.stage_3_force / ( -1 * self.stage_3_fuel_consumption )
        else: 
            return 0 # no more fuel

    def current_mass(self, time):
        if time <= self.stage_1_firing_time:
            # stage 1 is firing
            current_stage_time = time # the stage has currently been firing for "current time after 0" - "all previous stages firing time"
            total_current_mass = self.total_loaded_mass - ( self.stage_1_fuel_consumption * current_stage_time )
            #print('stage 1, time: ' + str(time) + " mass: ", total_current_mass)
            return total_current_mass
        elif time <= self.stage_1_firing_time + self.stage_2_firing_time:
            # stage 2 is firing
            current_stage_time = time - self.stage_1_firing_time # the stage has currently been firing for "current time after 0" - "all previous stages firing time"
            total_current_mass = self.total_loaded_mass - ( self.stage_2_fuel_consumption * current_stage_time ) - self.stage_1_loaded_mass
            #print('stage 2, time: ' + str(time) + " mass: ", total_current_mass)
            return total_current_mass
        elif time <= self.stage_1_firing_time + self.stage_2_firing_time + self.stage_3_firing_time:
            # stage 3 is firing
            current_stage_time = time - self.stage_1_firing_time - self.stage_2_firing_time # the stage has currently been firing for "current time after 0" - "all previous stages firing time"
            total_current_mass = self.total_loaded_mass - ( self.stage_3_fuel_consumption * current_stage_time ) - self.stage_1_loaded_mass - self.stage_2_loaded_mass
            #print('stage 3, time: ' + str(time) + " mass: ", total_current_mass)
            return total_current_mass    
        else: 
            #print('All stages dropped, current mass is only of module')
            return self.module_empty_mass # all stages have been decoupled, only the mass of the landing module remains
            # should we use module_loaded_mass or the empty mass here?
    
    def current_acceleration(self, time):
        return self.current_force(time) / self.current_mass(time)

    def current_drag(self, planet, time, altitude, velocity):
        density_atmosphere = planet.atmosphere_density(altitude)
        drag = 1/2 * self.drag_coefficient * density_atmosphere * self.current_crossection(time) * velocity**2 
        return drag

    def current_crossection(self, time):
        if time < self.total_firing_time:
            if time <= self.stage_1_firing_time:
                # stage 1 is firing
                return 10.1 * math.pi
            elif time <= self.stage_2_firing_time:
                # stage 2 is firing
                return 10.1 * math.pi
            else:
                # stage 3 is firing
                return 6.6 * math.pi
        else: 
            return 6.6 * math.pi

    def current_angle_to_origin(self,previous_xpos,previous_ypos):
        return math.atan2(previous_ypos, previous_xpos)

    def current_velocity_angle(self,previous_xvel, previous_yvel):
        return math.atan2(previous_yvel, previous_xvel)

    def decomposeVector(self, vector, angle):
        x = vector * math.cos(angle)
        y = vector * math.sin(angle)
        return x,y

    def thrust_angle(self, time, xvel, yvel):
        #return 6 * math.pi / 8
        return math.pi / 4

    def total_working_force(self, time, planet, previous_xpos, previous_xvel, previous_ypos, previous_yvel):

        distance_to_surface = planet.distance_from_center(previous_xpos, previous_ypos) - planet.equator_radius
        distance_to_center = planet.distance_from_center(previous_xpos, previous_ypos) #math.sqrt(previous_xpos**2 + previous_ypos**2)
        # How big is the gravitational force?
        gravity = planet.gravitational_force(self.current_mass(time), distance_to_center)
        # We know gravity allways points towards the earth, earth is at (0, 0)
        # We know our position (x, y) relative to the earth
        # Gx = G cos(angle to origin), Gy = G sin(angle to origin) 
        # Angle to origin = atan(y/x) = atan (previous_ypos/ previous_xpos)

        thrustForce = self.current_force(time)
        
        angle_to_origin = self.current_angle_to_origin(previous_xpos, previous_ypos)
        gravAngle=angle_to_origin+math.pi
        gravx, gravy = self.decomposeVector(gravity, gravAngle)

        
        
        velocity_angle = self.current_velocity_angle(previous_xvel,previous_yvel)
        velAngleOffset=0
        velocity = math.sqrt(previous_xvel**2 + previous_yvel**2)
        velx,vely=self.decomposeVector(velocity, velocity_angle)

        dragAngle = velocity_angle+math.pi
        drag = self.current_drag(planet, time, distance_to_surface, velocity)
        dragx, dragy = self.decomposeVector(drag, dragAngle)

        thrust_angle = self.thrust_angle(time, previous_xvel, previous_yvel)
        thrustForcex,thrustForcey = self.decomposeVector(thrustForce, thrust_angle)

        '''
        if math.sin(velocity_angle) == -1:
            print('rocket going down!')
        if dragy > 0:
            print(time,'Drag is pointing upwards?!?!')
        if gravy > 0:
            print('Gravity is pointing upwards?!?!')
        '''
        #print('Forex:', thrustForcex)
        #print('dragx:', dragx)
        #print('gravx:', gravx)
        forcex = thrustForcex + dragx + gravx
        forcey = thrustForcey + dragy + gravy
        
        return (forcex, forcey, thrust_angle), (dragx, dragy,dragAngle), (gravx, gravy,gravAngle),(velx,vely,velocity_angle)
