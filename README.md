# DESCRIPTION:
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

# INSTRUCTIONS:
1) Install requirements as explained in installation_steps.txt
2) add permissions: sudo chmod 666 /dev/ttyUSB0 (your serial port)
3) In the folder ./GENERAL/constants.py tcp/ip ADDRESS must be set: '10.1.25.82' (your IP)
4) Run MULTIMODAL_APP_00.py

# CITATION:
@DOI: 10.5281/zenodo.3727503 

# AUTHOR DETAILS AND CONTACT
author: Mikel Val Calvo
institution: Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED)
email: mikel1982mail@gmail.com
