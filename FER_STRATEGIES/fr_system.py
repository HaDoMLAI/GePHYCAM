# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo)s
@email: %(mikel1982mail@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED))
"""

from faced.detector import FaceDetector
import cv2
import numpy as np


class FR_system:
    
    def __init__(self):
        self.face_detector = FaceDetector()
        self.thresh=0.6
        
    def face_cropping(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        bboxes = self.face_detector.predict(frame, self.thresh)  
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if len(bboxes):
            bbox = bboxes[0]
            x_c, y_c, width, height = bbox[0], bbox[1], bbox[2], bbox[3]
            x, y = int(x_c - width / 2), int(y_c - height / 2)
            # preprocess image before prediction
            roi_gray = frame[y:y + height, x:x + width]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
            cropped_img = cropped_img / 255.
            
            return cropped_img
    
    