import time
import io
import threading
import picamera
import picamera.array
import numpy
import requests
import cv2
import base64

from StringIO import StringIO
from PIL import Image
from socketIO_client import SocketIO

class VideoStream(object):
    thread = None  # background thread that reads frames from camera
    server_url = None
    socketClient = None
    processors=[]

    def addCallback(self, callback):
        VideoStream.processors.append(callback)

    def initialize(self, socketClient):
        if VideoStream.thread is None:
            VideoStream.socketClient = socketClient

            # start background frame thread
            VideoStream.thread = threading.Thread(target=self._thread)
            VideoStream.thread.start()


    @classmethod
    def _thread(cls):
        with picamera.PiCamera() as camera:
            # camera setup
            camera.resolution = (320, 240)
            camera.framerate =30
            camera.hflip = True
            camera.vflip = True

            camera.start_preview()
            time.sleep(2)

            stream = io.BytesIO()
            for frame in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                #image = numpy.copy(frame.array)
                print("Loading Image")
                stream.seek(0)
                image = Image.open(stream)

                #resuts = (image,0,0,0,0)
                #for (callback in cls.processors):
                #    results = callback(*results)
                #image = results[0]
                print("Save to StringIO")
                buf = StringIO()
                image.save(buf, 'JPEG')

	        print("Send data")
                data = {
                    'raw': 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue())
                }

                cls.socketClient.emit('stream_input', data)

                #stream.write(cv2.imencode('.jpg', image)[1])

                # store frame
                #stream.seek(0)
                #frame = stream.read()

                #requests.post(cls.server_url, data=frame)
                print("Clean up")
                # reset stream for next frame
                stream.seek(0)
                stream.truncate()

                #rawCapture.truncate(0)

        cls.thread = None
