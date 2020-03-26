# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo)s
@email: %(mikel1982mail@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED))
"""
#%%
from DATA_MANAGERS.video_constants import video_constants
from multiprocessing import Process, Lock, Event
import time
import cv2

class VideoRecorder(Process, video_constants):

	# Video class based on openCV 
    def __init__(self, video_queue, streaming, isconnected):
        video_constants.__init__(self)
        Process.__init__(self)  
        # -- streaming --
        self.streaming = streaming
        self.video_queue = video_queue
        self.isconnected = isconnected
        # -- flag --
        self.exit = Event()
        self.exit.set()
        ###### mutex lock
        self.mutexBuffer = Lock()  
    
    def connect(self):
        try:
            self.video_cap = cv2.VideoCapture(self.device_index)
            self.isconnected.value = True
        except:
            print('Cannot connect to webcam.')
        
    def disconnect(self):
        try:
            self.video_cap.release()
        except:
            print('no video cap to release')
        self.isconnected.value = False

    def run(self):
        while self.exit.is_set():  
            if self.streaming.value:
                ret, frame = self.video_cap.read()
                if ret:
                    self.mutexBuffer.acquire()
                    self.video_queue.put(frame)
                    self.mutexBuffer.release()
                time.sleep(1/self.fps)
            else:                
                while not self.video_queue.empty():  
                    self.video_queue.get()
                time.sleep(.001)
                    
        print('killing video recorder')
        self.disconnect()
        print('video recorder killed')
            
    def kill(self):
        self.exit.clear()  
        
        