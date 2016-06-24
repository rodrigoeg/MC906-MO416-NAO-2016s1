#include <iostream>
#include "nao.h"

extern "C" {
#include "extApi.h"
}

using namespace std;

void NAO::start(int clientID) {
    cout << "NAO started\n";

    int headHandle, vision1Handle;
    simxUChar *image;
    simxInt resolution[2] = {0,0};
    simxGetObjectHandle(clientID, "HeadYaw", &headHandle, simx_opmode_blocking);
    simxGetObjectHandle(clientID, "NAO_vision1", &vision1Handle, simx_opmode_blocking);
    simxGetVisionSensorImage(clientID, vision1Handle, resolution, &image, 0, simx_opmode_streaming);

    simxSetJointTargetPosition(clientID, headHandle, -1.0f, simx_opmode_oneshot);
    extApi_sleepMs(2000);
    simxGetVisionSensorImage(clientID, vision1Handle, resolution, &image, 0, simx_opmode_buffer);
    cout<< image << "\n";

    simxSetJointTargetPosition(clientID, headHandle, 1.0f, simx_opmode_oneshot);
    extApi_sleepMs(1000);
    simxGetVisionSensorImage(clientID, vision1Handle, resolution, &image, 0, simx_opmode_buffer);
    cout<< image << "\n";

    simxSetJointTargetPosition(clientID, headHandle, 0, simx_opmode_oneshot);
    extApi_sleepMs(1000);
    simxGetVisionSensorImage(clientID, vision1Handle, resolution, &image, 0, simx_opmode_buffer);
    cout<< image << "\n";
}
