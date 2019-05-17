import cv2
import numpy as np

from tkinter import filedialog as fd

path = fd.askopenfilename()

filename = 'c'

def readUnicodePath(path):
    stream = open(path,"rb")
    bytes = bytearray(stream.read())
    numpyArray = np.asarray(bytes,dtype=np.uint8)
    img_bgr = cv2.imdecode(numpyArray, cv2.IMREAD_UNCHANGED)
    return img_bgr

img = readUnicodePath(path)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Smoothing
GAUSS_KERNEL_SIZE = 3
GAUSS_SIGMA = 25

# 1. 전처리 - 노이즈제거 (Blurring) : 가우시안 필터 적용
blurred = cv2.GaussianBlur(gray, (GAUSS_KERNEL_SIZE,GAUSS_KERNEL_SIZE), GAUSS_SIGMA)


# 2-A1 - opt1. 임계처리
THRESH = 240
ret, threshed = cv2.threshold(blurred.copy(), THRESH, 255, cv2.THRESH_BINARY_INV)

# 2-A2. 후처리 - 점 노이즈제거 (Blurring) : Morphology - Opening
morphed = cv2.morphologyEx(threshed, cv2.MORPH_OPEN, (5,5), iterations=4)

# 2-A3
contours, hierarchy = cv2.findContours(morphed, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

for length in range(1,3):
    canvas = np.zeros(gray.shape, np.uint8)
    cv2.drawContours(canvas, contours, -1, 255, length)
    cv2.imwrite("../%s_oldway_thresh%d.jpg"%(filename,length), canvas)

# 2-B1 - opt2. Edge 검출
edge = cv2.Canny(blurred, 50, 150, apertureSize=3)

# 2-B2
contours, hierarchy = cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

for length in range(1,3):
    canvas = np.zeros(gray.shape, np.uint8)
    cv2.drawContours(canvas, contours, -1, 255, length)
    cv2.imwrite("../%s_oldway_edge%d.jpg"%(filename,length), canvas)

cv2.waitKey(0)
cv2.destroyAllWindows()
