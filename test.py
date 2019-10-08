#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import cv2

addr = 'http://0.0.0.0:5000/receiveImg'

content_type = 'image/jpeg'
headers={'content-type':content_type}

img = cv2.imread('123.png')
_, im_encoded = cv2.imencode('.jpg', img)

response = requests.post(addr, 
                        data=im_encoded.tostring(), 
                        headers=headers)

print(json.loads(response.text))
