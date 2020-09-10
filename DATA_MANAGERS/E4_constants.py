#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 17:05:03 2020

@author: mikel
"""
class E4_constants():
    
    def __init__(self, signal, sample_rate, num_signals):
        self.SIGNAL = signal
        self.SAMPLE_RATE = sample_rate
        self.SIGNAL_NUMBERS = num_signals
        self.BVP_SECONDS = 12
        self.GSR_SECONDS = 120
        self.TMP_SECONDS = 120
        self.SECONDS = 6
        self.WINDOW = self.SAMPLE_RATE*self.SECONDS 
        self.freqTask = self.SAMPLE_RATE
        
    def update(self, signal, value):
        if signal == 'gsr':
            self.GSR_SECONDS = value
        elif signal == 'bvp':
            self.BVP_SECONDS = value
        elif signal == 'tmp':
            self.TMP_SECONDS = value
            
    def set_seconds(self, seconds):
        self.SECONDS = seconds