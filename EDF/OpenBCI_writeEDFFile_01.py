# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo)s
@email: %(mikel1982mail@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED))
"""
from multiprocessing import Process
import numpy as np
import os
 
def create_file(path, trial, all_data_store):
    data_file = os.path.join('.', path + '_' + 'EEG' + '_trial_' + str(trial))
    p = Process(target=save, args=(data_file,all_data_store))
    p.start()

def save(data_file,data):   
    np.save(data_file, data)
 