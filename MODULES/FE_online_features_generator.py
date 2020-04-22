# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo)s
@email: %(mikel1982mail@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED))
@DOI: 10.5281/zenodo.3727503 
"""
#%%
from FER_STRATEGIES.fr_system import FR_system
from COM.tcpip_dict_client import tcpip_client as client
from multiprocessing import Process
from threading import Thread
import numpy as np

class pipeline(Thread):
    '''
        A class for online feature extraction and estimation.
    '''
    def __init__(self, app):  
        Thread.__init__(self)
        self.app = app
        # -- tcpip dict client settings --
        self.client = client(self.app.video_dmg.buffer.toADDRESS, self.app.video_dmg.buffer.PORT)
        self.client.create_socket()
        self.client.connect()

    def run(self):
        print('##### start online estimation pipeline ######')
        self.app.slots.append(self.start_process)     
        print('############## slots appened #############')
            
    def start_process(self):
        print('start process method has been called')
        process = Process(target=self.send_data)
        process.start()
         
    def send_data(self):
        print('sending data get video frames')
        # -- get sample --
        video_frames = self.app.video_dmg.buffer.get_frames() 
        # -- facial recognition system --
        self.FR = FR_system()
        cropped_faces = np.array([self.FR.face_cropping(frame).squeeze() for frame in video_frames])
        print('cropped_faces shape: ', cropped_faces.shape)
        # -- send data --
        self.client.send_msg({'FER':cropped_faces})
        print('finish sending data')
        
        
