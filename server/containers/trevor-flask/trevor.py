# -*- coding: utf-8 -*-
"""
    Flaskr
    ~~~~~~
"""
import gevent.monkey

gevent.monkey.patch_all()

import os
import base64
import numpy
import cv2

from PIL import Image
from flask import Flask, render_template, request, jsonify, Response, make_response
from flask_socketio import SocketIO

app = Flask(__name__, static_url_path='/trevor/static')
socketio = SocketIO(app) #, message_queue='redis://')

@app.route('/trevor')
def show_dashboard():
    return render_template('index.html')

@app.route('/trevor/video_spec')
def video_spec():
    spec = {'width':320, 'height':240}
    return jsonify(results=spec)

@socketio.on('connect', namespace='/trevor/io')
def ws_conn():
    print("Connection established")
    socketio.emit('msg', {'count': 1}, namespace='/trevor/io')


@socketio.on('disconnect', namespace='/trevor/io')
def ws_disconn():
    print("Connection closed")
    socketio.emit('msg', {'count': 1}, namespace='/trevor/io')

@socketio.on('command', namespace='/trevor/io')
def ws_drive(message):
    print(message)
    socketio.emit('drive', message,
                  namespace="/trevor/io")

@socketio.on('stream_input', namespace='/trevor/io')
def stream_video(message):
    socketio.emit('stream_output', message,
                  namespace="/trevor/io")

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port='5000',
        policy_server=False, transports='websocket, xhr-polling, xhr-multipart', debug=True)
