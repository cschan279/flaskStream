#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: troyc
"""
from flask import Flask, render_template, Response
import Camfunc
from Camera import Camera
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(cam):
    fps = cam.fps
    waittime = round(1/fps,3)
    while True:
        ret, frame = cam.getframe()
        pack = Camfunc.encodeFrame(frame)
        time.sleep(waittime)
        yield (pack)

@app.route('/video_feed')
def video_feed():
    addr = 0
    return Response(gen(Camera(addr),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
