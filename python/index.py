# -*- coding: utf-8 -*-

""" Required libraries.
Built using python 3.7

numpy
numpy-stl
opency-python
pillow
"""

import numpy as np
import cv2

import module.gui as gui
import module.windowDetection as wd

# ============================================

TEST_IMAGE_PATH = 'test_model/2ds-preproc/토기2/outer.png'

# ============================================

def readUnicodePath(path):
    # `cv2.imread()`와 같은 기능을 가진 함수. 
    # `cv2.imread()`와 달리, 한국어 등의 유니코드로 이루어진 경로도 읽을 수 있음.
    stream = open(path,"rb")
    bytes = bytearray(stream.read())
    numpyArray = np.asarray(bytes,dtype=np.uint8)
    img_bgr = cv2.imdecode(numpyArray, cv2.IMREAD_UNCHANGED)
    return img_bgr

# ============================================

im = readUnicodePath(TEST_IMAGE_PATH)
output = wd.macro(im)

gui.updateImage_fromCv2(output[0])
gui.mainloop()