import time
import argparse
import numpy as np
import motion
from naoqi import ALProxy
from Sonar import Sonar
#from Controler import Controler

def main(robotIP, port=9559):
    sonar = Sonar(robotIP, port)
    #controler = Controler(initialState)
    motionProxy = ALProxy("ALMotion", robotIP, port)
    postureProxy = ALProxy("ALRobotPosture", robotIP, port)
    frame = motion.FRAME_ROBOT # maybe test TORSO?

    # Get ready, NAO!
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)

    start_t = time.time()

    # Main loop
    while (time.time() - start_t <= 30):
        # make course corrections
        # async walk
        # little sleep

        # Sensor reading step
        theta_correction = 0;
        lread, rread = sonar.getSampleReading(n_readings=10)

        print("Sonar readings (lread, rread) = (%.2f, %.2f)" % (lread, rread))

        # Course correction decision step (theta is positive counterclockwise)
        if (lread < 0.4 and rread > 2.0):
            theta_correction = np.deg2rad(-30)
        elif (rread < 0.4 and lread > 2.0):
            theta_correction = np.deg2rad(+30)
        elif (lread < 0.4 and rread < 0.4):
            theta_correction = np.deg2rad(160) # yes, this is dumb

        # Course correction execution step
        motionProxy.moveToward(1.0, 0, theta_correction)

        time.sleep(0.5)

    # Stop motion
    motionProxy.stopMove()

    # Just to indicate we're finished
    motionProxy.rest()

    print("NAOvigation script finished.")


'''
Code for main program initialisation
'''
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number")

    args = parser.parse_args()

    main(args.ip, args.port)
