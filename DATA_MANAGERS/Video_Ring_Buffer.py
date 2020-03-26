# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo)s
@email: %(mikel1982mail@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED))
"""
from FILTERS import image_processing
from DATA_MANAGERS.video_constants import video_constants
from PyQt5 import QtCore 
import numpy as np

class VideoRingBuffer(QtCore.QThread, video_constants):
    """ class that implements a not-yet-full buffer """
    emitter = QtCore.pyqtSignal()
    
    def __init__(self, parent=None):
        super(VideoRingBuffer, self).__init__(parent)
        video_constants.__init__(self)
        ##################################################
        self.max = self.WINDOW
        self.data = np.zeros(self.SHAPE, dtype=np.uint8)
        self.cur = self.max
        self.full = False
         
    def reset(self):
        self.data = np.zeros(self.SHAPE, dtype=np.uint8)
        self.cur = self.max
        self.full = False
        print('WEBCAM Buffer data has been cleared.')
        
    def append(self,x):
        """append an element at the end of the buffer"""  
        self.cur = self.cur % self.max
        self.data[self.cur] = image_processing.change_color(x)
        self.cur = self.cur+1
        # if (self.cur % self.WINDOW) == 0:
        #     self.emitter.emit()  
        #     print('WEBCAM full myfriend: ', self.cur)              

    def get_frames(self):
        """ Return a list of elements from the oldest to the newest. """
        return np.concatenate((self.data[self.cur:], self.data[:self.cur]), axis=0)
    
    def get_singleFrame(self):
        """ Return the last elemet queued. """
        frames = self.get_frames()
        frame = image_processing.transpose(frames[-1]) 
        return frame
    
    
    
