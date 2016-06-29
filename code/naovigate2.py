import time
import argparse
import numpy as np
import motion
from naoqi import ALProxy
from Sonar import Sonar
from Controller2 import Controller
#from Controler import Controler

def main(robotIP, port=9559):
    sonar = Sonar(robotIP, port)
    controler = Controller()
    motionProxy = ALProxy("ALMotion", robotIP, port)
    postureProxy = ALProxy("ALRobotPosture", robotIP, port)
    frame = motion.FRAME_ROBOT # maybe test TORSO?
    last_theta = 0
    memory_factor = 0.3

    # Get ready, NAO!
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)

    start_t = time.time()

    # Start walking (sonar appears to start reading correct values only after this)
    motionProxy.moveToward(0.01, 0, 0)
    time.sleep(0.5)

    # Main loop
    while (time.time() - start_t <= 180):
        # Sensor reading step
        x_velocity = 1
        y_velocity = 0
        theta_correction = 0

        lread, rread = sonar.getSampleReading(n_readings=10)

        # Course correction decision step (theta is positive counterclockwise)
        print("Sonar readings (lread, rread) = (%.2f, %.2f)" % (lread, rread))
        theta_correction, v_correction = controler.compute(lread=lread, rread=rread, last_theta=last_theta)
        print("Theta %.2f; Velocity %.2f" % (theta_correction, v_correction))

        # Course correction execution step
        #motionProxy.moveToward(v_correction, y_velocity, theta_correction)
        motionProxy.moveToward(v_correction, y_velocity, (memory_factor * last_theta + (1 - memory_factor) * theta_correction))

        last_theta = theta_correction

        time.sleep(0.5)

    # Stop motion
    motionProxy.moveToward(0, 0, 0) # I found this to be less motion breaking
    motionProxy.stopMove()
    postureProxy.goToPosture("standInit", 0.2) # make him stand again

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
