# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo)s
@email: %(mikel1982mail@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED))
@DOI: 10.5281/zenodo.3727503 
"""
#%%
from EDF import AudioVisual_io_01 as av_file_IO
from EDF import OpenBCI_writeEDFFile_01 as EEG_file_IO 
from EDF import E4_writeEDFFile as E4_writter
from COM.trigger_server_3 import trigger_server


from QTDesigner.INTEGRATOR_GUI_01 import  Ui_MainWindow as ui
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QFont
from qwt import QwtPlotCurve, QwtPlotItem, QwtText
import pyqtgraph as pg
import numpy as np

class GUI(QMainWindow, ui):
    def __init__(self, app, callbacks, parent=None):   
        QMainWindow.__init__(self, parent=parent) 
        self.app = app    
        ################    init #############################
        self.curves_EEG = []
        self.lr = None
        self.spectrogram_Img = None
        self.curves_Freq = []
        self.curves_EEG_short = []
        self.last_action = 'stop'
        self.trigger_server_activated = False
        ### BIOSIGNALS gui design ##############################
        self.setupUi(self)
        ############# callbacks ################################
        #-- General controls --
        self.save_bttn.clicked.connect(callbacks[0])
        self.script_bttn.clicked.connect(callbacks[1])
        self.trigger_bttn.clicked.connect(self.launch_trigger_server)
        self.PORT_SpinBox.valueChanged.connect(lambda: self.set_tcpip())
        self.IP_TextEdit.textChanged.connect(lambda: self.set_tcpip())
        self.E4_ip_lineEdit.textChanged.connect(lambda: self.set_E4_tcpip())
        self.start_bttn.clicked.connect(lambda: self.check_recording('test'))
        # -- drivers --
        self.E4_server_bttn.clicked.connect(callbacks[2])
        self.E4_connect_bttn.clicked.connect(callbacks[3])
        self.refresh_bttn.clicked.connect(callbacks[4])
        self.OpenBCI_connect_bttn.clicked.connect(callbacks[5])
        self.CAM_connect_bttn.clicked.connect(callbacks[6])
        # -- Filters --
        self.butterOrder_SpinBox.valueChanged.connect(lambda: self.set_order())
        self.filtering_ComboBox.currentIndexChanged.connect(lambda: self.set_filtering())
        self.frequency_ComboBox.currentIndexChanged.connect(lambda: self.set_frequency())
        self.Spectrogram_RadioButton.toggled.connect(lambda: self.set_channel_spectrogram())
        self.Spectrogram_ComboBox.currentIndexChanged.connect(lambda: self.set_channel_spectrogram())
        #-- Signals controls --
        self.CAM_ComboBox.valueChanged.connect(lambda: self.set_cam_bufferSize())
        self.EEG_ComboBox.valueChanged.connect(lambda: self.set_OpenBCI_bufferSize())
        self.BVP_ComboBox.valueChanged.connect(lambda: self.set_E4_bufferSize('BVP'))
        self.GSR_ComboBox.valueChanged.connect(lambda: self.set_E4_bufferSize('GSR'))
        self.TMP_ComboBox.valueChanged.connect(lambda: self.set_E4_bufferSize('TMP'))
        ############# set timers for updating plots ############
        # -- CAMERA Timers
        self.CAM_timer = QtCore.QTimer()
        self.CAM_timer.setTimerType(QtCore.Qt.PreciseTimer)
        self.CAM_timer.timeout.connect(self.face_streaming)
        # -- EEG timers --
        self.eeg_timer = QtCore.QTimer()
        self.eeg_timer.setTimerType(QtCore.Qt.PreciseTimer)
        self.eeg_timer.timeout.connect(self.eeg_update)
        self.eeg_short_timer = QtCore.QTimer()
        self.eeg_short_timer.setTimerType(QtCore.Qt.PreciseTimer)
        self.eeg_short_timer.timeout.connect(self.eeg_short_update)
        self.freq_timer = QtCore.QTimer()
        self.freq_timer.setTimerType(QtCore.Qt.PreciseTimer)
        self.freq_timer.timeout.connect(self.freq_update) 
        # -- BVP, GSR, TMP timers
        self.bvp_timer = QtCore.QTimer()
        self.bvp_timer.setTimerType(QtCore.Qt.PreciseTimer) 
        self.bvp_timer.timeout.connect(self.bvp_update)               
        self.gsr_timer = QtCore.QTimer()
        self.gsr_timer.setTimerType(QtCore.Qt.PreciseTimer) 
        self.gsr_timer.timeout.connect(self.gsr_update)      
        self.tmp_timer = QtCore.QTimer()
        self.tmp_timer.setTimerType(QtCore.Qt.PreciseTimer) 
        self.tmp_timer.timeout.connect(self.tmp_update)        
        
################ control streaming #######################
    def check_recording(self, action):          
        self.app.BCI_streaming.value = not self.app.BCI_streaming.value
        self.app.video_streaming.value = not self.app.video_streaming.value
        self.app.log.myprint('action ->' + action)
        
        if action == 'test' and self.app.BCI_streaming.value:
            self.startTimers()
        elif action == 'test' and not self.app.BCI_streaming.value:
            self.stopTimers()
            self.save_data()
              
    def launch_trigger_server(self):
        if self.trigger_server_activated:
            self.trigger_server.close_socket()
            del self.trigger_server
            self.trigger_server_activated = False
        else:
            self.trigger_server = trigger_server(address = self.app.constants.ADDRESS, port = self.app.constants.PORT)
            self.trigger_server.socket_emitter.connect(self.update_state)
            self.trigger_server.log_emitter.connect(self.app.log.myprint)
            self.trigger_server_activated = self.trigger_server.create_socket()
            if self.trigger_server_activated:
                self.trigger_server.start()  
            else:
                del self.trigger_server
                
    def update_state(self, action):
        if action != self.last_action:
            
            self.app.BCI_streaming.value = not self.app.BCI_streaming.value
            self.app.video_streaming.value = not self.app.video_streaming.value
            self.app.log.myprint('action ->' + action)
            self.last_action = action

            if action == 'start' and self.app.BCI_streaming.value:
                self.startTimers()
            elif action == 'stop' and not self.app.BCI_streaming.value:
                self.stopTimers()
                self.save_data()
    
    def save_data(self):
        # update trial
        self.app.constants.update_trial()
        self.app.log.myprint('trial updated -> ' + str(self.app.constants.TRIAL))
        #-- WEBCAM FILE IO
        av_file_IO.write_AV(self.app.video_dmg.get_allData(), self.app.constants.PATH, self.app.constants.TRIAL)
        # -- Empatica E4 FILE IO
        for dmg in self.app.E4_dmgs:
            E4_writter.create_file(self.app.constants.PATH, self.app.constants.TRIAL, dmg.buffer.SIGNAL, dmg.get_allData())
        # -- OpenBCI FILE IO
        EEG_file_IO.create_file(self.app.constants.PATH, self.app.constants.TRIAL,self.app.eeg_dmg.get_allData())
        print('all data is saved')
        # ###### reset buffers
        # -- OpenBCI
        self.app.eeg_dmg.reset_data_store()
        self.app.eeg_dmg.EEG_buffer.reset()
        # -- Empatica E4
        for dmg in self.app.E4_dmgs:
            dmg.clearBuffer()
        # -- WEBCAM
        self.app.video_dmg.reset_data_store()
        self.app.video_dmg.buffer.reset()
        print('all buffers are reset')
                
    def startTimers(self):
        ### START TIMERS 
        # -- Webcam
        self.CAM_timer.start(1/self.app.video_dmg.buffer.fps)
        # -- OpenBCI
        self.eeg_timer.start(1/250)
        self.eeg_short_timer.start(1/250)
        self.freq_timer.start(1/250)
        # --Empatica E4
        self.app.E4_driver.pause("OFF")
        self.bvp_timer.start((1/self.app.E4_dmgs[0].buffer.freqTask)*1000)
        self.gsr_timer.start((1/self.app.E4_dmgs[1].buffer.freqTask)*1000)
        self.tmp_timer.start((1/self.app.E4_dmgs[2].buffer.freqTask)*1000)
        

    def stopTimers(self):
        # -- Webcam
        self.CAM_timer.stop()
        # -- OpenBCI
        self.eeg_timer.stop()
        self.eeg_short_timer.stop()
        self.freq_timer.stop()
        # --Empatica E4
        self.app.E4_driver.pause("ON")
        self.bvp_timer.stop() 
        self.gsr_timer.stop() 
        self.tmp_timer.stop() 
        

######### SIGNAL VISUALIZATION UPDATE MANAGERS ################################ 
    def face_streaming(self):  
        frame = self.app.video_dmg.buffer.get_singleFrame()
        self.CAM_plot.imshow(frame)
        
    def eeg_update(self):       
        sample = self.app.eeg_dmg.get_sample()
        
        for i in range(self.app.eeg_dmg.EEG_buffer.CHANNELS):
            self.curves_EEG[i].setData(sample[i,:])
        
    def freq_update(self):
        if self.Spectrogram_RadioButton.isChecked():
            channel = self.app.eeg_dmg.EEG_buffer.CHANNEL_IDS.index(self.Spectrogram_ComboBox.currentText())
            spectrogram = self.app.eeg_dmg.get_powerSpectrogram(self.app.eeg_dmg.EEG_buffer.METHOD, channel) 
            if spectrogram != None:
                self.spectrogram_Img.setImage(spectrogram[:,:].T, autoLevels=True)
        else:
            out = self.app.eeg_dmg.get_powerSpectrum(self.app.eeg_dmg.EEG_buffer.METHOD)  

            if out != None and np.sum(out[1] > 1000):
                freqs = out[0]
                spectra = out[1]
                for i in range(self.app.eeg_dmg.EEG_buffer.CHANNELS):
                    try:
                        self.curves_Freq[i].setData(freqs,np.log10(spectra[i,:])) 
                    except:
                        pass


    def eeg_short_update(self):
        sample = self.app.eeg_dmg.get_short_sample(self.app.eeg_dmg.EEG_buffer.METHOD)
        for i in range(self.app.eeg_dmg.EEG_buffer.CHANNELS):
            self.curves_EEG_short[i].setData(sample[i,:])#
            
    def bvp_update(self):    
        val = self.app.E4_dmgs[0].getSamples()
        self.BVP_plot.curve.setData(np.arange(len(val)), val[:,1])
        self.BVP_plot.replot()

    def gsr_update(self):
        val = self.app.E4_dmgs[1].getSamples()
        self.GSR_plot.curve.setData(np.arange(len(val)),val[:,1])
        self.GSR_plot.replot()
        
    def tmp_update(self):  
        val = self.app.E4_dmgs[2].getSamples()
        self.TMP_plot.curve.setData(np.arange(len(val)),val[:,1])
        self.TMP_plot.replot()
#################### UPDATE GUI VALUES ############################################
    def set_cam_bufferSize(self):
        self.app.video_dmg.buffer.set_seconds(int(self.CAM_ComboBox.value()))
    
    def set_OpenBCI_bufferSize(self):
        self.app.eeg_dmg.EEG_buffer.update('seconds', int(self.EEG_ComboBox.value()))
        
    def set_E4_bufferSize(self, signal):
        if signal == 'BVP':
            self.app.E4_dmgs[0].buffer.set_seconds(int(self.BVP_ComboBox.value()))
        if signal == 'GSR':
            self.app.E4_dmgs[1].buffer.set_seconds(int(self.GSR_ComboBox.value()))
        if signal == 'TMP':
            self.app.E4_dmgs[2].buffer.set_seconds(int(self.TMP_ComboBox.value()))
        
    def set_tcpip(self):
        self.app.constants.set_tcpip(self.IP_TextEdit.text(), int(self.PORT_SpinBox.value()))      
        
    def set_E4_tcpip(self):
        self.app.constants.set_E4_tcpip(self.E4_ip_lineEdit.text())   
        
    def set_channel_spectrogram(self):
        self.initFrequencyView()
        
    def set_frequency(self):
        self.app.eeg_dmg.EEG_buffer.set_filter_range(self.frequency_ComboBox.currentText())  
        self.app.eeg_dmg.filter_bank.set_filters(self.app.eeg_dmg.EEG_buffer.LOWCUT, self.app.eeg_dmg.EEG_buffer.HIGHCUT)
    
    def set_order(self):
        self.app.eeg_dmg.EEG_buffer.update('order', int(self.butterOrder_SpinBox.value()))
        self.app.eeg_dmg.filter_bank.set_order(self.app.eeg_dmg.EEG_buffer.ORDER)
            
    def set_filtering(self):
        if self.app.BCI_streaming.value:
            self.eeg_timer.stop()      
            self.freq_timer.stop()
            self.eeg_short_timer.stop()
        self.app.eeg_dmg.EEG_buffer.update('method', self.filtering_ComboBox.currentText())  
        if self.app.BCI_streaming.value:
            self.eeg_timer.start(self.app.eeg_dmg.EEG_buffer.refresh_rate) 
            self.freq_timer.start(self.app.eeg_dmg.EEG_buffer.refresh_rate) 
            self.eeg_short_timer.start(self.app.eeg_dmg.EEG_buffer.short_refresh_rate) 

    def set_sampleSize(self):
        self.app.eeg_dmg.EEG_buffer.update('seconds', int(self.EEG_ComboBox.value()))
        self.app.eeg_dmg.EEG_buffer.reset(self.app.eeg_dmg.EEG_buffer.WINDOW)
        self.set_plots(reset = True)    
                
############ GUI interactions #################################################
    @QtCore.pyqtSlot(bool)  
    def device_connect_slot(self, device_connect):
        if device_connect:
            self.app.E4_driver.pause("ON")
        else:
            self.gui.log.myprint_error('The connection could not be established')
                
    @QtCore.pyqtSlot(list)  
    def device_list_slot(self, device_list):
        self.E4_device_ComboBox.clear()
        self.E4_device_ComboBox.addItems(device_list)
        
    @QtCore.pyqtSlot(bool)  
    def data_pause_slot(self, data_pause):
        if data_pause:
            self.start_bttn.setText("Start")
            self.E4_server_bttn.setEnabled(True)
            self.E4_connect_bttn.setEnabled(True)
        else:
            self.start_bttn.setText("Stop")
            self.E4_server_bttn.setEnabled(False)
            self.E4_connect_bttn.setEnabled(False)
        
    @QtCore.pyqtSlot(int)  
    def data_subscribe_slot(self, data_subscribe):
        if data_subscribe:
            self.contextView()
        else:
            self.app.log.myprint_error('Could not subscribe to all signals')
                    
################## SET GUI APPEARENCE #########################################
    def load_style(self): 
        self.styleQwtPlot("BVP",self.BVP_plot)
        self.styleQwtPlot("GSR",self.GSR_plot)
        self.styleQwtPlot("TMP",self.TMP_plot)        
        
        with open("QTDesigner/style.css") as f:
            self.app.setStyleSheet(f.read())
            
    def init_values(self):
        self.IP_TextEdit.setText(self.app.constants.ADDRESS)
        self.PORT_SpinBox.setProperty("value", self.app.constants.PORT)
        self.CAM_ComboBox.setProperty("value", self.app.video_dmg.buffer.CAMERA_SECONDS)
        self.initQwtCurves()
        self.initLongTermViewCurves()
        self.initShortTermViewCurves()
        self.initFrequencyView()
        self.set_plots()
        self.initFrequencyComboBox()
        self.initFilteringComboBox()
        self.initSpectrogramComboBox()
        self.load_style()
        self.show()
        
    def styleQwtPlot(self,name,elem):
        font = QFont()
        font.setPixelSize(12)
        title = QwtText(name)
        title.setFont(font)
        elem.setTitle(title)
        canvas = elem.canvas()
        canvas.setLineWidth(0);
        elem.setCanvas(canvas)
    
    def initQwtCurves(self):
        #BVP#
        self.BVP_plot.enableAxis(2,0)
        self.BVP_plot.curve = QwtPlotCurve()
        self.BVP_plot.curve.setPen(QPen(Qt.darkBlue))
        self.BVP_plot.curve.setStyle(QwtPlotCurve.Lines)
        self.BVP_plot.curve.setRenderHint(QwtPlotItem.RenderAntialiased)
        self.BVP_plot.curve.setPen(QPen(Qt.green))
        self.BVP_plot.curve.attach(self.BVP_plot)
        self.BVP_plot.setAutoReplot(False)
        #GSR#
        self.GSR_plot.enableAxis(2,0)
        self.GSR_plot.curve = QwtPlotCurve()
        self.GSR_plot.curve.setPen(QPen(Qt.darkBlue))
        self.GSR_plot.curve.setStyle(QwtPlotCurve.Lines)
        self.GSR_plot.curve.setRenderHint(QwtPlotItem.RenderAntialiased)
        self.GSR_plot.curve.setPen(QPen(Qt.green))
        self.GSR_plot.curve.attach(self.GSR_plot)
        self.GSR_plot.setAutoReplot(False)
        #TMP#
        self.TMP_plot.enableAxis(2,0)
        self.TMP_plot.curve = QwtPlotCurve()
        self.TMP_plot.curve.setPen(QPen(Qt.darkBlue))
        self.TMP_plot.curve.setStyle(QwtPlotCurve.Lines)
        self.TMP_plot.curve.setRenderHint(QwtPlotItem.RenderAntialiased)
        self.TMP_plot.curve.setPen(QPen(Qt.green))
        self.TMP_plot.curve.attach(self.TMP_plot)
        self.TMP_plot.setAutoReplot(False)
   
    def eeg_short_view(self):
        self.app.eeg_dmg.EEG_buffer.pos_ini, self.app.eeg_dmg.EEG_buffer.pos_end = self.lr.getRegion() 
        self.EEG_short_plot.setXRange(0, int(self.app.eeg_dmg.EEG_buffer.pos_end - self.app.eeg_dmg.EEG_buffer.pos_ini))
        self.EEG_short_plot.setLimits(xMin=0, xMax=int(self.app.eeg_dmg.EEG_buffer.pos_end - self.app.eeg_dmg.EEG_buffer.pos_ini))
        
    def set_plots(self, reset = False):
        channels = self.app.eeg_dmg.EEG_buffer.CHANNEL_IDS
        ### EEG plot settings ###
        self.EEG_plot.setLabel('bottom', 'Samples', units='n')
        self.EEG_plot.getAxis('left').setTicks([[(100, channels[0]), (200, channels[1]), (300, channels[2]), (400, channels[3]), (500, channels[4]), (600, channels[5]), (700, channels[6]), (800, channels[7])]])
        self.EEG_plot.setYRange(0, 900)
        self.EEG_plot.setXRange(0, self.app.eeg_dmg.EEG_buffer.LARGE_WINDOW)
        self.EEG_plot.showGrid(True, True, alpha = 0.3)
        self.EEG_plot.setLimits(xMin=0, xMax=self.app.eeg_dmg.EEG_buffer.LARGE_WINDOW)
        # Linear region settings #
        if not reset:
            self.lr = pg.LinearRegionItem([self.app.eeg_dmg.EEG_buffer.pos_ini,self.app.eeg_dmg.EEG_buffer.pos_end])
            self.EEG_plot.addItem(self.lr)
            self.lr.sigRegionChanged.connect(self.eeg_short_view)
            self.eeg_short_view()
        else:
            self.lr.setRegion([self.app.eeg_dmg.EEG_buffer.pos_ini,self.app.eeg_dmg.EEG_buffer.pos_end])
        ### EEG short view Plot settings ###
        self.EEG_short_plot.setLabel('bottom', 'Samples', units='n')
        self.EEG_short_plot.getAxis('left').setTicks([[(100, channels[0]), (200, channels[1]), (300, channels[2]), (400, channels[3]), (500, channels[4]), (600, channels[5]), (700, channels[6]), (800, channels[7])]])
        self.EEG_short_plot.setYRange(0, 900)
        self.EEG_short_plot.setXRange(0, int(self.app.eeg_dmg.EEG_buffer.pos_end - self.app.eeg_dmg.EEG_buffer.pos_ini))
        self.EEG_short_plot.showGrid(True, True, alpha = 0.3)
        self.EEG_short_plot.setLimits(xMin=0, xMax=int(self.app.eeg_dmg.EEG_buffer.pos_end - self.app.eeg_dmg.EEG_buffer.pos_ini))
        
    def initFrequencyComboBox(self):
        self.frequency_ComboBox.addItems(['Full','Delta','Theta','Alpha','Beta','Gamma'])
        
    def initSpectrogramComboBox(self):
        self.Spectrogram_ComboBox.addItems(self.app.eeg_dmg.EEG_buffer.CHANNEL_IDS)
       
    def initFilteringComboBox(self):
        self.filtering_ComboBox.addItems(['Butterworth'])
       
    def initLongTermViewCurves(self):
        ########################### EEG #####################################
        for i in range(self.app.eeg_dmg.EEG_buffer.CHANNELS):
            c = pg.PlotCurveItem(pen=(i,self.app.eeg_dmg.EEG_buffer.CHANNELS*1.3))
            c.setPos(0,0)
            self.EEG_plot.addItem(c)
            self.curves_EEG.append(c)
            
    def initShortTermViewCurves(self):
        ############ EEG short view ##########################
        for i in range(self.app.eeg_dmg.EEG_buffer.CHANNELS):
            c = pg.PlotCurveItem(pen=(i,self.app.eeg_dmg.EEG_buffer.CHANNELS*1.3))
            c.setPos(0,0)
            self.EEG_short_plot.addItem(c)
            self.curves_EEG_short.append(c)
            
    def initFrequencyView(self):
        self.curves_Freq = []
        self.Frequency_plot.clear()
        
        if self.Spectrogram_RadioButton.isChecked():
            self.Frequency_plot.showGrid(True, True, alpha = 0)
            self.Frequency_plot.setLogMode(False, False)
            self.Frequency_plot.setLabel('left', 'Frequency', units='Hz')
            self.Frequency_plot.setLabel('bottom', "Samples", units='n')
            
            self.spectrogram_Img = pg.ImageItem()     
            self.Frequency_plot.addItem(self.spectrogram_Img)

            pos = np.array([0.0, 0.5, 1.0])
            color = np.array([[0,0,0,255], [255,128,0,255], [255,255,0,255]], dtype=np.ubyte)
            map = pg.ColorMap(pos, color)
            lut = map.getLookupTable(0.0, 1.0, 256)           
            self.spectrogram_Img.setLookupTable(lut)
            
        else:   
            ### FREQUENCY Plot settings ###
            self.Frequency_plot.showGrid(True, True, alpha = 0.3)
            self.Frequency_plot.setLogMode(False, True)
            self.Frequency_plot.setLabel('left', 'Amplitude', units='dB')
            self.Frequency_plot.setLabel('bottom', "Frequency", units='Hz')
            
            for i in range(self.app.eeg_dmg.EEG_buffer.CHANNELS):
                c = pg.PlotCurveItem(pen=(i,self.app.eeg_dmg.EEG_buffer.CHANNELS*1.3))
                self.Frequency_plot.addItem(c)
                self.curves_Freq.append(c)
