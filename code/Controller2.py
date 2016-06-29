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
    sonar_interval = np.linspace(0.25, 2.25, 101)
    theta_interval = np.linspace(-1, 1, 101)
    v_interval = np.linspace(0, 1, 101)

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
        self.theta = ctrl.Consequent(self.theta_interval, 'theta')
        self.v_x = ctrl.Consequent(self.v_interval, 'v_x')

        # we need membership functions!
        distance_levels = ['dangerous', 'unsafe', 'safe']
        theta_directions = ['left', 'middle', 'right']
        velocity_levels = ['slow', 'medium', 'fast']

        self.lsonar.automf(names=distance_levels)
        self.rsonar.automf(names=distance_levels)
        self.theta.automf(names=theta_directions)
        self.v_x.automf(names=velocity_levels)

        low_mshp = mshp.trapmf(self.sonar_interval, [0.25, 0.25, 0.3, 0.4])
        mid_mshp = mshp.gaussmf(self.sonar_interval, 0.45, 0.15)
        high_mshp = mshp.trapmf(self.sonar_interval, [0.5, 0.8, 2.55, 2.55])

        self.lsonar['dangerous'] = low_mshp
        self.lsonar['unsafe'] = mid_mshp
        self.lsonar['safe'] = high_mshp

        self.rsonar['dangerous'] = low_mshp
        self.rsonar['unsafe'] = mid_mshp
        self.rsonar['safe'] = high_mshp
        
        self.theta['left'] = mshp.gaussmf(self.theta_interval, 1.0, 0.45)
        self.theta['middle'] = mshp.gaussmf(self.theta_interval, 0, 0.5)
        self.theta['right'] = mshp.gaussmf(self.theta_interval, -1.0, 0.3)

        self.v_x['slow'] = mshp.trimf(self.v_interval, [0, 0, 0.4])
        self.v_x['medium'] = mshp.gaussmf(self.v_interval, 0.6, 0.1)
        self.v_x['fast'] = mshp.trapmf(self.v_interval, [0.8, 0.98, 1.0, 1.0])

        # Here the rules are defined!
        # look at http://pythonhosted.org/scikit-fuzzy/auto_examples/plot_control_system_advanced.html#set-up-the-fuzzy-control-system
        # and http://pythonhosted.org/scikit-fuzzy/auto_examples/plot_tipping_problem_newapi.html
        # for good examples
        rules = []

        # this first rule needs a way to choose theta
        rules.append(ctrl.Rule(label="lowlow", 
                               antecedent=(self.lsonar['dangerous'] & self.rsonar['dangerous']), 
                               consequent=(self.v_x['slow'])))
        rules.append(ctrl.Rule(label="lowmid", 
                               antecedent=(self.lsonar['dangerous'] & self.rsonar['unsafe']), 
                               consequent=(self.theta['right'], self.v_x['medium'])))
        rules.append(ctrl.Rule(label="lowhigh", 
                               antecedent=(self.lsonar['dangerous'] & self.rsonar['safe']), 
                               consequent=(self.theta['right'], self.v_x['medium'])))

        rules.append(ctrl.Rule(label="midlow", 
                               antecedent=(self.lsonar['unsafe'] & self.rsonar['dangerous']), 
                               consequent=(self.theta['left'], self.v_x['medium'])))
        rules.append(ctrl.Rule(label="midmid", 
                               antecedent=(self.lsonar['unsafe'] & self.rsonar['unsafe']), 
                               consequent=(self.theta['middle'], self.v_x['fast'])))
        rules.append(ctrl.Rule(label="midhigh", 
                               antecedent=(self.lsonar['unsafe'] & self.rsonar['safe']), 
                               consequent=(self.theta['right'], self.v_x['fast'])))

        rules.append(ctrl.Rule(label="highlow", 
                               antecedent=(self.lsonar['safe'] & self.rsonar['dangerous']), 
                               consequent=(self.theta['left'], self.v_x['medium'])))
        rules.append(ctrl.Rule(label="highmid", 
                               antecedent=(self.lsonar['safe'] & self.rsonar['unsafe']), 
                               consequent=(self.theta['left'], self.v_x['fast'])))
        rules.append(ctrl.Rule(label="highhigh", 
                               antecedent=(self.lsonar['safe'] & self.rsonar['safe']), 
                               consequent=(self.theta['middle'], self.v_x['fast'])))

        # Create the control system
        self.system = ctrl.ControlSystem(rules=rules)

        # System is created, just create a simulation, input values and call compute()
        self.sim = ctrl.ControlSystemSimulation(self.system)
        
    def compute(self, lread=0, rread=0):
        self.sim.input['lsonar'] = lread
        self.sim.input['rsonar'] = rread

        self.sim.compute()
        
        return (self.sim.output['theta'], self.sim.output['v_x'])

