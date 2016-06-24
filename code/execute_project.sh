#!/bin/bash
PYNAOQI_PATH=~/pynaoqi-python2.7-2.1.2.17-linux64

export PYTHONPATH=${PYTHONPATH}:${PYNAOQI_PATH}
export DYLD_LIBRARY_PATH=${DYLD_LIBRARY_PATH}:${PYNAOQI_PATH}



python main.py