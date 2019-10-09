#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: troyc
"""
import cv2
import signal
import time
from contextlib import contextmanager



def encodeFrame(img):
    r, codeframe = cv2.imencode('.jpg', img)
    bytesframe = codeframe.tobytes()
    head = b'--frame\r\nContent-Type: image/jpeg\r\n\r\n'
    tail = b'\r\n\r\n'
    package = head + bytesframe + tail
    return package


@contextmanager
def timeout(t=0.5):
    signal.signal(signal.SIGALRM, raise_timeout)
    signal.alarm(t)
    
    try:
        yield
    except TimeoutError:
        pass
    finally:
        signal.signal(signal.SIGALRM, signal.SIG_IGN)
        
def raise_timeout(signum, frame):
    raise TimeoutError

'''
def testfunc(t):
    x = time.time()
    while time.time()-x < t:
        print('.', end='')
        time.sleep(0.2)
    return True

def trialfunc(t):
    x = 0
    with timeout(t=t):
        x = testfunc(2)
    return x
'''

