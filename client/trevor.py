#!/usr/bin/env python

import sys
import json
import signal

from socketIO_client import SocketIO, BaseNamespace

import camera_stream
import motormanager
import collision_sensor
import datarecorder
import image_processor
import image_tracker
import pantiltmanager
import heading_sensor
import datarecorder

#import logging
#logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
#logging.basicConfig()

motorManager = None
panTiltManager = None
videoStream = None
socketIO = None
cmd_namespace = None
headingSensor = None
collisionSensor = None
coliisionManager = None

def drive(angle, speed):
   if (speed == 0):
     motorManager.stop()
   elif (angle < -15):
     motorManager.left(speed)
   elif (angle > 15):
     motorManager.right(speed)
   else:
     motorManager.forward(speed)

class IONamespace(BaseNamespace):
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

def signal_handler(signal, frame):
        videoStream.stop()
        headingSensor.stop()
        collisionSensor.stop()
        sys.exit(0)

def main(argv):
    print('Hostname:'+argv[1])
    print('Web Port:'+argv[2])
    print('Influx DB Port:'+argv[3])

    hostname = argv[1]
    webPort = argv[2]
    influxPort = argv[3]

    global motorManager, panTiltManager, videoStream,
           socketIO, cmd_namespace, headingSensor,
           collisionSensor, collisionManager

    socketIO = SocketIO(hostname, webPort)
    io_namespace = socketIO.define(IONamespace, '/trevor/io')

    dataRec = datarecorder.DataRecorder("","",host=hostname, port=influxPort)

    panTiltManager = pantiltmanager.PanTiltManager()

    videoStream = camera_stream.VideoStream(io_namespace)
    videoStream.addCallback(image_processor.FaceProcessor().process)
    videoStream.addCallback(image_tracker.ImageTracker(panTiltManager).process)
    videoStream.start()

    motorManager = motormanager.MotorManager(dataRecorder=dataRec)

    headingSensor = heading_sensor.HeadingManager(dataRecorder=dataRec)
    headingSensor.start()

    collisionManager = collision_manager.CollisionManager(panTiltManager, motorManager)

    collisionSensor = collision_sensor.CollisionSensor(dataRecorder=dataRec)
    collisionSensor.addEventListener(collisionManager.processEvent)
    collisionSensor.start()





    socketIO.wait()

if __name__ == "__main__":
   signal.signal(signal.SIGINT, signal_handler)
   main(sys.argv)
