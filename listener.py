from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from socketIO_client import BaseNamespace
from socketIO_client import LoggingNamespace
from socketIO_client import SocketIO

from subprocess import Popen, PIPE


INPUT_URI='http://ec2-52-24-126-225.us-west-2.compute.amazonaws.com'
INPUT_PORT=81

class Namespace(BaseNamespace):

  def run_roslaunch(self, mission_number):
    roslauch_process = Popen(['roslaunch', 'multirobot', '{}.launch'.format(mission_number)], stdout=PIPE, stderr=PIPE)
    
    for line in roslaunch.stdout:
      if "odom received!" in line:
        self.emit('initialized', "{} initialized!")
        break

  def on_cmstartmission(self, *args):
    print('Starting {}'.format(args[0]))

  def on_tester(self, *args):
    print('test: ', args)

  def on_cminitializemission(self, *args):
    switch_case = {
      "mission1": "mission1 initialized",
      "mission2": "mission2 initialized",
      "mission3": "mission3 initialized",
      "mission4": "mission4 initialized",
      "mission5": "mission5 initialized"
    }

    mission_number = "Control & Mapping: ", switch_case.get(args[0], "received a message, but the message did not match the expected format.")
    print("Running roslaunch file (test)")
    #run_roslaunch(mission_number)

    self.emit('initialized', mission_number)

  def on_something(self, *args):
    print(args)
    

class Listener(object):

  def __init__(self, URI, PORT):
    self.URI = URI
    self.PORT = PORT

  def test(*args):
      print("Mission Initialized!")

  def listen(self):

    socketio = SocketIO('http://ec2-52-24-126-225.us-west-2.compute.amazonaws.com', 81, LoggingNamespace)
    io = socketio.define(Namespace, '/socket.io')

    while True:
      socketio.wait(seconds=1)    


if __name__ == "__main__":
  listener = Listener(INPUT_URI, INPUT_PORT)
  listener.listen()
