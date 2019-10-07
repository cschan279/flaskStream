#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: troyc
"""
from flask import Flask, render_template, Response
from cam import VidCam
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(cam):
    fps = cam.fps
    waittime = round(1/fps,3)
    while True:
        frame = cam.get_frame()
        time.sleep(waittime)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VidCam(0)),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
