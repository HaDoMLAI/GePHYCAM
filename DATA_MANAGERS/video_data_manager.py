# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo)s
@email: %(mikel1982mail@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED))
@DOI: 10.5281/zenodo.3727503 
"""
#%%
from DATA_MANAGERS.Video_Ring_Buffer import VideoRingBuffer
from FILTERS import image_processing

from threading import Thread, Lock, Event
import numpy as np
import time

class VideoDMG(Thread):
    
    def __init__(self, queue, streaming):
        Thread.__init__(self) 
        # -- assignments --
        self.streaming = streaming
        self.queue = queue
        self.buffer = VideoRingBuffer()
        # -- data --
        self.all_video_frames = []
        # -- flag --
        self.exit = Event()
        self.exit.set()
        ###### mutex lock
        self.mutexBuffer = Lock()  
        
    def run(self):              
        while self.exit.is_set():
            if self.streaming.value and not self.queue.empty():
                self.mutexBuffer.acquire()
                frame = self.queue.get()
                self.mutexBuffer.release()
                try:
                    self.buffer.append(frame)
                    self.all_video_frames.append(image_processing.change_color(frame))
                except:
                    print('Sample loss in data manager -> ', self.buffer.signal)
            else:
                time.sleep(.001)
    
    def reset_data_store(self):       
        self.all_video_frames = []
    
    def get_allData(self):
        return np.asarray(self.all_video_frames)
        
    def kill(self):
        self.exit.clear() 
    
