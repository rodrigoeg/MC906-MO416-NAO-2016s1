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

    # Start walking (sonar appears to start reading correct values only after this)
    motionProxy.moveToward(0.01, 0, 0)
    time.sleep(0.5)

    # Main loop
    while (time.time() - start_t <= 30):
        # make course corrections
        # async walk
        # little sleep

        # Sensor reading step
        x_velocity = 1
        y_velocity = 0
        theta_correction = 0

        lread, rread = sonar.getSampleReading(n_readings=10)

        print("Sonar readings (lread, rread) = (%.2f, %.2f)" % (lread, rread))

        # Course correction decision step (theta is positive counterclockwise)
        if (lread < 0.4 and rread > 1.0):
            theta_correction = np.deg2rad(-20)
            x_velocity = 0
        elif (rread < 0.4 and lread > 1.0):
            theta_correction = np.deg2rad(+20)
            x_velocity = 0
        elif (lread < 0.4 and rread < 0.4):
            if lread < rread:
                theta_correction = np.deg2rad(-55)
            else:
                theta_correction = np.deg2rad(+55)
            x_velocity = 0

        print("Theta %.2f" % theta_correction)

        # Course correction execution step
        motionProxy.moveToward(x_velocity, y_velocity, theta_correction)

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
