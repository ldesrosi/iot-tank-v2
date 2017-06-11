import base64
import io
import picamera
import time
import threading

from PIL import Image
from socketIO_client import SocketIO
from StringIO import StringIO

class VideoStream(threading.Thread):

    def __init__(self, socketClient):
        threading.Thread.__init__(self)
	self.done = False
        self.socketClient = socketClient
        self.processors = []

    def addCallback(self, callback):
        self.processors.append(callback)

    def stop(self):
        self.done=True

    def run(self):
        with picamera.PiCamera() as camera:
            # camera setup
            camera.resolution = (320, 180)
            camera.framerate =30
            camera.hflip = True
            camera.vflip = True

            camera.start_preview()
            time.sleep(2)

            print('[camera: starting video stream]')
            stream = io.BytesIO()
            for frame in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                if (self.done):
		    break;

                stream.seek(0)
                image = Image.open(stream)

                results = (image,0,0,0,0)
                for callback in self.processors:
                    results = callback(*results)
                image = results[0]

                buf = StringIO()
                image.save(buf, 'JPEG')

                data = {
                    'raw': 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue())
                }

                self.socketClient.emit('stream_input', data)

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()


            print("[camera: shutting down video stream]") 
            stream.close()
            camera.close()
