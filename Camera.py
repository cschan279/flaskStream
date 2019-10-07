#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: troyc
"""
import cv2
import numpy as np
import time
from threading import Thread

class Camera:
    def __init__(self, source, width=None, height=None, fps=None):
        
        self.ready, self.repeat = False, False
        self.th = Thread()
        self.width, self.height, self.fps = 2, 2, 1
        self.th1 = Thread(target=self.startcam, 
                         args=(source, ), 
                         kwargs={'width':width, 'height':height, 'fps':fps})
        self.th1.start()
        
        self.ret, self.frame = False, self.emptyframe()
        self.th2 = Thread(target=self.loopread)
        self.th2.start()
        
        
        return
    
    def startcam(source, width=None, height=None, fps=None):
        self.source = source
        self.repeat = True
        while self.repeat:
            self.camera = cv2.VideoCapture(source)
            if self.checkcam():
                break
            else:
                print('Failed to connect with source-{}'.format(source))
        self.repeat = False
        return 
    
    def loopread(self):
        self.repeat = True
        while self.repeat:
            if self.ready:
                r, f = self.camera.read()
                if r:
                    self.ret, self.frame = True, f.copy()
                else:
                    self.ret, self.frame = False, self.emptyframe()
            else:
                time.sleep(1)
        return
        
    def getframe(self):
        return self.ret, self.frame
    
    def getencode(self):
        r, f = self.ret, self.frame.copy()
        cf = cv2.imencode('.jpg', f)
        return r, cf.tobytes()
        
    def emptyframe(self):
        return np.zeros((self.width,self.height,3),np.uint8)
        
    def checkcam(self):
        if self.camera.isOpened():
            self.setcam(width=width, height=height, fps=fps)
            self.ready = True
            return True
        else:
            self.ready = False
            self.camera.release()
            return False
    
    def setcam(width=None, height=None, fps=None):
        if width:
            self.camera.set(3, width)
        self.width = self.camera.get(3)
        
        if height:
            self.camera.set(4, height)
        self.height = self.camera.get(4)
        
        if fps:
            self.camera.set(5, fps)
        self.fps = self.camera.get(5)
        return
    
    
    def wait4stop(self):
        self.repeat = False
        i = 0
        msgWait = '\nWaiting threads for cam-{} to be stopped.'
        msgStop = '\nThread for cam-{} was terminated.'
        while self.th1.isAlive() or self.th2.isAlive():
            if i%10:
                print('.', end='')
            else:
                print(msgWait.format(self.source), end='')
            i += 1
            time.sleep(0.2)
        print(msgStop.format(self.source))
        return
    
    def __del__(self):
        self.wait4stop()
        self.camera.release()
        print('camera-{} released'.format(self.source))
        return
    
    
