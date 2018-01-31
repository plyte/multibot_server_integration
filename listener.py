from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from socketIO_client import LoggingNamespace
from socketIO_client import SocketIO


# 'http://ec2-52-24-126-225.us-west-2.compute.amazonaws.com'
# 81
INPUT_URI='http://ec2-52-24-126-225.us-west-2.compute.amazonaws.com'
INPUT_PORT=81

class Listener(object):

  def __init__(self, URI, PORT):
    self.URI = URI
    self.PORT = PORT

  def test(*args):
      print("Mission Initialized!")

  def check_message_recieved(*args):
    switch_case = {
      "mission1": "hellomission1",
      "mission2": "hellomission2",
      "mission3": "hellomission3",
      "mission4": "hellomission4",
      "mission5": "hellomission5"
    }

    socketio.emit('cm-mission-initialized', switch_case.get(args, "Nothing found!!"))

  def listen(self):

    print("Currently listening on {}".format(INPUT_URI))
    socketio = SocketIO('http://ec2-52-24-126-225.us-west-2.compute.amazonaws.com', 8080, LoggingNamespace)
    
    socketio.on('cm-initialize-mission', check_message_recieved)
    #socketio.on('tester', test)
    #socketio.emit('testee', 'asdf')
    socketio.wait(seconds=1)


if __name__ == "__main__":
  listener = Listener(INPUT_URI, INPUT_PORT)
  listener.listen()
