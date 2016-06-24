#!/bin/bash
PYNAOQI_PATH=~/pynaoqi-python2.7-2.1.2.17-linux64
CHROREGRAPHE_PATH=~/choregraphe-suite-2.1.4.13-linux64



export PYTHONPATH=${PYTHONPATH}:${PYNAOQI_PATH}
export DYLD_LIBRARY_PATH=${DYLD_LIBRARY_PATH}:${PYNAOQI_PATH}

$CHROREGRAPHE_PATH/bin/naoqi-bin -p 9559 &

cd NAO-control/
python single_nao_control.py <(echo 127.0.0.1) <(echo 9559)
