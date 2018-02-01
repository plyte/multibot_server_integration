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
verbose=True
mission_number = ""

class Namespace(BaseNamespace):

  def on_cmstartmission(self, *args):
    print('Starting {}'.format(args[0]))

  def on_tester(self, *args):
    print('test: ', args)

  def on_cminitializemission(self, *args):

    counter=0

    def run_roslaunch(self, message):

        roslauch_process = Popen('roslaunch multirobot {}.launch'.format(message), stdout=PIPE, stderr=PIPE, shell=True)
        
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
        
        if len(message_emit) < 30:
            self.emit('cminitializemission', 'Initializing gazebo environment')       
            run_roslaunch(self, message)
        else: 
            self.emit('cminitializemission', message_emit)

    if counter == 0:
        check_switch_case(self, args[0])
        counter+=1

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
