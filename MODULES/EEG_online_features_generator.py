#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo)s
@email: %(mikel1982mail@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED))
"""
from FEATURES.online_features_02 import compute_online_features
from FILTERS.EAWICA import eawica
from COM.tcpip_dict_client import tcpip_client as client
from multiprocessing import Process
from threading import Thread


class pipeline(Thread):
    '''
        A class for online feature extraction and estimation.
    '''
    def __init__(self, app):  
        Thread.__init__(self)
        self.app = app
        # -- tcpip dict client settings --
        self.client = client(self.app.constants.toADDRESS, self.app.constants.PORT)
        self.client.create_socket()
        self.client.connect()

    def run(self):
        print('##### start online estimation pipeline ######')
        self.app.slots.append(self.start_process)     
        print('############## slots appened #############')
            
    def start_process(self):
        process = Process(target=self.send_data)
        process.start()
        
    def send_data(self):
        # -- get sample --
        sample = self.app.eeg_dmg.get_short_sample(self.app.constants.METHOD)   
        # -- artifact removal --
        sample = eawica(sample,self.app.constants)
        # -- compute features --
        features = compute_online_features(sample,self.app.constants)
        # -- send data --
        self.client.send_msg({'EEG':features})
        
        

        
    

        
        