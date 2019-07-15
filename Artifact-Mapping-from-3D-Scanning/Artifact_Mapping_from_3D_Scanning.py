import cv2
import numpy as np
from stl import mesh

from __3D__ import *
from DepthSegment import *

testmodel1 = '../Torus.stl'
testmodel2 = '../토기 예시 데이터/3D 스캔 파일/토기1.stl'

def __main__():
    m = mesh.Mesh.from_file(testmodel1)
    m.normals
    
    svg = create_svg(m)
    f = open('../output.svg','w')
    f.write(svg)
    f.close()

print('Start.')
__main__()
input('Done.')
exit()