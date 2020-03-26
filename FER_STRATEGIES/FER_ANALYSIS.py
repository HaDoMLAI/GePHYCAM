# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo)s
@email: %(mikel1982mail@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED))
"""

#%%
from faced.detector import FaceDetector
from tensorflow.compat.v1.keras.models import load_model
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

import numpy as np
import cv2
import time

def predict_by_ensemble(models, image):
    tic=time.time()
    outputs = [model.predict(image) for model in models]
    ensemble_prediction = np.sum(outputs,axis=0)/len(outputs)
    prediction = np.argmax(ensemble_prediction)
    toc=time.time()
    time_spent = float("{0:.2f}".format((toc - tic) * 1000))
    return prediction, time_spent,ensemble_prediction

conv_pool_cnn_modelA=load_model('./models/conv_pool_cnnA_merged_fer68,74_ck97,42_.h5')
conv_pool_cnn_modelB=load_model('./models/conv_pool_cnnB_merged_fer67,96_ck96,13_.h5')
conv_pool_cnn_modelC=load_model('./models/conv_pool_cnnC_merged_fer67,90_ck98,71_.h5')

Model_ABC=[conv_pool_cnn_modelA,conv_pool_cnn_modelB,conv_pool_cnn_modelC]

emotion_dict = {0: "Angry", 1: "Disgust", 2: "Fear", 3: "Happy", 4: "Sad", 5: "Surprise", 6: "Neutral"}
thresh=0.5
#%%
cap = cv2.VideoCapture('./RECORDINGS/lidia/lidia_WEBCAM_trial_5.mp4')

face_detector = FaceDetector()
while True:
    ret, frame = cap.read()
    print(frame.shape)
    t1=time.time()
    rgb_img= cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    bboxes = face_detector.predict(rgb_img, thresh)
    bbox = bboxes[0]
    x_c, y_c, w, h = bbox[0], bbox[1], bbox[2], bbox[3]
    x, y = int(x_c - w / 2), int(y_c - h / 2)
    
    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 1)
    
    gray= cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)
    roi_gray = gray[y:y + h, x:x + w]
    cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
    cropped_img = cropped_img/255.
    prediction, time_spent,outputs=predict_by_ensemble(Model_ABC,cropped_img)
    
    
    t2=time.time()
    t = float("{0:.2f}".format((t2 - t1) * 1000))
    cv2.putText(frame, emotion_dict[int(prediction)], (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(frame, str(time_spent) + ' ms for prediction', (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1,
                cv2.LINE_AA)
    cv2.putText(frame, str(t) + ' ms for whole system with YOLO', (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1,
                cv2.LINE_AA)
    cv2.putText(frame, ' Angry : '+str("{0:.2f} %".format(outputs[0][0]*100)), (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),
                1,
                cv2.LINE_AA)
    cv2.putText(frame, ' Disgust : ' + str("{0:.2f} %".format(outputs[0][1] * 100)), (30, 100), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 0, 0),
                1,
                cv2.LINE_AA)
    cv2.putText(frame, ' Fear : ' + str("{0:.2f} %".format(outputs[0][2] * 100)), (30, 120), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 0, 0),
                1,
                cv2.LINE_AA)
    cv2.putText(frame, ' Happy : ' + str("{0:.2f} %".format(outputs[0][3] * 100)), (30, 140), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 0, 0),
                1,
                cv2.LINE_AA)
    cv2.putText(frame, ' Sad : ' + str("{0:.2f} %".format(outputs[0][4] * 100)), (30, 160), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 0, 0),
                1,
                cv2.LINE_AA)
    cv2.putText(frame, ' Surprise : ' + str("{0:.2f} %".format(outputs[0][5] * 100)), (30, 180), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 0, 0),
                1,
                cv2.LINE_AA)
    cv2.putText(frame, ' Neutral : ' + str("{0:.2f} %".format(outputs[0][6] * 100)), (30, 200),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 0, 0),
                1,
                cv2.LINE_AA)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()