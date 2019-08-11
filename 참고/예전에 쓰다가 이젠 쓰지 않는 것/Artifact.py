import cv2
import numpy as np
from Artifact_Face import *

class Abstract_Artifact():
    def __init__(self, path):
        # Original source file
        self.raw = None

        # Resolution of the output image
        self.shape = tuple(0,0)
        
        self.name = ""

        self.front = Artifacts_Face()
        self.slice = Artifacts_Face()
        self.back  = Artifacts_Face()

    def depth(self):
        raise NotImplementedError()

    def preproc(self):
        raise NotImplementedError()


class Artifact():
    def __init__(self):
        self.raw = None
        self.shape = None
        self.name = ""
        
        self.faces = {
            'front' : Artifacts_Face(),
            'slice' : Artifacts_Face(),
            'back'  : Artifacts_Face(),
        }

    def load(self, path):
        self.raw = readUnicodePath(path)
        self.shape = self.raw.shape

        # TODO - Add "Auto Depth-Based-Segmentation" feature
        path = path[:-4]
        pack = [readUnicodePath(path+t) for t in ["-외.png","-단.png","-내.png"]]
        pack = [self.preproc(im) for im in pack]

        front, slice, back = pack
        self.shape = front.shape #REMOVE
        self.faces['front'].build_from(front)
        self.faces['slice'].build_from(slice)
        self.faces['back'].build_from(back)

    def preproc(self, src):
        src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        src = cv2.GaussianBlur(src, (5,5), 25)
        return src

def readUnicodePath(path):
    stream = open(path,"rb")
    bytes = bytearray(stream.read())
    numpyArray = np.asarray(bytes,dtype=np.uint8)
    img_bgr = cv2.imdecode(numpyArray, cv2.IMREAD_UNCHANGED)
    return img_bgr

class Artifacts_Face():
    def __init__(self):
        self.gray_image = None
        self.bin_image = {
            'default' : None,
            'body'   : [], # Multi Layer Bin images
            'window' : []
        }
        self.contours = None

    def build_from(self, gray):
        self.gray_image = gray
        self.binarize()
        self.findContour()

    def binarize(self):
        src = self.gray_image
        r, src = cv2.threshold(src, 250, 255, cv2.THRESH_BINARY_INV)
        src = cv2.morphologyEx(src, cv2.MORPH_CLOSE,(5,5), iterations=3)
        self.bin_image['default'] = src

    def findContour(self):
        contours, hierarchy = cv2.findContours(self.bin_image['default'], cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        self.contours = contours

        for i in range(len(contours)):
            cont = contours[i]
            hier = hierarchy[0,i]
            canvas = np.zeros(self.gray_image.shape, np.uint8)
            cv2.drawContours(canvas, [cont], 0, 255, -1) # Fill

            isBody = hier[3] < 0
            if isBody:
                self.bin_image['body'].append(canvas)
            else:
                self.bin_image['window'].append(canvas)