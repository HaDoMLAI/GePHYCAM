#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 18:03:01 2020

@author: anaiak
"""
#%%
import numpy as np
import matplotlib.pyplot as plt
#%%
trial = 14
user = 'prueba'
a = np.load('./data_test/'+user+'_bvp_trial_'+str(trial)+'.npy')

a.shape

plt.plot(a[:,1])
print('bvp -> ', (len(a[:,1])/64)//60, (len(a[:,1])/64)%60)

a = np.load('./data_test/'+user+'_gsr_trial_'+str(trial)+'.npy')

a.shape

plt.plot(a[:,1])
print('gsr -> ', (len(a[:,1])/4)//60 , (len(a[:,1])/4)%60)

a = np.load('./data_test/'+user+'_tmp_trial_'+str(trial)+'.npy')

a.shape

plt.plot(a[:,1])
print('tmp -> ', (len(a[:,1])/4)//60 , (len(a[:,1])/4)%60)

a = np.load('./data_test/'+user+'_EEG_trial_'+str(trial)+'.npy')

a.shape

plt.plot(a[:,1])
print('eeg -> ', (len(a[:,1])/250)//60 , (len(a[:,1])/250)%60)