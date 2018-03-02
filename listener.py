from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from socketIO_client import BaseNamespace
from socketIO_client import LoggingNamespace
from socketIO_client import SocketIO

from subprocess import Popen, PIPE
import shlex
import time

#added
import os
import signal 
import sys


# INPUT_URI='http://ec2-52-24-126-225.us-west-2.compute.amazonaws.com'
INPUT_URI='http://192.168.1.11'
# INPUT_PORT=81
INPUT_PORT=8000
verbose=True
mission_number = ""
roslaunch_process = None

class Namespace(BaseNamespace):

  def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper

  def on_cmstartmission(self, *args):
    print('Starting {}'.format(args[0]))

  def on_tester(self, *args):
    print('test: ', args)

  def on_cminitializemission(self, *args):
    global roslaunch_process
    counter=0

    def run_roslaunch(self, message):
        global roslaunch_process

        self.emit('initialized', "{} initialized!".format(message))
        print('attempting roslaunch')

        station4_cmd = 'gnome-terminal -x xterm -e roslaunch multirobot run_mission.launch mission_string:={};'.format(message)
        
        roslaunch_process = Popen(station4_cmd, stdout=PIPE, stderr=PIPE, shell=True, preexec_fn=os.setsid)
        
        for line in roslaunch_process.stdout:
          if verbose: print(line)

          if "odom received!" in line:
            
            break

    def check_switch_case(self, message):
        global mission_number

        switch_case = {
          "mission1": "mission1 initialized",
          "mission2": "mission2 initialized",
          "mission3": "mission3 initialized",
          "mission4": "mission4 initialized",
          "mission5": "mission5 initialized"
        }
        

        message_emit = "[INFO] Control & Mapping: ", switch_case.get(message, "received a message, but the message did not match the expected format of mission#.")
        
        if len(message_emit) < 60:
            self.emit('cm-initialize-mission', 'Initializing gazebo environment')       
            run_roslaunch(self, message)
        else: 
            self.emit('cm-initialize-mission', message_emit)

    check_switch_case(self, args[0])

  def on_cmstopmission(self, *args):
    global roslaunch_process
    print('killing package')
    os.system('killall xterm')

    poll = roslaunch_process.poll()

    if poll == None:
      print('Subprocess is still alive')
    else:
      print('Subprocess is dead')

    os.system('killall -9 roscore; killall -9 rosmaster')


class Listener(object):

  def __init__(self, URI, PORT):
    self.URI = URI
    self.PORT = PORT

  def test(*args):
      print("Mission Initialized!")

  def listen(self):
    print('Listening on {} with port {}'.format(INPUT_URI, INPUT_PORT))
    print('Waiting for \'mission#\' on port')
    socketio = SocketIO(INPUT_URI, INPUT_PORT, LoggingNamespace)
    io = socketio.define(Namespace, '/socket.io')

    while True:
      socketio.wait(seconds=1)    
      #print('wait')


if __name__ == "__main__":
  listener = Listener(INPUT_URI, INPUT_PORT)
  listener.listen()
