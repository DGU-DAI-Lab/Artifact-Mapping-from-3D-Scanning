# !user/bin/env/python

##
# Wrote by hepheir@gmail.com
# Last updated: Oct 25, 2019

import tkinter as tk
import numpy as np
import cv2
from PIL import ImageTk, Image
# ============================================

TEST_IMAGE_PATH = 'test_model/2ds-preproc/토기2/all.png'
IMAGE_SHAPE = (480, 480) # (h, w)

# ============================================
 
def debug():
    im = readUnicodePath(TEST_IMAGE_PATH)
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

def readUnicodePath(path):
    # `cv2.imread()`와 같은 기능을 가진 함수. 
    # `cv2.imread()`와 달리, 한국어 등의 유니코드로 이루어진 경로도 읽을 수 있음.
    stream = open(path,"rb")
    bytes = bytearray(stream.read())
    numpyArray = np.asarray(bytes,dtype=np.uint8)
    img_bgr = cv2.imdecode(numpyArray, cv2.IMREAD_UNCHANGED)
    return img_bgr

# ============================================

class Window:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("by Hepheir, 2019")
        self.root.geometry("640x480+100+100")
        self.root.resizable(False,False)
        self.hierarchy = [
            self.root
        ]

    def init_left_frame(self):
        fl = tk.Frame(self.root,
            bg = "black",
            width = IMAGE_SHAPE[0],
            height = IMAGE_SHAPE[1]
        )
        fl__l = tk.Label(fl, text="")
        fl.pack_propagate(False)
        self.hierarchy.append([fl,[fl__l]])

        fl__l.pack(fill="both",expand=False)
        fl.pack(side="left",fill="both",expand=False)

# ============================================


# --------------------------------------------
fr = tk.Frame(root,bg="lightgray")

fr.pack(side="right",fill="both",expand=True)

# ============================================

debug()
root.mainloop()