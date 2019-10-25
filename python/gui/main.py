# !user/bin/env/python

##
# Wrote by hepheir@gmail.com
# Last updated: Oct 25, 2019

import tkinter as tk
import cv2
from PIL import ImageTk, Image
# ============================================

TEST_IMAGE_PATH = 'test_model/2ds-preproc/토기2/all.png'
IMAGE_SHAPE = (480, 480) # (h, w)

# ============================================

def debug():
    im = cv2.imread(TEST_IMAGE_PATH)
    updateImage_cv2(im)

def updateImage_cv2(cv2Image):
    cv_im = cv2.cvtColor(cv2Image, cv2.COLOR_BGR2RGB)
    cv_im = cv2.resize(cv_im, IMAGE_SHAPE)
    tk_im = ImageTk.PhotoImage(Image.fromarray(cv_im))
    callback__updateImage(tk_im)

def callback__updateImage(img):
    global fl__l
    fl__l.configure(image=img)
    fl__l.image = img

# ============================================

root = tk.Tk()
root.title("by Hepheir, 2019")
root.geometry("640x480+100+100")
root.resizable(False,False)

# ============================================

fl = tk.Frame(root,bg="black",width=IMAGE_SHAPE[0],height=IMAGE_SHAPE[1])
fl__l = tk.Label(fl, text="")
fl.pack_propagate(False)

fl__l.pack(fill="both",expand=False)
fl.pack(side="left",fill="both",expand=False)
# --------------------------------------------
fr = tk.Frame(root,bg="lightgray")

fr.pack(side="right",fill="both",expand=True)

# ============================================

debug()
root.mainloop()