# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo)s
@email: %(mikel1982mail@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED))
@DOI: 10.5281/zenodo.3727503 
"""
#%%
from DATA_MANAGERS.E4_constants import E4_constants
#from PyQt5 import QtCore 
import numpy as np

class RingBuffer(E4_constants):#QtCore.QThread, 
    """ class that implements a not-yet-full buffer """
#    emitter = QtCore.pyqtSignal()
    
    def __init__(self, signal, sample_rate, num_signals, parent=None):
#        super(RingBuffer, self).__init__(parent)
        E4_constants.__init__(self, signal, sample_rate, num_signals)
        #-------------------------------------
        self.channels = self.SIGNAL_NUMBERS+1
        self.max = self.WINDOW
        self.data = np.zeros((self.max, self.channels))
        self.cur = self.max
        self.control = self.SAMPLE_RATE*self.SECONDS
   
    def reset(self):
        self.data = np.zeros((self.max, self.channels))
        self.cur = self.max
        
    def append(self,x):
        """append an element at the end of the buffer"""  
        self.cur = self.cur % self.max
        self.data[self.cur,:] = np.array(x)
        self.cur = self.cur+1

        # if self.cur % self.control == 0:
        #     self.emitter.emit()  
        #     print('Empatica E4 buffer full myfriend')       

    def get(self):
        """ Return a list of elements from the oldest to the newest. """ 
        data = np.vstack((self.data[self.cur:,:], self.data[:self.cur,:]))
        return data
    
    
