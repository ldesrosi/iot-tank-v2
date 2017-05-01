import time
import io
import threading
import picamera
import picamera.array
import numpy
import requests
import cv2

class Camera(object):
    thread = None  # background thread that reads frames from camera

    def initialize(self):
        if Camera.thread is None:
            # start background frame thread
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

    @classmethod
    def _thread(cls):
        with picamera.PiCamera() as camera:
            # camera setup
            camera.resolution = (320, 240)
            camera.hflip = True
            camera.vflip = True
            
            rawCapture = picamera.array.PiRGBArray(camera, size=(320, 240))
            # let camera warm up
            camera.start_preview()
            time.sleep(2)

            stream = io.BytesIO()
            i = 0
            for frame in camera.capture_continuous(rawCapture, 'bgr',
                                                 use_video_port=True):
                image = numpy.copy(frame.array)
           
                stream.write(cv2.imencode('.jpg', image)[1]) 
                
                # store frame
                stream.seek(0)
                frame = stream.read()

                requests.post('http://192.168.0.21:5000/video_input', data=frame)
                
                print i
                i = i + 1
                # reset stream for next frame
                stream.seek(0)
                stream.truncate()

                rawCapture.truncate(0)

        cls.thread = None

camera_stream = Camera()
camera_stream.initialize()
