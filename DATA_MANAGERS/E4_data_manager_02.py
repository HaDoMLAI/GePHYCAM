# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 15:26:41 2018

@author: UNED
"""
from DATA_MANAGERS.E4_ring_buffer_02 import RingBuffer as buffer
from threading import Lock
import numpy as np

class E4_data_manager():
   
    def __init__(self, signal=None, signal_numbers=None, seconds=None, sample_rate=None):
        ############### CONSTANTS ######################  
        self.SIGNAL = signal
        self.SIGNAL_NUMBERS = signal_numbers
        self.SECONDS = seconds
        self.SAMPLE_RATE = sample_rate         
        self.WINDOW = self.SAMPLE_RATE*self.SECONDS 
        self.freqTask = self.SAMPLE_RATE
        ############### buffer ########################
        self.buffer = buffer(channels=self.SIGNAL_NUMBERS+1, num_samples=self.WINDOW, sample_rate=self.SAMPLE_RATE)
        self.allData = np.empty((0, self.buffer.channels))
        ###### mutex lock
        self.mutexBuffer = Lock()       
               
    def get_allData(self):
        return self.allData
        
    def reset_data_store(self):
        self.allData = np.empty((0, self.buffer.channels))
        print('reset alldata E4 signal' + self.SIGNAL)
        
    def setWindow(self,seconds):
        self.mutexBuffer.acquire()
        self.SECONDS = seconds
        self.WINDOW = self.SAMPLE_RATE * self.SECONDS
        self.mutexBuffer.release()
        
    def getWindow(self):
        return self.WINDOW
    
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
    