import numpy as np
from stl import mesh

from src import DepthSegment as ds

testmodel_1 = '../test_model/토기 예시 데이터/3D 스캔 파일/토기1.stl'
testmodel_5 = '../test_model/토기 예시 데이터/3D 스캔 파일/토기5.stl'
testmodel_t  = '../test_model/Torus.stl'
testmodel_tu = '../test_model/Torus Upward.stl'

def main():
    m = mesh.Mesh.from_file(testmodel_1)
    d = ds.DepthSegmentation(m)

    o = len(d[0])
    s = len(d[1])
    i = len(d[2])
    print(o, s, i, o+i+s)

print('Start.')
main()
print('Done.')
exit()