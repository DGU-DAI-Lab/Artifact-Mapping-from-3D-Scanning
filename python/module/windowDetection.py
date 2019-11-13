#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ============================================
# 
# Module : 2D Window Auto Detection
#
# Written by hepheir@gmail.com
# Last updated : Oct 27 2019
#
# ============================================
#
#  Process order
#
#  1. Extract Body Mask
#  2. Extract Window Masks
#  3. Mask Dilation
#  4. Extract Window Masks with their frames
#
# ============================================

import cv2
import numpy as np

# ============================================

CANNY_THRESH = (78, 188)

DILATION_KERNEL_TYPE = cv2.MORPH_ELLIPSE
DILATION_KERNEL_SIZE = (99,99)

MIN_AREA = 30
    
# ============================================

def macro(color_image):
    gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
    # Get window masks with their frames
    body_mask = extract_body_mask(gray_image)
    window_masks = extract_window_masks(body_mask)
    dilated_win_masks = dilate_window_masks(window_masks)
    # Apply mask images
    win_masks_w_frames = [cv2.bitwise_and(color_image,color_image, mask=m) for m in dilated_win_masks]
    return win_masks_w_frames

# ============================================

def extract_body_mask(gray_image):
    # image background should've been removed.
    _,th = cv2.threshold(gray_image, 250,255, cv2.THRESH_BINARY_INV)
    return cv2.morphologyEx(th, cv2.MORPH_CLOSE,(5,5), iterations=3)

def extract_window_masks(body_mask):
    cont,hier = cv2.findContours(body_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    window_contours = []
    for i in range(len(cont)):
        c,h = cont[i], hier[0,i]
        if not h[3] < 0:
            window_contours.append(c)
    zeros = np.zeros(body_mask.shape[:2], dtype=np.uint8)
    window_masks = [cv2.drawContours(zeros.copy(), [c], -1, 255, -1) for c in window_contours]
    return window_masks

def dilate_window_masks(window_masks):
    global DILATION_KERNEL_TYPE, DILATION_KERNEL_SIZE
    kernel = cv2.getStructuringElement(DILATION_KERNEL_TYPE,DILATION_KERNEL_SIZE)
    dilated_masks = [cv2.dilate(m,kernel) for m in window_masks]
    return dilated_masks