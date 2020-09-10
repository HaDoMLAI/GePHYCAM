# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo)s
@email: %(mikel1982mail@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED))
@DOI: 10.5281/zenodo.3727503 
"""
#%%

from DRIVERS.EMPATICA_E4 import E4_socket 
from DRIVERS.OpenBCI import OpenBCIBoard as openBCI
from DRIVERS.video_recorder import VideoRecorder

from DATA_MANAGERS.E4_data_manager_02 import E4_data_manager
from DATA_MANAGERS.OpenBCI_data_manager import OpenBCI_data_manager 
from DATA_MANAGERS.video_data_manager import VideoDMG

from GUI.integrator_GUI_00 import GUI 
from LOG.log import log

from GENERAL import Dynamic_Import as Dyn_import 
from GENERAL.global_constants import constants

from multiprocessing import Queue, Value
from PyQt5 import QtWidgets
import sys

class MyApp(QtWidgets.QApplication):
    def __init__(self):
        QtWidgets.QApplication.__init__(self,[''])
        # -- CREATE SHARED VARIABLES AND QUEUES ------------
        self.constants = constants()
        # -- shared values for streaming control --
        self.video_streaming = Value('b',0)
        self.BCI_streaming = Value('b',0)
        # -- shared values to check socket connections --
        self.OpenBCI_connected = Value('b',0)
        self.E4_connected = Value('b',0)
        self.CAM_connected = Value('b',0)
        # -- queues --
        self.video_queue = Queue()
        self.eeg_queue = Queue()
        ############# GUI DEFINITION ############################
        self.gui = GUI(self, callbacks = [self.saveFileDialog, self.openFileNameDialog, 
                                          self.E4_server_link, self.E4_connect, self.E4_refresh, 
                                          self.OpenBCI_connection_manager,
                                          self.webcam_connection_manager])  
        # -- CREATE SERVICES ----------------
        self.log = log(self.gui.logger)
        # ------------ DRIVERS definitions --------------------        
        #-- OpenBCI DataManager
        self.eeg_dmg = OpenBCI_data_manager(self.eeg_queue)  
        self.eeg_dmg.start()
        # # -- Empatica E4 DataManagers--
        self.E4_dmgs = []
        self.E4_dmgs.append(E4_data_manager(signal='bvp', num_signals=1, sample_rate=64))
        self.E4_dmgs.append(E4_data_manager(signal='gsr', num_signals=1, sample_rate=4))
        self.E4_dmgs.append(E4_data_manager(signal='tmp', num_signals=1, sample_rate=4))
        # -- webcam --
        self.video_dmg = VideoDMG(self.video_queue, self.video_streaming)
        self.video_dmg.start()
        # ---------- INITIALIZE GUI ----------- 
        self.gui.init_values()
        
    def webcam_connection_manager(self):
        if not self.CAM_connected.value:
            try:
                self.log.myprint('Trying to connect to webcam device')
                self.VideoRecorder = VideoRecorder(self.video_queue, self.video_streaming, self.CAM_connected)
                self.VideoRecorder.connect()
                if self.CAM_connected.value:
                    self.VideoRecorder.start()
                    self.log.myprint('webcam is ready')
                else:
                    self.VideoRecorder.kill()
            except:
                self.log.myprint_error('Cannot connect to webcam device')
                self.VideoRecorder.kill()
        else:
            self.VideoRecorder.kill()
            self.log.myprint('webcam is over')
            
    def OpenBCI_connection_manager(self):     
        if not self.OpenBCI_connected.value:
            self.BCI_driver = openBCI(self.eeg_queue, self.BCI_streaming, self.OpenBCI_connected)
            self.BCI_driver.set_logger(self.log)
            self.BCI_driver.connect()
            print('main bci driver is connected: ', self.OpenBCI_connected.value)
            if self.OpenBCI_connected.value:
                self.BCI_driver.start()
            else:
                self.BCI_driver.kill()
        else:
            self.BCI_driver.kill()
    
    def E4_server_link(self):
        print('E4 server link ', not self.E4_connected.value)
        if not self.E4_connected.value:
            try:
                print('entro')
                self.E4_driver = E4_socket(self.E4_connected, 
                                           self.E4_dmgs, 
                                           callbacks=[self.gui.device_list_slot,
                                                      self.gui.device_connect_slot, 
                                                      self.gui.data_pause_slot, 
                                                      self.gui.data_subscribe_slot])  
                self.E4_driver.set_logger(self.log)
                self.E4_driver.openPort(self.constants.E4_IP, self.constants.E4_PORT)
                self.E4_refresh()
                self.E4_driver.start()
            except:
                self.log.myprint_error('Cannot connect to Empatica Server')
                self.E4_driver.kill()
        else:
            self.E4_driver.kill()

            
    def E4_connect(self):
        try:
            self.E4_driver.connectDevice(self.gui.E4_device_ComboBox.itemText(self.gui.E4_device_ComboBox.currentIndex()))
            self.E4_driver.subscribe("ON")
        except:
            self.log.myprint_error('The connection is already in process')
            
    def E4_refresh(self):
        self.E4_driver.listDevice()
        
    def saveFileDialog(self):    
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self.gui,"QFileDialog.getSaveFileName()","","EDF Files (*.edf)", options=options)
        if fileName:
            self.constants.set_path(fileName)
            
    def openFileNameDialog(self):    
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileType = "PYTHON Files (*.py)"
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self.gui,"QFileDialog.getOpenFileName()","",fileType, options=options)       
        #----- LOAD AND EXECUTE THE MODULE -----#
        print('opening: ', fileName)
        if fileName:
            Dyn_import.load_module(fileName, self)
            
    def execute_gui(self):
        ret = self.exec_()
        # -- release devices --
        if self.OpenBCI_connected.value:
            self.BCI_driver.kill()
        if self.CAM_connected.value:
            self.VideoRecorder.kill()
        if self.E4_connected.value:
            self.E4_driver.kill()
        # -- system exit --
        sys.exit(ret)

if __name__ == "__main__":
    main = MyApp()
    main.execute_gui()
