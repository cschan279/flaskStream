#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: troyc
"""
import cv2
import time

from func_timeout import func_timeout, FunctionTimedOut



def encodeFrame(img):
    r, codeframe = cv2.imencode('.jpg', img)
    bytesframe = codeframe.tobytes()
    head = b'--frame\r\nContent-Type: image/jpeg\r\n\r\n'
    tail = b'\r\n\r\n'
    package = head + bytesframe + tail
    return package



def timeoutCam(cam, t=1):
    r, f = False, None
    try:
        r, f = func_timeout(1, cam.read)
        return r, f
    except:
        return False, None
        

'''

