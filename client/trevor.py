#!/usr/bin/env python

import sys

from socketIO_client import SocketIO, BaseNamespace
from camera_stream import VideoStream

import motormanager
import collisionmanager
import datarecorder
import image_processor
import pantiltmanager

#import logging
#logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
#logging.basicConfig()
motorManager = None
videoStream = None
socketIO = None
cmd_namespace = None

def drive():
   direction = request.args.get("direction")
   if (direction == "left"):
     motorManager.left(0.5)
   elif (direction == "right"):
     motorManager.right(0.5)
   elif (direction == "front"):
     motorManager.forward(0.5)
   elif (direction == "back"):
     motorManager.backward(0.5)
   else:
     motorManager.stop()

class CommandNamespace(BaseNamespace):
    def on_drive(self, *args):
        print('[websocket: drive]', args)
        print(type(args))

    def on_connect(self):
        print('[websocket: connect]')

    def on_disconnect(self):
        print('[websocket: disconnect]')

    def on_reconnect(self):
        print('[websocket: reconnect]')

def main(argv):
    videoStream = VideoStream()
    videoStream.initialize(server_url="http://" + argv[1] + ":" + argv[2] +"/video_input")

    motorManager = MotorManager()

    socketIO = SocketIO(argv[1], argv[2])
    cmd_namespace = socketIO.define(CommandNamespace, '/commands')
    socketIO.wait()



if __name__ == "__main__":
   main(sys.argv[1:])
