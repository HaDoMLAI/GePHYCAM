# GePHYCAM: GENERAL PHYSIOLOGICAL and CAMERA FOR REAL-TIME RECORDINGS AND PROCESSING
In order to record and collect the data, a self-produced software, GePHYCAM, is
developed. This application looks forward to being accessible to the whole scientific
community, providing a resourceful tool for human-behaviour experimental paradigms,
covering the following functionalities:

1. Real-time acquisition and visualisation of EEG, BVP, GSR, TMP and WEBCAM
signals.
2. Trigger synchronisation by a tcp/ip interface which allows start/stop recordings
remotely.
3. Data recording on EDF file format for electrophysiological signals and MP4 file
format for the audio-visual signals.
4. Online behaviour labelling interface which labels are synchronised and stored on
EDF files.

# APP:
![Image description](https://github.com/mikelval82/GePHYCAM/blob/master/images/GePHYCAM.png)

# DEPENDENCIES:
```
PythonQwt
pyserial
neurodsp
PyQt5
pyqtwebengine
scikit-learn
pandas
ica
scipy
pyqtgraph
pyEDFlib
PyWavelets
lspopt
spectrum
pyhrv
opencv-python
pyedflib
ffmpeg-python
```

# USE EXAMPLE:
1) add permissions: 
```
sudo chmod 666 /dev/ttyUSB0 (your serial port)
```
2) Run in one terminal:
```
python MULTIMODAL_APP_00.py
```
3) Set the user filename

4) Set IP and PORT in the app and click the trigger button

5) Run in another terminal:
```
python
```
6) Create a client
```
from COM.trigger_client import trigger_client

tc = trigger_client('IP','PORT')
tc.create_socket()
tc.connect()
```
Then you are ready to start the recording.

```
tc.send_msg(b'start')
```
Labels can be sent asynchronously during the recording and will be stored as events in the EDF user file.

```
tc.send_msg(b'happy')
```

To stop the recording and save the temporal series in the user EDF file.

```
tc.send_msg(b'stop')
```

# CITATION:
@DOI: 10.5281/zenodo.3727503 

# AUTHOR DETAILS AND CONTACT
Author: Mikel Val Calvo
Institution: Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED)
Email: mikel1982mail@gmail.com

