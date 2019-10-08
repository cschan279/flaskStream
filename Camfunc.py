#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: troyc
"""
import cv2




def encodeFrame(img):
    r, codeframe = cv2.imencode('.jpg', img)
    bytesframe = codeframe.tobytes()
    head = b'--frame\r\nContent-Type: image/jpeg\r\n\r\n'
    tail = b'\r\n\r\n'
    package = head + bytesframe + tail
    return package


