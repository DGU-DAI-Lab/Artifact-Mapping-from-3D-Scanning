import cv2
import numpy as np
from stl import mesh

from __3D__ import *
from DepthSegment import *

testmodel0 = '../토기 예시 데이터/3D 스캔 파일/토기1.stl'
testmodel1 = '../Torus.stl'
testmodel2 = '../Torus Upward.stl'

def __main__():
    m = mesh.Mesh.from_file(testmodel2)
    m.normals
    
    front,slice,behind = DepthSegmentation(m)
    f = open('../output.svg','w')
    f.write(front.to_svg())
    f.close()

print('Start.')
__main__()
input('\n'+'Done.')
exit()