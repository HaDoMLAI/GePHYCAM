# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo)s
@email: %(mikel1982mail@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED))
"""
from DATA_MANAGERS.OpenBCI_ring_buffer_02 import RingBuffer as EEG_buffer

from FILTERS.filter_bank_manager import filter_bank_class
from FILTERS.spectrum import spectrum 

from threading import Thread, Lock, Event
import time 
import numpy as np

class OpenBCI_data_manager(Thread):
    
    def __init__(self, queue):
        Thread.__init__(self) 
        ### data ###########
        self.EEG_buffer = EEG_buffer()
        self.all_data_store = []
        self.queue = queue
        ########### SHARED QUEUE ###########
        self.filter_bank = filter_bank_class(self.EEG_buffer.LOWCUT, self.EEG_buffer.HIGHCUT, self.EEG_buffer.NOTCH, self.EEG_buffer.ORDER, self.EEG_buffer.SAMPLE_RATE)
        self.filter_bank.set_filters(self.EEG_buffer.LOWCUT, self.EEG_buffer.HIGHCUT)
        self.spectrum = spectrum(self.EEG_buffer.NDIMS, self.EEG_buffer.SAMPLE_RATE)
        # -- flag --
        self.exit = Event()
        self.exit.set()
        ###### mutex lock
        self.mutexBuffer = Lock()  
     
    def run(self):     
        while self.exit.is_set():  
            time.sleep(0.001)
            while not self.queue.empty(): 
                try:
                    self.mutexBuffer.acquire()
                    sample = self.queue.get()
                    self.mutexBuffer.release()
                    self.EEG_buffer.append(sample)
                    self.all_data_store.append(np.asarray(sample).transpose())
                except:
                    print('algo pasa en dmg tronco!!!!!')
                
    def reset_data_store(self):     
        self.all_data_store = []
        
    def get_allData(self):
        return np.asarray(self.all_data_store)
        
    def get_sample(self): 
        filtered = self.filter_bank.pre_process( self.EEG_buffer.get() )
        return filtered
    
    def get_short_sample(self, method): 
        filtered = self.filter_bank.pre_process( self.EEG_buffer.get() )
        filtered = filtered[:,int(self.EEG_buffer.pos_ini):int(self.EEG_buffer.pos_end)]  
        return filtered

    def get_powerSpectrum(self, method):
        try:
            filtered = self.filter_bank.pre_process( self.EEG_buffer.get() )
            freqs, spectra = self.spectrum.get_spectrum( filtered )
            return [freqs, spectra]
        except:
            return None
        
    
    def get_powerSpectrogram(self, method, channel):
        try:
            filtered = self.filter_bank.pre_process( self.EEG_buffer.get() )
            spectrogram = self.spectrum.get_spectrogram( filtered[channel,:])
            return spectrogram
        except:
            return None
 
    def kill(self):
        self.exit.clear() 

        
    
        
        
        
        
        
        