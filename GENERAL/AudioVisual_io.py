# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo)s
@email: %(mikel1982mail@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED))
"""
#%%
from GENERAL.audio_constants import audio_constants as ac
from GENERAL.video_constants import video_constants as vc
import wave
import pyaudio
import cv2
import subprocess
import os 
import numpy as np
import ffmpeg

audio_constants = ac()
video_constants = vc()

def write_audioTemp(audio_frames):
    print('Writting audio temporal file')
    waveFile = wave.open(audio_constants.temp, 'wb')
    waveFile.setnchannels(audio_constants.channels)
    waveFile.setsampwidth(pyaudio.PyAudio().get_sample_size(audio_constants.format))
    waveFile.setframerate(audio_constants.rate)
    waveFile.writeframes(b''.join(audio_frames))
    waveFile.close()
    
def vidwrite(images, framerate=30, vcodec='libx264'):
    if not isinstance(images, np.ndarray):
        images = np.asarray(images)
    n,height,width,channels = images.shape
    process = (
        ffmpeg
            .input('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(width, height))
            .output('./data/temp_video.avi', pix_fmt='yuv420p', vcodec=vcodec, r=framerate)
            .overwrite_output()
            .run_async(pipe_stdin=True)
    )
    for frame in images:
        process.stdin.write(
            frame
                .astype(np.uint8)
                .tobytes()
        )
    process.stdin.close()
    process.wait()
    
def remove_temps():
	os.remove("./data/temp_audio.wav")
	os.remove("./data/temp_video.avi")
        
def write_AV(audio_frames, video_frames, path, trial):
    try:
        remove_temps()
    except:
        pass
    try:
        vidwrite(video_frames)
        write_audioTemp(audio_frames)
        print('Temporal files succesfully writted')
        output = path + '_' + trial + '.mp4'
        print('Writting movie in: ', output)
        cmd = "ffmpeg -i " + path + "temp_video.avi" + " -i " + path + "temp_audio.wav -c:v copy -c:a aac -strict experimental " + output
        subprocess.call(cmd, shell=True)
        print('Finish writting movie')
    except:
        print('Cannot write AV file.')
