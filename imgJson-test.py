#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, render_template, Response, request, jsonify
import json
import base64
import cv2
import pickle
import numpy as np

cv_img = np.zeros((600,800,3),np.uint8)
im_size = [600,800]
coor = [0,0]
r_size = 50,50


app = Flask(__name__)


def draw_new_img():
    global im_size, coor
    cv_img = np.zeros((tuple(im_size)+(3,)),np.uint8)
    
    c1 = tuple(coor)
    c2 = (c1[0] + r_size[0]), (c1[1] + r_size[1])
    
    cv2.rectangle(cv_img, c1, c2, (0, 255, 0), 2)
    
    coor[0] = coor[0]+ im_size[0]//100
    coor[1] = coor[1]+ im_size[1]//100
    
    if coor[0] >= im_size[0]:
        coor[0] = coor[0] - im_size[0]
    if coor[1] >= im_size[1]:
        coor[0] = coor[1] - im_size[1]
    
    return cv_img
    

@app.route('/')
def index():
    return render_template('test-json-img.html')

@app.route('/jsonImg/')
def jsonImg():
    global cv_img, coor
    print('jsonImg')
    cv_img = draw_new_img()
    _, data_img = cv2.imencode('.JPG',cv_img)
    try:
        b_img = base64.b64encode(data_img).decode('ascii')
    except Exception as e:
        print(e)
    jstr = json.dumps({"image": b_img})
    print('Hello')
    return jstr

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
    print('exit')
