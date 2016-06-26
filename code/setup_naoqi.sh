#!/bin/bash

NAOQI_PATH=~/.local/share/Cyberbotics/Webots/8.2/projects/robots/aldebaran/aldebaran/simulator-sdk

function kill_naoqi {
	echo "Killing naoqi"
    pkill naoqi
}

# Kills naoqi if we ctrl+c this script
trap kill_naoqi SIGINT

# Will run at port 9559
cd ${NAOQI_PATH}
./naoqi
