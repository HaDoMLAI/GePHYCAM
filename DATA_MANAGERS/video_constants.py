# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo)s
@email: %(mikel1982mail@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED))
"""
#%%
from GENERAL.global_constants import constants

class video_constants(constants):
    def __init__(self):
        constants.__init__(self, 'video')
        # -- initializations --
        self.fps = 30
        self.device_index = -1
        self.WINDOW = self.fps * self.CAMERA_SECONDS
        self.frameSize = (480,640) 
        self.all_data_shape = (0,480,640,3)     
        self.SHAPE = (self.WINDOW,480,640,3)
        self.temp = './data/temp_' + str(self.name) + '.avi'
        


          
        
