#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ============================================
# 
# Module : Graphical User Interface using Tkinter
#
# Written by hepheir@gmail.com
# Last updated: Oct 27, 2019
#
# ============================================

import tkinter as tk
import numpy as np
import cv2
from PIL import ImageTk, Image

# ============================================

WINDOW_SHAPE = (640, 480) # (w, h)
IMAGE_FRAME_SHAPE = (480, 480) # (w, h)

# ============================================

def updateImage_fromCv2(cv2_img):
    cv_im = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    cv_im = cv2.resize(cv_im, IMAGE_FRAME_SHAPE)
    tk_im = ImageTk.PhotoImage(Image.fromarray(cv_im))
    updateImage(tk_im)

def updateImage(tk_img):
    global fl__l
    fl__l.configure(image=tk_img)
    fl__l.image=tk_img

def mainloop():
    global root
    root.mainloop()
# ============================================

###############[root]################
#                   #               #
#                   #               #
#                   #               #
#                   #               #
#      Content      #     Aside     #
#       Frame       #     Frame     #
#                   #               #
#                   #               #
#                   #               #
#####################################

# ============================================

root = tk.Tk()
root.title("Contour Extraction of Pottery Relics (by Dept. of EICE. 2019)")
root.geometry("%dx%d+100+100" % WINDOW_SHAPE)
root.resizable(False,False)

# ============================================

fl = tk.Frame(root,
    bg = "black",
    width  = IMAGE_FRAME_SHAPE[0],
    height = IMAGE_FRAME_SHAPE[1]
)
fl__l = tk.Label(fl,
    text="label"
)
fl__l.pack(fill="both",expand=False)
fl.pack_propagate(False)
fl.pack(side="left",fill="both",expand=False)

fr = tk.Frame(root,
    bg="lightgray"
)
fr.pack(side="right",fill="both",expand=True)

# ============================================
