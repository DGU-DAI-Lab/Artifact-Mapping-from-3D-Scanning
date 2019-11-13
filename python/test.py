import numpy as np
import cv2
from matplotlib import pyplot as plt

import module.windowDetection as wd

# ====================================================

TEST_IMAGE_PATH = 'test_model/2ds-preproc/토기2/all.png'

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

im = readUnicodePath(TEST_IMAGE_PATH)

ims = wd.macro(im)
ims = [cv2.cvtColor(i, cv2.COLOR_BGR2GRAY) for i in ims]

target = ims[0]
target = cv2.Canny(target, 78,188,apertureSize=3)
target = cv2.morphologyEx(target, cv2.MORPH_CLOSE, (5,5))
conts,_ = cv2.findContours(target,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

areas = [[cv2.contourArea(c)] for c in conts]

hist = cv2.calcHist([ims[0]], [0], None, [256], [1,256],accumulate=1)
print(hist)

plt.subplot(211)
plt.imshow(target, 'gray')
plt.title('Detected Window')

plt.subplot(212)
plt.plot(areas, color='r')
plt.title('histogram')
plt.xlim([0,100])
plt.show()

cv2.waitKey(0)