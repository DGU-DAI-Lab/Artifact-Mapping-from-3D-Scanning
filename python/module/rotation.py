#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ====================================================
# 
# Module : Rotation
#
# Written by hepheir@gmail.com
# Last updated : Oct 27 2019
#
# ====================================================

import numpy as np
import cv2

# ====================================================

THICKNESS = 2
COLOR_WHITE = (0xFF, 0xFF, 0xFF)
COLOR_PRIMARY = (0xFF, 0xFF, 0x00)
COLOR_SECONDARY = (0x00, 0xFF, 0xFF)

# ====================================================

def byBoundingBox(image,showbox=False):
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    center = (gray.shape[0]//2, gray.shape[1]//2)
    # 1. Get Body Contour
    _, th = cv2.threshold(gray, 245, 255, cv2.THRESH_BINARY_INV)
    cont,_ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # 2. Get the Smallest Bounding Box
    rect = cv2.minAreaRect(cont[0])
    if showbox:
        box = np.int0(cv2.boxPoints(rect))
        image = cv2.drawContours(image,[box],-1,COLOR_PRIMARY,thickness=THICKNESS)
    # 3. Get the Rotation Matrix and Apply the mat.
    _,_,rad = rect
    rmat = cv2.getRotationMatrix2D(center, rad, 1)
    rotated = cv2.warpAffine(image, rmat, gray.shape)
    return rotated

# ====================================================

def byHoughTransform(image,showline=False):
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    center = (gray.shape[0]//2, gray.shape[1]//2)
    lines = cv2.HoughLines(image, 1, np.pi/180, 100)
    # ------------------------------------------------
    # TODO: Decide which line will be the reference.
    line = lines[0]
    # ------------------------------------------------
    rho,theta = line[0]
    if showline:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 +1000*(-b))
        y1 = int(y0 +1000*(a))
        x2 = int(x0 -1000*(-b))
        y2 = int(y0 -1000*(a))
        cv2.line(image,(x1,y1),(x2,y2),COLOR_PRIMARY,1)
    rmat = cv2.getRotationMatrix2D(center, (theta*180/np.pi), 1)
    rotated = cv2.warpAffine(image, rmat, gray.shape)
    return rotated

# ====================================================

def Rotate_Direct(image, degree):
    size = image.shape[:2]
    center = (size[0]//2, size[1]//2)
    rmat = cv2.getRotationMatrix2D(center, degree, 1)
    rotated = cv2.warpAffine(image, rmat, size)
    return rotated