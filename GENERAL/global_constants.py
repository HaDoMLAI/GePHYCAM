# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo)s
@email: %(mikel1982mail@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED))
@DOI: 10.5281/zenodo.3727503 
"""
#%%
class constants:
    
    def __init__(self):
        # -- TCPIP --
        self.ADDRESS = 'localhost'
        self.PORT = 10000
        # -- E4 IP adress --
        self.E4_IP = 'localhost'
        self.E4_PORT = 8000
        # -- Devices --
        self.PATH = ''
        self.TRIAL = 0

    def set_path(self, path):
        self.PATH = path
        
    def update_trial(self):
        self.TRIAL += 1
        
    def set_tcpip(self, address, port):
        self.ADDRESS = address
        self.PORT = port
        
    def set_E4_tcpip(self, address):
        self.E4_IP = address
