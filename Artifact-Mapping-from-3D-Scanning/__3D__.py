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


