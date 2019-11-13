#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ====================================================
# 
# Contour Extraction of Pottery Relics (by Dept. of EICE. 2019)
#
# Written by hepheir@gmail.com
# Last updated: Oct 27, 2019
#
# ====================================================
# 
# Developed with Python 3.x
# using OpenCV 4.0
#
# Required Libraries:
# * numpy
# * numpy-stl
# * opency-python
# * pillow
# 
# ====================================================

import numpy as np
import cv2

import module.gui as gui
import module.rotation as r
import module.windowDetection as wd

# ====================================================

TEST_IMAGE_PATH = 'test_model/2ds-preproc/토기2/inner.png' # 'test_model/1.jpg' #

# ====================================================

def readUnicodePath(path):
    # `cv2.imread()`와 같은 기능을 가진 함수. 
    # `cv2.imread()`와 달리, 한국어 등의 유니코드로 이루어진 경로도 읽을 수 있음.
    stream = open(path,"rb")
    bytes = bytearray(stream.read())
    numpyArray = np.asarray(bytes,dtype=np.uint8)
    img_bgr = cv2.imdecode(numpyArray, cv2.IMREAD_UNCHANGED)
    return img_bgr

# ====================================================


print("Booting...")
im = readUnicodePath(TEST_IMAGE_PATH)

gui.updateImage_fromCv2(im)

print("Starting mainloop...")
gui.mainloop()




"""
im = readUnicodePath(TEST_IMAGE_PATH)
# im = r.byBoundingBox(im,True)
output = np.zeros(im.shape[:2], dtype=np.uint8)


gray_image = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
# Get window masks with their frames
body_mask = wd.extract_body_mask(gray_image)
window_masks = wd.extract_window_masks(body_mask)
dilated_win_masks = wd.dilate_window_masks(window_masks)
# Apply mask images
win_masks_w_frames = [cv2.bitwise_and(im,im, mask=m) for m in dilated_win_masks]


for i in range(len(win_masks_w_frames)):
    w = win_masks_w_frames[i]
    w = cv2.cvtColor(w, cv2.COLOR_BGR2GRAY)
    w = cv2.Canny(w, 78,188,apertureSize=3)
    w = cv2.morphologyEx(w, cv2.MORPH_CLOSE, (5,5))

    conts = cv2.findContours(w,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)[0]
    conts_th = []
    black = np.zeros(im.shape[:2], dtype=np.uint8)
    for c in conts:
        if cv2.contourArea(c) > 20:
            cv2.drawContours(black, [c], -1, 255, 1)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    black = cv2.add(black,black,mask= cv2.erode(dilated_win_masks[i],kernel,iterations=3)) #
    output = cv2.add(output, black)

bc, _ = cv2.findContours(body_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
cv2.drawContours(output, bc, -1, 255, 1)

cv2.imshow('result', output)
cv2.waitKey(0)
"""