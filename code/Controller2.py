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
    sonar_interval = np.linspace(0.25, 2.25, 51)
    theta_interval = np.linspace(-1, 1, 51)
    v_interval = np.linspace(0, 1, 21)

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
        var_names = ['low', 'mid', 'high']
        var_names_theta = ['left', 'middle', 'right']

        self.lsonar.automf(names=var_names)
        self.rsonar.automf(names=var_names)
        self.theta.automf(names=var_names_theta)
        self.v_x.automf(names=var_names)

        low_mshp = mshp.trapmf(self.sonar_interval, [0.25, 0.25, 0.5, 1.0])
        mid_mshp = mshp.gaussmf(self.sonar_interval, 1.25, 0.25)
        high_mshp = mshp.trapmf(self.sonar_interval, [1.5, 2.0, 2.25, 2.25])

        self.lsonar['low'] = low_mshp
        self.lsonar['mid'] = mid_mshp
        self.lsonar['high'] = high_mshp

        self.rsonar['low'] = low_mshp
        self.rsonar['mid'] = mid_mshp
        self.rsonar['high'] = high_mshp
        
        self.theta['left'] = mshp.gaussmf(self.theta_interval, 1.0, 0.2)
        self.theta['middle'] = mshp.gaussmf(self.theta_interval, 0, 0.6)
        self.theta['right'] = mshp.gaussmf(self.theta_interval, -1.0, 0.2)

        self.v_x['low'] = mshp.gaussmf(self.v_interval, 0, 0.2)
        self.v_x['mid'] = mshp.gaussmf(self.v_interval, 0.5, 0.3)
        self.v_x['high'] = mshp.gaussmf(self.v_interval, 1, 0.2)

        # Here the rules are defined!
        # look at http://pythonhosted.org/scikit-fuzzy/auto_examples/plot_control_system_advanced.html#set-up-the-fuzzy-control-system
        # and http://pythonhosted.org/scikit-fuzzy/auto_examples/plot_tipping_problem_newapi.html
        # for good examples
        rules = []

        rules.append(ctrl.Rule(label="lowlow", 
                               antecedent=(self.lsonar['low'] & self.rsonar['low']), 
                               consequent=(self.v_x['low'])))
        rules.append(ctrl.Rule(label="lowmid", 
                               antecedent=(self.lsonar['low'] & self.rsonar['mid']), 
                               consequent=(self.theta['right'], self.v_x['mid'])))
        rules.append(ctrl.Rule(label="lowhigh", 
                               antecedent=(self.lsonar['low'] & self.rsonar['high']), 
                               consequent=(self.theta['right'], self.v_x['low'])))
        rules.append(ctrl.Rule(label="midlow", 
                               antecedent=(self.lsonar['mid'] & self.rsonar['low']), 
                               consequent=(self.theta['left'], self.v_x['mid'])))
        rules.append(ctrl.Rule(label="midmid", 
                               antecedent=(self.lsonar['mid'] & self.rsonar['mid']), 
                               consequent=(self.theta['middle'], self.v_x['mid'])))
        rules.append(ctrl.Rule(label="midhigh", 
                               antecedent=(self.lsonar['mid'] & self.rsonar['high']), 
                               consequent=(self.theta['right'], self.v_x['high'])))
        rules.append(ctrl.Rule(label="highlow", 
                               antecedent=(self.lsonar['high'] & self.rsonar['low']), 
                               consequent=(self.theta['left'], self.v_x['low'])))
        rules.append(ctrl.Rule(label="highmid", 
                               antecedent=(self.lsonar['high'] & self.rsonar['mid']), 
                               consequent=(self.theta['left'], self.v_x['high'])))
        rules.append(ctrl.Rule(label="highhigh", 
                               antecedent=(self.lsonar['high'] & self.rsonar['high']), 
                               consequent=(self.theta['middle'], self.v_x['high'])))

        # Create the control system
        self.system = ctrl.ControlSystem(rules=rules)

        # System is created, just create a simulation, input values and call compute()
        self.sim = ctrl.ControlSystemSimulation(self.system)
        
    def compute(self, lread=0, rread=0):
        self.sim.input['lsonar'] = lread
        self.sim.input['rsonar'] = rread

        self.sim.compute()
        
        return (self.sim.output['theta'], self.sim.output['v_x'])

