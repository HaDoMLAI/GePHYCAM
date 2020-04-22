# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo)s
@email: %(mikel1982mail@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED))
@DOI: 10.5281/zenodo.3727503 
"""
#%%
from scipy.signal import butter, iirnotch, filtfilt
import numpy as np

class filter_bank_class(): 
    def __init__(self, LOWCUT, HIGHCUT, NOTCH, ORDER, SAMPLE_RATE):
        self.LOWCUT = LOWCUT
        self.HIGHCUT = HIGHCUT
        self.NOTCH = NOTCH
        self.ORDER = ORDER
        self.SAMPLE_RATE = SAMPLE_RATE
        
    def set_filters(self, LOWCUT, HIGHCUT):
        self.LOWCUT = LOWCUT
        self.HIGHCUT = HIGHCUT
        self.b0, self.a0 = self.notch_filter()
        self.b, self.a = self.butter_bandpass()
        
    def set_order(self, ORDER):
        self.ORDER = ORDER

    def pre_process(self, sample):
        sample = np.array(sample)
        [fil,col] = sample.shape	
        sample_processed = np.zeros([fil,col])
        for i in range(fil):
            data = sample[i,:] 
            data = data - np.mean(data) 	
            if self.LOWCUT != None and self.HIGHCUT != None: # 
                data = self.butter_bandpass_filter(data)
            data = data*1000000+(i+1)*100
            sample_processed[i,:] = data
  
        return sample_processed
        
    def notch_filter(self): # f0 50Hz, 60 Hz
        Q = 30.0  # Quality factor
        # Design notch filter
        b0, a0 = iirnotch(self.NOTCH , Q, self.SAMPLE_RATE)
        return b0,a0
    
    def butter_bandpass(self):
        nyq = 0.5 * self.SAMPLE_RATE
        low = self.LOWCUT / nyq
        high = self.HIGHCUT / nyq
        b, a = butter(self.ORDER , [low, high], btype='band')
        return b, a
    
    def butter_bandpass_filter(self, data):
        noth_data = filtfilt(self.b0, self.a0, data)
        band_passed_data = filtfilt(self.b, self.a, noth_data)
        return band_passed_data

    def butter_bandpass_specific_filter(self, data, lowcut, highcut, Fs, order):
        # -- notch filter --
        noth_data = filtfilt(self.b0, self.a0, data)
        # -- butterworth filter --
        nyq = 0.5 * Fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order , [low, high], btype='band')
        band_passed_data = filtfilt(b, a, noth_data)
        return band_passed_data
    
    def filter_bank(self, signal, Fs, filter_ranges, order=5):
        filterbank = []
        for [lowcut,highcut] in filter_ranges:
            y = self.butter_bandpass_specific_filter(signal, lowcut, highcut, Fs, order)
            filterbank.append(y)
        return np.asarray(filterbank)

    


