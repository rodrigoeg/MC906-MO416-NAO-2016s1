#Installation

- Download Webots for NAO (tested with version 8.2.1): https://community.ald.softbankrobotics.com/en/resources/software/language/en-gb
- Install NAOqi Python SDK (tested with version pynaoqi-python2.7-2.1.4.13): http://doc.aldebaran.com/2-1/dev/python/install_guide.html
- Execute "pip install -r requirements.txt" to download the Python project dependencies

#Quickstart

Configure the paths in env_run.sh and etup_naoqi.sh


Load the scene in Webots and start the simulation


Execute naoqi:

./setup_naoqi.sh


Execute the project:

./env_run.sh filename.py
