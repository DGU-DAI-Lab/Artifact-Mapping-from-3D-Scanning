import cv2
import numpy as np

from matplotlib import pyplot as plt

def readUnicodePath(path):
    stream = open(path,"rb")
    bytes = bytearray(stream.read())
    numpyArray = np.asarray(bytes,dtype=np.uint8)
    img_bgr = cv2.imdecode(numpyArray, cv2.IMREAD_UNCHANGED)
    return img_bgr

class Container():
    def __init__(self):
        self.front = []
        self.collapse = None
        self.back = []

class Artifact():
    def __init__(self):
        self.raw = None
        self.shape = None

        self.image = Container()
        self.binary = Container()
        self.masks = Container()
        self.contours = Container()

        self.availableParts = ['front', 'back']

    def load(self, path):
        self.image.raw = readUnicodePath(path)
        self.image.front[0] = readUnicodePath(path[:-5]+"-외"+path[-4:])
        self.image.back[0] = readUnicodePath(path[:-5]+"-내"+path[-4:])
        self.shape = self.image.raw.shape

    def _binarize(im):
        im = cv2.cvtColor(im.copy(), cv2.COLOR_BGR2GRAY)
        im = cv2.GaussianBlur(im, (5,5), 25)
        r, im = cv2.threshold(im, 250, 255, cv2.THRESH_BINARY_INV)
        return im

    def binarize(self):
        for part in self.availableParts:
            for im in self.image[part]:
                im = self._binarize(im)
                self.binary[part].append(im)

        self.findContours()
        self.generateMask()

    def findContours(self):
        for part in self.availableParts:
            for bin_im in self.binary[part]:
                conts, hier = cv2.findContours(bin_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
                self.contours[part].append(conts)

    def generate_masks(self):
        for part in self.availableParts:
            for cont in self.contours[part]:
                mask = np.zeros(self.image.shape[:1], np.uint8)
                cv2.drawContours(mask, [cont], 0, 255, -1)
                self.masks.append(mask)

samples = []

def load(): # Depth-Based Segmentation
    global samples
    for name in ["고배", "굽다리접시1", "토기6"]:
        art = Artifact()
        art.load("../캐럿펀트 샘플 데이터/"+name+".png")
        art.binarize()
        samples.append()



def getFrontContour():
    global samples
    for artifact in samples:
        for b in artifact.binary.front:
            _getContours(b)

class M():
    def __init__(self):
        self.mlb = []
        self.center = 0
        self.masks = []

samples = [];

def analyze():
    global samples
    for m in samples:
        for a in m.mlb:
            k = 1
            bin_src = cv2.dilate(a, (5,5), iterations=k)
            contours, hierarchy = cv2.findContours(bin_src, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            print(len(contours))
            for cont in contours:
                canvas = np.zeros(bin_src.shape, np.uint8)
                cv2.drawContours(canvas, [cont], 0, 255, -1)
                m.masks.append(canvas)

def mask_operation(image, mask):
    pass

open_files()
analyze()

for i in range(len(samples)):
    samp = samples[i]
    for j in range(len(samp.masks)):
        mask = samp.masks[j]
        cv2.imwrite("../mask_%d_%d.jpg"%(i,j), mask)
    for k in range(len(samp.mlb)):
        mlb = samp.mlb[k]
        cv2.imwrite("../mlb_%d_%d.jpg"%(i,k),mlb)
cv2.waitKey(0)
exit()



img=cv2.imread('test.jpg', cv2.IMREAD_GRAYSCALE)

cut1=img[0:256, 0:381]
cut2=img[0:256, 381:801]
cut3=img[257:664,0:381]
cut4=img[257:664,381:801]
ret, thr=cv2.threshold(img,255,255,0)
cut_b1=thr[0:256, 0:381]
cut_b2=thr[0:256, 381:801]
cut_b3=thr[257:664,0:380]
cut_b4=thr[257:664,381:801]


cv2.imshow('cut1',cut1)
cv2.imshow('cut2',cut2)
cv2.imshow('cut3',cut3)
cv2.imshow('cut4',cut4)

blur1=cv2.bilateralFilter(cut1,3,50,50)
blur1=cv2.bilateralFilter(blur1,3,60,60)
canny1=cv2.Canny(blur1,100,200)
contours, hierachy=cv2.findContours(canny1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(cut_b1, contours, -1, (255,255,255), 1)
cv2.imshow('rcut1',cut1)

blur2=cv2.medianBlur(cut2,5)
blur2=cv2.medianBlur(blur2,7)
canny2=cv2.Canny(blur2,100,200)
contours2, hierachy=cv2.findContours(canny2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(cut_b2, contours2, -1, (255,255,255), 1)
cv2.imshow('rcut2',cut2)

blur3=cv2.GaussianBlur(cut3,(3,3),0)

blur3=cv2.GaussianBlur(blur3,(7,7),0)
canny3=cv2.Canny(blur3,40,60)
contours3, hierachy=cv2.findContours(canny3, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(cut_b3, contours3, -1, (255,255,255), 1)
cv2.imshow('rcut3',cut3)

blur4=cv2.medianBlur(cut4,3)
blur4=cv2.medianBlur(blur4,5)
canny4=cv2.Canny(blur4,78,188)
contours4, hierachy=cv2.findContours(canny4, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(cut_b4, contours4, -1, (255,255,255), 1)
cv2.imshow('rcut4',cut4)

cv2.imshow('canny1', canny1)
cv2.imshow('canny2',canny2)
cv2.imshow('canny3',canny3)
cv2.imshow('canny4',canny4)
cv2.imshow('contours',img)
cv2.imshow('th',thr)
cv2.waitKey(0)
cv2.destroyAllWindows()