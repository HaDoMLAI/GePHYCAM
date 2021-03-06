# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo)s
@email: %(mikel1982mail@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED))
@DOI: 10.5281/zenodo.3727503 
"""
#%%
import numpy as np
#from scipy import signal
from neurodsp import spectral
from lspopt.lsp import spectrogram_lspopt

class spectrum():
    def __init__(self, NDIMS, SAMPLE_RATE):
        self.NDIMS = NDIMS
        self.SAMPLE_RATE = SAMPLE_RATE
        
    def get_spectrum(self, samples):
        spectrums = []
        for i in range(self.NDIMS):
             freqs, spectre  = spectral.compute_spectrum(samples[i,:], self.SAMPLE_RATE)
             spectrums.append(spectre)
        return freqs, np.asarray(spectrums)
    
    def get_spectrogram(self, samples):
#        _, _, Sxx = signal.spectrogram(samples, self.constants.SAMPLE_RATE)
        _,_, Sxx = spectrogram_lspopt(samples, self.SAMPLE_RATE, c_parameter=20.0)
        return Sxx
        
