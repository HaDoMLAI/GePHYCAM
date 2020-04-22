# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo)s
@email: %(mikel1982mail@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED))
@DOI: 10.5281/zenodo.3727503 
"""
#%%
import os
import numpy as np
from multiprocessing import Process
    
def create_file(path, trial, signal, all_data_store):
    data_file = os.path.join('.', path + '_' + signal + '_trial_' + str(trial))
    p = Process(target=save, args=(data_file,all_data_store))
    p.start()

def save(data_file,data):   
    np.save(data_file, data)
 
