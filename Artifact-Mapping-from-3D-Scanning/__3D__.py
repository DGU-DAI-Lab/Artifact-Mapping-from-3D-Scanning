"""3D 데이터를 다루는 처리 (mesh)"""
import math
import stl
from stl import mesh
import numpy as np

def D_SEGMENT(obj):
    obj = ROTATE.AUTO_ALIGN(obj)

    face = cut = back = None
    return face, cut, back

def BOUDING_BOX_CENTER(obj):
    minx, maxx, miny, maxy, minz, maxz = BOUNDING_BOX(obj)
    x = (minx + maxx)/2
    y = (miny + maxy)/2
    z = (minz + maxz)/2
    return x, y, z

def BOUNDING_BOX(obj):
    minx = maxx = miny = maxy = minz = maxz = None
    for p in obj.points:
        # p contains (x, y, z)
        if minx is None:
            minx = p[stl.Dimension.X]
            maxx = p[stl.Dimension.X]
            miny = p[stl.Dimension.Y]
            maxy = p[stl.Dimension.Y]
            minz = p[stl.Dimension.Z]
            maxz = p[stl.Dimension.Z]
        else:
            maxx = max(p[stl.Dimension.X], maxx)
            minx = min(p[stl.Dimension.X], minx)
            maxy = max(p[stl.Dimension.Y], maxy)
            miny = min(p[stl.Dimension.Y], miny)
            maxz = max(p[stl.Dimension.Z], maxz)
            minz = min(p[stl.Dimension.Z], minz)
    return minx, maxx, miny, maxy, minz, maxz




#from numba import jit
#import numba

#obj = mesh.Mesh.from_file('../토기 예시 데이터/3D 스캔 파일/토기1.stl')


#considers = []

#@jit
#def a():
#    i = 0
#    l = len(obj.vectors)
#    for vect in obj.vectors:
#        behind = front = False
#        direction = np.cross(np.subtract(vect[0],vect[1]), np.subtract(vect[0],vect[2]))
#        for x,y,z in vect:
#            front  |= (x >= 0)
#            behind |= (x <= 0)
#        if front and behind:
#            considers.append(vect)
#        i += 1
#        print("\r%d/%d"%(i,l), end="")