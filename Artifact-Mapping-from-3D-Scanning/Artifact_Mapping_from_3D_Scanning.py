import cv2
import numpy as np
from stl import mesh

from __3D__ import *

directory = '../토기 예시 데이터/3D 스캔 파일/'
m = mesh.Mesh.from_file(directory+'토기1.stl')
m.normals
def __main__():
    nm = ROTATE(m)
    nm.save('./output.stl')
        
__main__()
input()
exit()