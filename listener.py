from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from socketIO_client import BaseNamespace
from socketIO_client import LoggingNamespace
from socketIO_client import SocketIO

from subprocess import Popen, PIPE

import os
import signal
import sys


INPUT_URI='http://ec2-52-24-126-225.us-west-2.compute.amazonaws.com'
INPUT_PORT=81
verbose=True
mission_number = ""
roslauch_process = None

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

  @run_once
  def on_cminitializemission(self, *args):
    global roslauch_process
    counter=0

    def run_roslaunch(self, message):
      global roslauch_process
      #test_cmd = 'echo hello'
      cmd = 'roslaunch multirobot {}.launch'.format(message)
      roslauch_process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True, preexec_fn=os.setsid)
      
      for line in roslauch_process.stdout:
        if verbose: print(line)

        if "odom received!" in line:
          self.emit('initialized', "{} initialized!")
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
      

      message_emit = "Control & Mapping: ", switch_case.get(message, "received a message, but the message did not match the expected format of mission#.")
      
      if len(message_emit) < 60:
          self.emit('cminitializemission', 'Initializing gazebo environment')       
          run_roslaunch(self, message)
      else: 
          self.emit('cminitializemission', message_emit)

    if counter == 0:
        check_switch_case(self, args[0])
        counter+=1

  @run_once
  def on_cmstopmission(self, *args):
    global roslauch_process
    os.killpg(os.getpgid(roslauch_process.pid), signal.SIGTERM)

    poll = roslauch_process.poll()
    if poll == None:
      print('Subprocess is still alive')
    else:
      print('Subprocess is dead')

    sys.exit(0)


class Listener(object):

  def __init__(self, URI, PORT):
    self.URI = URI
    self.PORT = PORT

  def test(*args):
      print("Mission Initialized!")

  def listen(self):
    print('Listening on {} with port {}'.format(INPUT_URI, INPUT_PORT))
    socketio = SocketIO(INPUT_URI, INPUT_PORT, LoggingNamespace)
    io = socketio.define(Namespace, '/socket.io')

    while True:
      socketio.wait(seconds=1)    


if __name__ == "__main__":
  listener = Listener(INPUT_URI, INPUT_PORT)
  listener.listen()
