#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: troyc
"""
import cv2
import numpy as np
from threading import Thread
import time

class VidCam:
    def __init__(self, source):
        self.source = source
        self.cam = cv2.VideoCapture(source)
        self.repeat = False
        self.w = self.cam.get(3)
        self.h = self.cam.get(4)
        self.fps = self.cam.get(5)
        print('size: {}x{}'.format(self.w, self.h))
        print('fps: {}/second'.format())
        return
    
    def loop(self):
        self.wait4stop()
        self.repeat = True
        while self.repeat:
            self.r
        
    def wait4stop(self):
        self.repeat = False
        i = 0
        msgWait = '\nwaiting thread for cam-{} to be stopped'
        msgStop = ''
        while self.th.isAlive():
            if i%10:
                print('.', end='')
            else:
                print(msgWait.format(self.source), end='')
            i += 1
            time.sleep(0.2)
        print('no threading on capturing cam-{}'.format(self.source))
        return
    
    def __del__(self):
        self.wait4stop()
        self.cam.release()
        print('cam-{} released'.format(self.source))
        return
        
    def get_frame(self):
        r,f = self.cam.read()
        if r:
            re, fe = cv2.imencode('.jpg',f)
        else:
            re, fe = cv2.imencode('.jpg',np.zeros((self.w,self.h,3),np.uint8))
        return fe.tobytes()
