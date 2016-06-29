# This example can be found at http://pythonhosted.org/scikit-fuzzy/

import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import skfuzzy.membership as mshp
# plotting only
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Controller:
    # Variable intervals (greater the third parameter, better the resolution)
    sonar_interval = np.linspace(0.25, 2.55, 201)
    theta_interval = np.linspace(-1, 1, 121)
    v_interval = np.linspace(0, 1, 101)

    # TODO: add previous theta (which starts as 0)

    # Internal variables (fuzzy stuff)
    lsonar = None
    rsonar = None
    theta = None
    v_x = None
    system = None
    sim = None

    def __init__(self):
        # Create input and output variables
        self.lsonar = ctrl.Antecedent(self.sonar_interval, 'lsonar')
        self.rsonar = ctrl.Antecedent(self.sonar_interval, 'rsonar')
        self.last_theta = ctrl.Antecedent(self.theta_interval, 'last_theta')
        self.theta = ctrl.Consequent(self.theta_interval, 'theta')
        self.v_x = ctrl.Consequent(self.v_interval, 'v_x')

        # we need membership functions!
        distance_levels = ['dangerous', 'unsafe', 'safe']
        theta_directions = ['left', 'centre', 'right']
        velocity_levels = ['slow', 'medium', 'fast']

        self.lsonar.automf(names=distance_levels)
        self.rsonar.automf(names=distance_levels)
        self.last_theta.automf(names=theta_directions)
        self.theta.automf(names=theta_directions)
        self.v_x.automf(names=velocity_levels)

        low_mshp = mshp.trimf(self.sonar_interval, [0.25, 0.25, 0.31])
        mid_mshp = mshp.trimf(self.sonar_interval, [0.28, 0.35, 0.45])
        high_mshp = mshp.trapmf(self.sonar_interval, [0.4, 0.6, 2.55, 2.55])

        self.lsonar['dangerous'] = low_mshp
        self.lsonar['unsafe'] = mid_mshp
        self.lsonar['safe'] = high_mshp

        self.rsonar['dangerous'] = low_mshp
        self.rsonar['unsafe'] = mid_mshp
        self.rsonar['safe'] = high_mshp

        left_angle_mshp = mshp.gaussmf(self.theta_interval, 0.7, 0.2)
        centre_angle_mshp = mshp.gaussmf(self.theta_interval, 0, 0.1)
        right_angle_mshp = mshp.gaussmf(self.theta_interval, -0.7, 0.2)
        
        self.theta['left'] = left_angle_mshp
        self.theta['centre'] = centre_angle_mshp
        self.theta['right'] = right_angle_mshp

        self.last_theta['left'] = left_angle_mshp
        self.last_theta['centre'] = centre_angle_mshp
        self.last_theta['right'] = right_angle_mshp

        self.v_x['slow'] = mshp.trimf(self.v_interval, [0, 0, 0.32])
        self.v_x['medium'] = mshp.gaussmf(self.v_interval, 0.5, 0.36)
        self.v_x['fast'] = mshp.trapmf(self.v_interval, [0.75, 0.95, 1.0, 1.0])

        # Here the rules are defined!
        # look at http://pythonhosted.org/scikit-fuzzy/auto_examples/plot_control_system_advanced.html#set-up-the-fuzzy-control-system
        # and http://pythonhosted.org/scikit-fuzzy/auto_examples/plot_tipping_problem_newapi.html
        # for good examples
        rules = []

        # Sonars are NOT dangerous, go fast and forward
        rules.append(ctrl.Rule(label="FastAndForward", 
                               antecedent=(~self.lsonar['dangerous'] & ~self.rsonar['dangerous']), 
                               consequent=(self.theta['centre'], self.v_x['fast'])))

        # Right sonar reads dangerous, left does not, steer left
        rules.append(ctrl.Rule(label="SteerLeftCaution", 
                               antecedent=(~self.lsonar['dangerous'] & self.rsonar['dangerous']), 
                               consequent=(self.theta['left'], self.v_x['slow'])))
        # Left sonar reads dangerous, right does not, steer left
        rules.append(ctrl.Rule(label="SteerRightCaution", 
                               antecedent=(self.lsonar['dangerous'] & ~self.rsonar['dangerous']), 
                               consequent=(self.theta['right'], self.v_x['slow'])))

        # Right sonar is NOT safe, left reads safe, turn left full speed
        rules.append(ctrl.Rule(label="SteerLeftReckless", 
                               antecedent=(self.lsonar['safe'] & ~self.rsonar['safe']), 
                               consequent=(self.theta['left'], self.v_x['fast'])))
        # Left sonar is NOT safe, right reads safe, turn right full speed
        rules.append(ctrl.Rule(label="SteerRightReckless", 
                               antecedent=(~self.lsonar['safe'] & self.rsonar['safe']), 
                               consequent=(self.theta['right'], self.v_x['fast'])))

        # Left sonar is NOT dangerous and right is NOT safe, turn left medium speed
        rules.append(ctrl.Rule(label="SteerLeftWatchSpeed", 
                               antecedent=(~self.lsonar['dangerous'] & ~self.rsonar['safe']), 
                               consequent=(self.theta['left'], self.v_x['medium'])))
        # Right sonar is NOT dangerous and left is NOT safe, turn right medium speed
        rules.append(ctrl.Rule(label="SteerRightWatchSpeed", 
                               antecedent=(~self.lsonar['safe'] & ~self.rsonar['dangerous']), 
                               consequent=(self.theta['right'], self.v_x['medium'])))

        # Last theta was right, right sonar is dangerous, turn left slow speed
        rules.append(ctrl.Rule(label="SteerLeftMedSpeed", 
                               antecedent=(self.rsonar['dangerous'] & self.last_theta['right']), 
                               consequent=(self.theta['left'], self.v_x['medium'])))
        # Last theta was left, left sonar is dangerous, turn right slow speed
        rules.append(ctrl.Rule(label="SteerRightMedSpeed", 
                               antecedent=(self.lsonar['dangerous'] & self.last_theta['left']), 
                               consequent=(self.theta['right'], self.v_x['medium'])))

        # Last theta was left, rsonar reads not dangerous, turn centre, full speed
        rules.append(ctrl.Rule(label="OutOfDangerFromLeft", 
                               antecedent=(~self.rsonar['dangerous'] & self.last_theta['left']), 
                               consequent=(self.theta['centre'], self.v_x['fast'])))
        # Last theta was right, lsonar reads not dangerous, turn centre, full speed
        rules.append(ctrl.Rule(label="OutOfDangerFromRight", 
                               antecedent=(~self.lsonar['dangerous'] & self.last_theta['right']), 
                               consequent=(self.theta['centre'], self.v_x['fast'])))

        # Create the control system
        self.system = ctrl.ControlSystem(rules=rules)

        # System is created, just create a simulation, input values and call compute()
        self.sim = ctrl.ControlSystemSimulation(self.system)
        
    def compute(self, lread=0, rread=0, last_theta=0):
        self.sim.input['lsonar'] = lread
        self.sim.input['rsonar'] = rread
        self.sim.input['last_theta'] = last_theta

        self.sim.compute()
        
        return (self.sim.output['theta'], self.sim.output['v_x'])

