# -*- coding: utf-8 -*-
"""
    Flaskr
    ~~~~~~
"""
import eventlet
eventlet.monkey_patch()

import os
import numpy
import cv2

from PIL import Image
from flask import Flask, render_template, request, jsonify, Response, make_response
from flask_socketio import SocketIO

app = Flask(__name__, static_url_path='/static')
socketio = SocketIO(app, message_queue='redis://')

frame=None

@app.route('/')
def show_dashboard():
    return render_template('index.html')

@app.route('/video_spec')
def video_spec():
    spec = {'width':320, 'height':240}
    return jsonify(results=spec)

@app.route('/video_input', methods=['POST'])
def store_video_frame():
    global frame
    frame = request.data
    return make_response('OK')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def gen():
    global frame

    if (frame == None):
        """No frame received yet...Loading default image to fill the video stream frame"""
        img = numpy.asarray(Image.open('./empty_frame.jpg'))
        frame = cv2.imencode('.jpg', img)[1].tostring()

    while True:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@socketio.on('connect', namespace='/commands')
def ws_conn():
    print("Connection established")
    socketio.emit('msg', {'count': 1}, namespace='/commands')


@socketio.on('disconnect', namespace='/commands')
def ws_disconn():
    print("Connection closed")
    socketio.emit('msg', {'count': 1}, namespace='/commands')

@socketio.on('command', namespace='/commands')
def ws_drive(message):
    print(message)
    socketio.emit('drive', message,
                  namespace="/commands")

if __name__ == "__main__":
    socketio.run(app, "0.0.0.0", port=5000)