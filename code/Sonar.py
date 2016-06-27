# This exports the env variable in case I forget
#import os
#os.system("export PYTHONPATH=`echo ~/pynaoqi-python2.7-2.1.4.13-linux64/`")

import numpy as np
from naoqi import ALProxy, ALBroker

class Sonar:
    """
    Wrapper for Sonar sensors
    Let v be the value of the first echo:
        v = 0 => an error has occurred
        v = Max Detection Distance => no echo
        v = 0.40 => could be the ground!
    Let d be the measured distance:
        d < 0.25 => real distance is unknown
        d > 0.80 => d is considered a rough estimate (up to 2.25 m, the max range)
    The sensor resolution is 0.01-0.04 metres.
    Events for the ALSonar are:
        - SonarLeftDetected
        - SonarRightDetected
        - SonarLeftNothingDetected
        - SonarRightNothingDetected
    """
    # Constants
    __left_sonar_addr = "Device/SubDeviceList/US/Left/Sensor/Value"
    __right_sonar_addr = "Device/SubDeviceList/US/Right/Sensor/Value"

    # Internal variables
    server_addr = ""
    server_port = 0
    sonar_proxy = None
    mem_proxy = None

    def __init__(self, serverAddr, serverPort):
        self.server_addr = serverAddr
        self.server_port = serverPort

        self.sonar_proxy = ALProxy("ALSonar", serverAddr, serverPort)

        # ubscription name, period in ms precision
        self.sonar_proxy.subscribe("NAONAONAO", 30, 1.0)

        self.mem_proxy = ALProxy("ALMemory", serverAddr, serverPort)

    def getReading(self):
        """
        Returns a list with 2 items inside: each one containing the number of
        requested readings from left and right sensors.
        """

        return (self.mem_proxy.getData(self.__left_sonar_addr), self.mem_proxy.getData(self.__right_sonar_addr))

    def getSampleReading(self, n_readings=1):
        """
        The return has the same format as getReading, but every number now is 
        the mean of n_readings. When n_readings is 1, this method is equivalent 
        to getReading.
        """

        # Aggregator variable (cheaper than stacking all readings in memory)
        aggr = np.array(self.getReading())

        for k in range(n_readings-1):
            aggr = aggr + np.array(self.getReading())

        aggr = aggr / n_readings

        return aggr
