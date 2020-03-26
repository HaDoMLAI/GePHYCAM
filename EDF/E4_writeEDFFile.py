#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 10:42:31 2019

@author: anaiak
"""
import os
import numpy as np
from multiprocessing import Process
    
def create_file(path, trial, signal, all_data_store):
    data_file = os.path.join('.', path + '_' + signal + '_trial_' + str(trial))
    p = Process(target=save, args=(data_file,all_data_store))
    p.start()

def save(data_file,data):   
    np.save(data_file, data)
 
