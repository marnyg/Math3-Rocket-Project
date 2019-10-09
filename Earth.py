import sys
import math
class Earth:
    def __init__(self):
        self.equator_diameter = 12756.28 * 1000 # meters
        self.pole_diameter = 12713.56 * 1000 # meters
        self.equator_radius = self.equator_diameter / 2
        self.mass = 5.9736 * 10**24 # kg
        self.rotation_period = 23.934 / (60 * 60) # roations per second
        self.G = 6.67428 * 10**-11
        self.troposphere = (0, 11000)
        self.lower_stratosphere = (self.troposphere[1], 25000)
        self.upper_stratosphere = (self.lower_stratosphere[1], 60000)

    def gravitational_force(self, object_mass, distance):
        if distance != 0:
            return self.G * self.mass * object_mass / distance**2
        else: 
            return self.G * self.mass * object_mass / sys.float_info.min**2 # smallest possible non zero float value
            #return object_mass * 9.81

    def atmosphere_density(self, altitude):
        return ( self.__pressure__(altitude) / self.__airtemp__(altitude) ) * 3.4855 / 1000
        
    def __airtemp__(self, altitude): # returns air temperature (in kelvin) at altitude (in meters) 
        if altitude <= self.troposphere[1]:
            # Troposphere
            return 288.19 - (0.00649 * altitude)
        elif altitude < self.lower_stratosphere[1]: 
            # Lower stratosphere
            return 216.69 # constant
        else:
            # Upper stratoshpere
            return 141.94 + (0.00299 * altitude)

    def __pressure__(self, altitude): # Returns pressure (in Pa (not kPa)) at altitude (in meters)
        if altitude <= self.troposphere[1]:
            # Troposphere
            return 101.29 * 1000 * (self.__airtemp__(altitude) / 288.08)**5.256
        elif altitude < self.lower_stratosphere[1]: 
            # Lower stratosphere
            return 127.76 * 1000 * (math.exp(-0.000157 * altitude)) # constant
        else:
            # Upper stratoshpere
            return 2.488 * 1000 * (self.__airtemp__(altitude)/216.6)**-11.388
          
    def distance_from_center(self, objectx, objecty):
        return math.sqrt(objectx**2 + objecty**2)
