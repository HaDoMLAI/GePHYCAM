# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo)s
@email: %(mikel1982mail@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED))
@DOI: 10.5281/zenodo.3727503 
"""
#%%
from GENERAL.audio_constants import audio_constants
from multiprocessing import Process, Event
import pyaudio
import time

class AudioRecorder(Process, audio_constants):

    def __init__(self, audio_queue, streaming):
        Process.__init__(self) 
        audio_constants.__init__(self)
        # -- streaming --
        self.streaming = streaming
        self.audio_queue = audio_queue
        # -- flag --
        self.flag = Event()
        self.flag.set()
        
    def run(self):
        print('audio thread started')
        # -- settings --
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,input=True,
                                      frames_per_buffer=self.frames_per_buffer)
        print('audio streaming started')
        while self.flag.is_set():  
            if self.streaming.value:
                data = self.stream.read(self.frames_per_buffer) 
                self.audio_queue.put(data)
            else:                
                while not self.audio_queue.empty():  
                    self.audio_queue.get()
                time.sleep(.001)
                    
        print('killing audio recorder')
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        print('audio recorder killed')
   
    def kill(self):
        self.flag.clear()

