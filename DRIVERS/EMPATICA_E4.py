# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo)s
@email: %(mikel1982mail@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED))
"""
#%%
from threading import Event, Thread
import socket
import time
from DRIVERS.communication_signals import empatica_signals
from GENERAL import preprocessing as pre

class E4_socket(Thread):
    
    def __init__(self, E4_connected, dmgs, callbacks):
        #Process class overwritten
        Thread.__init__(self) 
        ### data manager ####
        self.dmgs = dmgs
        self.exit = Event()
        self.flag = Event()
        ### communication signals and values #######
        self.com_signals = empatica_signals()
        self.com_signals.connect(callbacks)
        self.device_list = []
        self.E4_connected = E4_connected
        self.device_connect = False
        self.data_pause = False
        self.data_subscribe = 0
        self.stream_subscribe = [False, False, False, False]
        self.count_subscribe = 0
        self.error_subscribe = False
        
    def run(self):
        msg = ''
        while not self.exit.is_set():
            msg += self.sock.recv(8).decode('utf8')
            msg,lines = pre.extractMessages(msg)
            if len(lines):
                for i in range(0,len(lines)):
                    #message
                    if lines[i][0] == 'R':
                        #enviamos a log
                        self.log.myprint_in(lines[i])
                        #analizamos mensaje
                        head,message = pre.extractHead(lines[i])
                        if head == "device_list":
                            self.device_list = pre.extractDevice(message)
                            self.com_signals.device_list_emit(self.device_list)
                        elif head == "device_connect":
                            if message[0] == "OK":
                                self.device_connect = True
                            elif message[0] == "ERR":
                                self.log.myprint_error(message[1]+'\r\n') 
                            self.com_signals.device_connect_emit(self.device_connect)
                        elif head == "device_disconnect":
                            if message[0] == "OK":
                                self.device_connect = False
                            elif message[0] == "ERR":
                                self.log.myprint_error(message[1]+'\r\n')
                            self.com_signals.device_connect_emit(self.device_connect)
                        elif head == "pause":
                            if message[0] == "ON":
                                self.data_pause = True
                            elif message[0] == "OFF":
                                self.data_pause = False
                            elif message[0] == "ERR":
                                self.log.myprint_error(message[1]+'\r\n') 
                            self.com_signals.data_pause_emit(self.data_pause)
                        elif head == "device_subscribe":
                            self.count_subscribe += 1
                            #comprobamos señal
                            if message[0] == "bvp":
                                ind = 0
                            elif message[0] == "gsr":
                                ind = 1
                            elif message[0] == "tmp":
                                ind = 2
                            elif message[0] == "acc":
                                ind = 3
                            else:
                                ind = -1
                            #comprobamos subscripcion
                            if message[1] == "ERR":
                                self.error_subscribe = True
                                self.log.myprint_error(message[2]+'\r\n')
                            elif ind == -1:
                                self.error_subscribe = True
                                self.log.myprint_error('The stream is not identified\r\n')
                            else:
                                self.stream_subscribe[ind] = True
                            #Comprobamos si se recibieron las cuatro subcripciones y emitimos señal
                            if self.count_subscribe == 4:
                                self.count_subscribe = 0
                                if self.error_subscribe:
                                    self.data_subscribe = -1
                                else:
                                    if self.stream_subscribe[0] and self.stream_subscribe[1] and self.stream_subscribe[2] and self.stream_subscribe[3]:
                                        self.data_subscribe = 1
                                    else:
                                        self.data_subscribe = 0
                                self.com_signals.data_subscribe_emit(self.data_subscribe)
                        else:   
                            self.log.myprint_error('The message '+head+' is unknown\r\n')
    
                    #Data stream
                    else:                   
                        if lines[i][0:6] == 'E4_Bvp': #Aunque seria interesante un case que en python no lo hay
                            ind =  0
                        elif lines[i][0:6] == 'E4_Gsr':
                            ind =  1
                        elif lines[i][0:6] == 'E4_Tem':
                            ind =  2
                        elif lines[i][0:6] == 'E4_Acc':
                            ind =  3
                        else:
                            ind =  -1
                            
                        if ind >= 0:
                            data = pre.extractData(lines[i])
                            self.dmgs[ind].appendSample(data)
                            
                            if self.flag.is_set():
                                self.dmgs[ind].allData.append(data)
                    

            
        # finally           
        self.log.myprint('Killing thread')
        print('E4 driver is killed')
         
    def set_logger(self, log):
        self.log = log 
        
    def listDevice(self):
        message = 'device_list\r\n'
        self.send_msg(message)
        
    def connectDevice(self,device):
        message = 'device_connect '+device+'\r\n'
        self.send_msg(message)
        
    
    def disconnectDevice(self):
        message = 'device_disconnect\r\n'
        self.send_msg(message)
        
    def pause(self, state):
        message = 'pause ' + state +'\r\n' 
        self.send_msg(message)
        
    def subscribe(self,action):
        for dmg in self.dmgs:
            message = 'device_subscribe '+ dmg.SIGNAL + ' ' + action +'\r\n' 
            self.send_msg(message)
            time.sleep(0.1)
        
    def openPort(self, IP, PORT):
        # self.log.myprint("Trying to connect with Empatica server")
        print('paso 1')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('paso 2')
        # self.log.myprint('Create socket')
        server_address = (IP, PORT)
        print('paso 3')
        # self.log.myprint('Socket on ip and port initialized')
        self.sock.connect(server_address)
        print('paso 4')
        self.E4_connected.value = True
        # self.log.myprint("Connected to Empatica Server")
        
          
    def closePort(self): 
        self.sock.close() #Cerramos el socket
        self.E4_connected.value = False
        self.log.myprint("Connection closure with the Empatica Server")
        
        
    def send_msg(self,message):
        self.log.myprint_out(message[0:len(message)-2])
        self.sock.send(message.encode('utf-8'))
        
    def kill(self):
        self.closePort()
        self.exit.set() 
        self.log.myprint("Destroying E4 socket thread instance")
 