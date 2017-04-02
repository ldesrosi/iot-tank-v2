#!/usr/bin/env python
from flask import Flask, render_template, Response, request

# Raspberry Pi camera module (requires picamera package)
from camera_pi import Camera

import motormanager

motorManager = motormanager.MotorManager(120, 5)

app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

@app.route('/control')
def controller():
    return render_template('leapControl.html')

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/drive')
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

   return Response("", status=200, mimetype='application/json')
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
