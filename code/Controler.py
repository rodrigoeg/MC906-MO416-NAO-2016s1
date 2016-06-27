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
    sonar_interval = np.linspace(0.25, 2.25, 50)
    theta_interval = np.linspace(-1, 1, 50)

    # Internal variables (fuzzy stuff)
    lsonar = None
    rsonar = None
    theta = None
    system = None

    def __init__(self):
        # Create input and output variables
        self.lsonar = ctrl.Antecedent(sonar_interval, 'lsonar')
        self.rsonar = ctrl.Antecedent(sonar_interval, 'rsonar')
        self.theta = ctrl.Consequent(theta_interval, 'theta')

        # we need membership functions!
        var_names = ['low', 'mid', 'high']
        lsonar.automf(names=var_names)
        rsonar.automf(names=var_names)
        theta.automf(names=var_names) # using low/mid/high in this example

        # If you want a diferent/custom membership function:
        theta['low'] = mshp.gaussmf(theta_interval, 0, 0.02)

        # Here the rules are defined!
        # look at http://pythonhosted.org/scikit-fuzzy/auto_examples/plot_control_system_advanced.html#set-up-the-fuzzy-control-system
        # and http://pythonhosted.org/scikit-fuzzy/auto_examples/plot_tipping_problem_newapi.html
        # for good examples

        # Create the control system
        system = ctrl.ControlSystem(rules=[''' rule variables '''])

        # System is created, just create a simulation, input values and call compute()
        #sys_sim = ctrl.ControlSystemSimulation(system)
        #sys_sim['lsonar'] = 0
        #sys_sim['rsonar'] = 0
        #sys_sim.compute()
        #sys_sim.output['theta']
