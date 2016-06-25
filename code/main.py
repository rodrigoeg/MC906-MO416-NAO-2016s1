import math
import time
import argparse
from naoqi import ALProxy
import vrep

def main(robotIP, PORT=9559):
    vrep.simxFinish(-1)
    clientID=vrep.simxStart('127.0.0.1',20000,True,True,5000,5)
    if clientID!=-1:
        print 'Connected to remote API server'

    else:
        print 'Connection non successful'

    proximitySensor1 = vrep.simxGetObjectHandle(clientID,'Proximity_sensor1',vrep.simx_opmode_oneshot_wait)[1]
    proximitySensor2 = vrep.simxGetObjectHandle(clientID,'Proximity_sensor2',vrep.simx_opmode_oneshot_wait)[1]

    vrep.simxReadProximitySensor(clientID, proximitySensor1, vrep.simx_opmode_streaming);
    vrep.simxReadProximitySensor(clientID, proximitySensor2, vrep.simx_opmode_streaming);

    motionProxy  = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)

    # Wake up robot
    motionProxy.wakeUp()

    # Send robot to Pose Init
    postureProxy.goToPosture("StandInit", 0.5)

    # Example showing the moveTo command
    # The units for this command are meters and radians
    for count in range(0,10):
        x  = 1
        y  = 0
        theta  = 0
        motionProxy.move(x, y, theta)
        print "Sensor 1 - Left"
        print vrep.simxReadProximitySensor(clientID, proximitySensor1, vrep.simx_opmode_buffer);
        print "Sensor 2 - Right"
        print vrep.simxReadProximitySensor(clientID, proximitySensor2, vrep.simx_opmode_buffer);
        print ""
        time.sleep(1)

    # Go to rest position
    motionProxy.rest()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number")

    args = parser.parse_args()
    main(args.ip, args.port)
