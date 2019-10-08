#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: troyc
"""
from flask import Flask, render_template, Response, request, jsonify
import time
import cv2
import numpy as np
import json
import Camfunc
from Camera import Camera


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
        time.sleep(1/cam.fps)
        yield (pack)

@app.route('/video_feed')
def video_feed():
    addr = 'rtsp://admin:cepa5566@192.168.1.11'
    return Response(gen(Camera(addr)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/receiveImg', methods=['POST'])
def receiveImg():
    r = request
    nparr = np.fromstring(r.data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    time.sleep(1)
    response = {'size':list(img.shape)}
    return jsonify(response)



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
