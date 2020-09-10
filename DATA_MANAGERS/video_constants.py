# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo)s
@email: %(mikel1982mail@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED))
@DOI: 10.5281/zenodo.3727503 
"""
#%%
class video_constants():
    def __init__(self):
        self.CAMERA_SECONDS = 6
        self.fps = 30
        self.device_index = -1
        self.WINDOW = self.fps * self.CAMERA_SECONDS
        self.frameSize = (480,640) 
        self.all_data_shape = (0,480,640,3)     
        self.SHAPE = (self.WINDOW,480,640,3)
        self.temp = './data/temp_webcam.avi'
        
    def set_seconds(self, seconds):
        self.CAMERA_SECONDS = seconds

        


          
        
