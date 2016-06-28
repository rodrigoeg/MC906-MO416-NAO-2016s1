# This example can be found at http://pythonhosted.org/scikit-fuzzy/

import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import skfuzzy.membership as mshp
# plotting only
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Controler:
    # Variable intervals (greater the third parameter, better the resolution)
    sonar_interval = np.linspace(0.25, 2.55, 50)
    theta_interval = np.linspace(-1, 1, 50)

    # Internal variables (fuzzy stuff)
    lsonar = None
    rsonar = None
    theta = None
    system = None
    sys_sim = None

    def __init__(self):
        # Create input and output variables
        self.lsonar = ctrl.Antecedent(self.sonar_interval, 'lsonar')
        self.rsonar = ctrl.Antecedent(self.sonar_interval, 'rsonar')
        self.theta = ctrl.Consequent(self.theta_interval, 'theta')

        # we need membership functions!
        var_names = ['low', 'mid', 'high']
        var_names_theta = ['left', 'middle', 'right']
        self.lsonar.automf(names=var_names)
        self.rsonar.automf(names=var_names)
        self.theta.automf(names=var_names_theta)

        # If you want a different/custom membership function:
        #self.theta['low'] = mshp.gaussmf(self.theta_interval, 0, 0.02)

        # Here the rules are defined!
        # look at http://pythonhosted.org/scikit-fuzzy/auto_examples/plot_control_system_advanced.html#set-up-the-fuzzy-control-system
        # and http://pythonhosted.org/scikit-fuzzy/auto_examples/plot_tipping_problem_newapi.html
        # for good examples
        rule1 = ctrl.Rule(antecedent=(self.lsonar['low'] & ~ self.rsonar['low']),
                          consequent=self.theta['left'],
                          label='rule left')
        rule2 = ctrl.Rule(antecedent=(~ self.lsonar['low'] & self.rsonar['low']),
                          consequent=self.theta['right'],
                          label='rule right')
        rule3 = ctrl.Rule(antecedent=(self.lsonar['mid'] & self.rsonar['mid']),
                          consequent=self.theta['middle'],
                          label='rule middle')

        # Create the control system
        self.system = ctrl.ControlSystem(rules=[rule1, rule2, rule3])

        # System is created, just create a simulation, input values and call compute()
        self.sys_sim = ctrl.ControlSystemSimulation(self.system)

    def compute(self, lread=0, rread=0):
        self.sys_sim.input['lsonar'] = lread
        self.sys_sim.input['rsonar'] = rread
        self.sys_sim.compute()
        return self.sys_sim.output['theta']
