# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo)s
@email: %(mikel1982mail@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED))
"""


class constants:
    
    def __init__(self, name):
        # -- TCPIP --
        self.ADDRESS = '10.1.28.141'
        self.PORT = 10006
        # -- E4 IP adress --
        self.E4_IP = '10.1.28.138'
        self.E4_PORT = 8000
        # -- Devices --
        self.CAMERA_SECONDS = 6
        self.EEG_SECONDS = 6
        self.BVP_SECONDS = 12
        self.GSR_SECONDS = 120
        self.TMP_SECONDS = 120
        self.PATH = ''
        self.TRIAL = 0
        # -- ID --
        self.name = name
        
    def set_path(self, path):
        self.PATH = path
        
    def update_trial(self):
        self.TRIAL += 1
        
    def set_seconds(self, seconds):
        self.SECONDS = seconds
        print('constants: ', self.SECONDS)
        
    def set_tcpip(self, address, port):
        self.ADDRESS = address
        self.PORT = port
        print('constants: ', self.ADDRESS, self.PORT)
        