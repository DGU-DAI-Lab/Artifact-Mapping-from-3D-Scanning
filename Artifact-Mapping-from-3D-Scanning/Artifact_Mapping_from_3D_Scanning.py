import cv2
import numpy as np
from stl import mesh

from __3D__ import *

def load_obj():
    directory = '../토기 예시 데이터/3D 스캔 파일/'
    m = mesh.Mesh.from_file(directory+'토기1.stl')
    m.normals
    return m

def __main__():
    m = load_obj()
    nm = ROTATE.AUTO_ALIGN(m)
    nm.save('./output.stl')
        
__main__()
input()
exit()