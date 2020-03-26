# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo)s
@email: %(mikel1982mail@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED))
"""
#%%
import cv2
import numpy as np

def change_color(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

def transpose(frame):
    frame = np.transpose(frame,(1,0,2))
    frame = cv2.flip(frame,1)
    return frame
