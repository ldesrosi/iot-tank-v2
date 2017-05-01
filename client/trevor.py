#!/usr/bin/env python

import sys
import json

from socketIO_client import SocketIO, BaseNamespace

import camera_stream 
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

def drive(angle, speed):
   if (speed == 0):
     motorManager.stop()
   elif (angle < -15):
     motorManager.left(speed)
   elif (angle > 15):
     motorManager.right(speed)
   else:
     motorManager.forward(0.5)

class CommandNamespace(BaseNamespace):
    def on_drive(self, *args):
        print('[websocket: drive]:',args)
        data = json.loads(args[0])
        drive(data['a'],data['s'])

    def on_connect(self):
        print('[websocket: connect]')

    def on_disconnect(self):
        print('[websocket: disconnect]')

    def on_reconnect(self):
        print('[websocket: reconnect]')

def main(argv):
    print('Hostname:'+argv[1])
    print('Port:'+argv[2])

    global motorManager, videoStream, socketIO, cmd_namespace 

    videoStream = camera_stream.VideoStream()
    videoStream.initialize(server_url="http://" + argv[1] + ":" + argv[2] +"/video_input")

    motorManager = motormanager.MotorManager()

    socketIO = SocketIO(argv[1], argv[2])
    cmd_namespace = socketIO.define(CommandNamespace, '/commands')
    socketIO.wait()

if __name__ == "__main__":
   main(sys.argv)
