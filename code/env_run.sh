#!/bin/bash
PYNAOQI_PATH=~/pynaoqi-python2.7-2.1.4.13-linux64
CHROREGRAPHE_PATH=~/choregraphe-suite-2.1.4.13-linux64
WEBOTS_PATH=~/webots
PYTHON_NAME=python2

export PYTHONPATH=${PYTHONPATH}:${PYNAOQI_PATH}
export DYLD_LIBRARY_PATH=${DYLD_LIBRARY_PATH}:${PYNAOQI_PATH}
export WEBOTS_HOME=${WEBOTS_PATH}

#$CHROREGRAPHE_PATH/bin/naoqi-bin -p 9559 &

YELLOW='\033[1;33m'
NC='\033[0m'
printf "${YELLOW}Use this as ./env_run.sh file.py.\n"
printf "If used without a py script, it will open the interpreter, which is also useful :P\n${NC}"

${PYTHON_NAME} $1
