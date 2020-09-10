# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo)s
@email: %(mikel1982mail@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED))
@DOI: 10.5281/zenodo.3727503 
"""
#%%
from DATA_MANAGERS.E4_ring_buffer_02 import RingBuffer as buffer
from threading import Lock
import numpy as np

class E4_data_manager():
   
    def __init__(self, signal=None, num_signals=None, sample_rate=None):
        ############### buffer ########################
        self.buffer = buffer(signal, sample_rate, num_signals)
        self.allData = np.empty((0, self.buffer.channels))
        ###### mutex lock
        self.mutexBuffer = Lock()       
               
    def get_allData(self):
        return self.allData
        
    def reset_data_store(self):
        self.allData = np.empty((0, self.buffer.channels))
        print('reset alldata E4 signal' + self.buffer.SIGNAL)
        
    def setWindow(self,seconds):
        self.buffer.SECONDS = seconds
        self.buffer.WINDOW = self.buffer.SAMPLE_RATE * self.buffer.SECONDS
        
    def getWindow(self):
        return self.buffer.WINDOW
    
    def clearBuffer(self):
        self.mutexBuffer.acquire()
        self.buffer.reset()
        self.reset_data_store()
        print('E4 Buffer data has been cleared.')
        self.mutexBuffer.release()
    
    def appendSample(self,sample):
        self.mutexBuffer.acquire()            
        self.buffer.append(sample)
        self.allData = np.vstack((self.allData, sample))
        self.mutexBuffer.release()
        
    def getSamples(self):
        self.mutexBuffer.acquire()
        plot_data = self.buffer.get()
        self.mutexBuffer.release()       
        return plot_data
    
    def close_file(self):
        self.io.close_file()
    
