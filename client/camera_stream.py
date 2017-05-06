import time
import io
import threading
import picamera
import picamera.array
import numpy
import requests
import cv2

class VideoStream(object):
    thread = None  # background thread that reads frames from camera
    server_url = None
    processors=[]

    def addCallback(self, callback):
        VideoStream.processors.append(callback)

    def initialize(self, server_url='http://localhost:5000/trevor/video_input'):
        if VideoStream.thread is None:
            VideoStream.server_url = server_url

            # start background frame thread
            VideoStream.thread = threading.Thread(target=self._thread)
            VideoStream.thread.start()


    @classmethod
    def _thread(cls):
        with picamera.PiCamera() as camera:
            # camera setup
            camera.resolution = (320, 240)
            camera.hflip = True
            camera.vflip = True

            rawCapture = picamera.array.PiRGBArray(camera, size=(320, 240))

            camera.start_preview()
            time.sleep(2)

            stream = io.BytesIO()
            for frame in camera.capture_continuous(rawCapture, 'bgr',
                                                 use_video_port=True):
                image = numpy.copy(frame.array)

                resuts = (image,0,0,0,0)
                for (callback in cls.processors):
                    results = callback(expand(results))
                image = results[0]

                stream.write(cv2.imencode('.jpg', image)[1])

                # store frame
                stream.seek(0)
                frame = stream.read()

                requests.post(cls.server_url, data=frame)

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()

                rawCapture.truncate(0)

        cls.thread = None
