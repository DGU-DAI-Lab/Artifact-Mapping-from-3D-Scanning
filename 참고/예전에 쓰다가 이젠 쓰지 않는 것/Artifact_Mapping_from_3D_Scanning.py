import cv2
import numpy as np
from stl import mesh

from Rotate3D import *
from DepthSegment import *

testmodel_1 = '../토기 예시 데이터/3D 스캔 파일/토기1.stl'
testmodel_5 = '../토기 예시 데이터/3D 스캔 파일/토기5.stl'
testmodel_t = '../Torus.stl'
testmodel_u = '../Torus Upward.stl'

def __main__():
    m = mesh.Mesh.from_file(testmodel_t)
    m.normals
    
    front,slice,behind = DepthSegmentation(m)
    f = open('../output.svg','w')
    f.write(behind.to_svg())
    f.close()

print('Start.')
__main__()
input('\n'+'Done.')
exit()