#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
create images
"""
import cv2
import glob
import numpy as np
import os

ids = os.listdir('images/abs/')

abs_list = []
for filename in glob.glob('images/abs/*.png'): 
    im = cv2.imread(filename, 0) # 0 to open as grey which will be just one channel
    im = cv2.resize(im, (224,224))
    abs_list.append(im)

mag_list = []
for filename in glob.glob('images/mag/*.png'): 
    im = cv2.imread(filename, 0)
    im = cv2.resize(im, (224,224))
    mag_list.append(im)

pha_list = []
for filename in glob.glob('images/pha/*.png'): 
    im = cv2.imread(filename, 0)
    im = cv2.resize(im, (224,224))
    pha_list.append(im)

peak_list = []
for filename in glob.glob('images/peak/*.png'): 
    im = cv2.imread(filename, 0)
    im = cv2.resize(im, (224,224))
    peak_list.append(im)

amb_list = []
for filename in glob.glob('images/amb/*.png'): 
    im = cv2.imread(filename, 0)
    im = cv2.resize(im, (224,224))
    amb_list.append(im)

# make images with 3 channels
abs_ims = [] 
for i in range(0, len(abs_list)):
    ch1 = abs_list[i]
    ch2 = abs_list[i]
    ch3 = abs_list[i]
    im = np.stack([ch1, ch2, ch3], axis=2)
    abs_ims.append(im)

wai_ims = [] 
for i in range(0, len(abs_list)):
    ch1 = abs_list[i]
    ch2 = mag_list[i]
    ch3 = pha_list[i]
    im = np.stack([ch1, ch2, ch3], axis=2)
    wai_ims.append(im)
    
wbt_ims = [] 
for i in range(0, len(abs_list)):
    ch1 = abs_list[i]
    ch2 = peak_list[i]
    ch3 = amb_list[i]
    im = np.stack([ch1, ch2, ch3], axis=2)
    wbt_ims.append(im)
    
# save images
for i in range(0, len(abs_ims)):
    im = abs_ims[i]
    id = ids[i]
    path = 'images_for_model/abs/' + id
    cv2.imwrite(path, im)

for i in range(0, len(wai_ims)):
    im = wai_ims[i]
    id = ids[i]
    path = 'images_for_model/wai/' + id
    cv2.imwrite(path, im)

for i in range(0, len(wbt_ims)):
    im = wbt_ims[i]
    id = ids[i]
    path = 'images_for_model/wbt/' + id
    cv2.imwrite(path, im)



