import cv2
import numpy as np
from Artifact_Face import *

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
        #src = cv2.GaussianBlur(src, (5,5), 25)
        return src

def readUnicodePath(path):
    stream = open(path,"rb")
    bytes = bytearray(stream.read())
    numpyArray = np.asarray(bytes,dtype=np.uint8)
    img_bgr = cv2.imdecode(numpyArray, cv2.IMREAD_UNCHANGED)
    return img_bgr