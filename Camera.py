#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: troyc
"""
import cv2
import numpy as np
import time
import Camfunc
from threading import Thread

class Camera:
    def __init__(self, source, width=None, height=None, fps=None):
        
        self.ready, self.repeat = False, False
        self.th = Thread()
        self.width, self.height, self.fps = 20, 20, 1
        
        self.th1 = Thread(target=self.startcam, 
                         args=(source, ), 
                         kwargs={'width':width, 'height':height, 'fps':fps})
        self.th1.start()
        
        self.ret, self.frame = False, self.emptyframe()
        self.th2 = Thread(target=self.loopread)
        self.th2.start()
        
        
        return
    
    def startcam(self, source, width=None, height=None, fps=None):
        self.source = source
        self.repeat = True
        while self.repeat:
            self.camera = cv2.VideoCapture(source)
            if self.checkcam():
                self.setcam(width=width, height=height, fps=fps)
                break
            else:
                print('Failed to connect with source-{}'.format(source))
        return 
    
    def loopread(self):
        self.repeat = True
        count=0
        while self.repeat:
            if self.ready:
                r, f = Camfunc.timeoutCam(self.camera, t=1)
                #r, f = self.camera.read()
                if r:
                    self.ret, self.frame = True, f.copy()
                else:
                    print('#', self.width,self.height)
                    self.ret, self.frame = False, self.emptyframe()
                    self.restartCam()
                    time.sleep(1)
            else:
                time.sleep(1)
        return
        
    def getframe(self):
        return self.ret, self.frame
    
    def restartCam(self):
        if not self.th1.isAlive():
            self.camera.release()
            self.th1 = Thread(target=self.startcam, 
                         args=(self.source, ), 
                         kwargs={'width':self.width, 'height':self.height, 'fps':self.fps})
            self.th1.start()
        else:
            print('pending to start the camera')
        return
        
    def emptyframe(self):
        return np.zeros((self.width,self.height,3),np.uint8)
        
    def checkcam(self):
        if self.camera.isOpened():
            self.ready = True
            return True
        else:
            self.ready = False
            self.camera.release()
            return False
    
    def setcam(self, width=None, height=None, fps=None):
        if width:
            self.camera.set(3, width)
        self.width = int(self.camera.get(3))
        
        if height:
            self.camera.set(4, height)
        self.height = int(self.camera.get(4))
        
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
    
    
