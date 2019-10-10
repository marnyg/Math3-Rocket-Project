import unittest
from Earth import Earth
from SaturnV import SaturnV
from RocketState import RocketState
import math

earth = Earth()
rocket = SaturnV()
starting_state = (0, earth.equator_radius, 0, 0) # (time=1, xpos=0, ypos=earth.equator_radius, xvel=0, yvel=0)
state = RocketState(rocket, earth, starting_state, stepsize=1)
class TestStringMethods(unittest.TestCase):


    def test(self):
        self.assertEqual(1,1)

    def testRocketMass(self):
        self.assertEqual(rocket.current_mass(0),2924400)
        self.assertEqual(rocket.current_mass(1),2911542.8571428573)
        self.assertEqual(rocket.current_mass(100),1638685.7142857143)
        self.assertEqual(rocket.current_mass(1100),4280)
    def testRocketCrosssection(self):
        self.assertEqual(rocket.current_crossection(0),10.1*math.pi)
        self.assertEqual(rocket.current_crossection(rocket.stage_1_firing_time),10.1*math.pi)
        self.assertEqual(rocket.current_crossection(rocket.stage_2_firing_time),10.1*math.pi)
        self.assertEqual(rocket.current_crossection(rocket.stage_3_firing_time),6.6*math.pi)
        self.assertEqual(rocket.current_crossection(rocket.stage_3_firing_time+10),6.6*math.pi)

    def testRocketAngleToOrigin(self):
        self.assertEqual(rocket.current_angle_to_origin(0,0), 3*math.pi/2)
        self.assertEqual(rocket.current_angle_to_origin(0,1), 3*math.pi/2)
        self.assertEqual(rocket.current_angle_to_origin(1,1), math.pi/4)
        self.assertEqual(rocket.current_angle_to_origin(1,0), 0)
        self.assertEqual(rocket.current_angle_to_origin(-1,-1), (5*math.pi/4)%math.pi)

    def testRocketVelocityAngle(self):
        self.assertEqual(rocket.current_velocity_angle(0,0), 3*math.pi/2)
        self.assertEqual(rocket.current_velocity_angle(0,1), 3*math.pi/2)
        self.assertEqual(rocket.current_velocity_angle(1,1), math.pi/4)
        self.assertEqual(rocket.current_velocity_angle(1,0), 0)
        self.assertEqual(rocket.current_velocity_angle(-1,-1), (-math.pi+math.pi/4))
        
    def testDecomposeVector(self):
        #self.assertEqual(rocket.decomposeVector(1,math.pi),(-1.0,0))
        x,y=rocket.decomposeVector(1,math.pi)
        self.assertAlmostEqual(x,-1)
        self.assertAlmostEqual(y,0)
        self.assertEqual(rocket.decomposeVector(1,0),(1.0,0))
        self.assertEqual(rocket.decomposeVector(2,0),(2.0,0))
        x,y=rocket.decomposeVector(math.sqrt(2**2+2**2),math.pi/4)
        self.assertAlmostEqual(x,2)
        self.assertAlmostEqual(y,2)

    def testPlanetGravAtDistance(self):
        self.assertEqual(1,2)

if __name__ == '__main__':
    unittest.main()

