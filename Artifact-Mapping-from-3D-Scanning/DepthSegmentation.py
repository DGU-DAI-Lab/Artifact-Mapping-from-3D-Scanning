import math
import stl
from stl import mesh
import numpy as np

class Obj2D:
    pass

class Obj3D:
    def __init__(self, my_mesh):
        self.mesh = my_mesh

        self.volume, self.cog, self.inertia = self.mesh.get_mass_properties()
        
        self.computeBoundingBox()
        self.center = [(self.boundingBox[0][i]+self.boundingBox[1][i])/2 for i in [0,1,2]]

    def computeBoundingBox(self):
        minx = maxx = None
        miny = maxy = None
        minz = maxz = None
        for p in self.mesh.points:
            if minx is None:
                minx = maxx = p[stl.Dimension.X]
                miny = maxy = p[stl.Dimension.Y]
                minz = maxz = p[stl.Dimension.Z]
            maxx = max(p[stl.Dimension.X], maxx)
            maxy = max(p[stl.Dimension.Y], maxy)
            maxz = max(p[stl.Dimension.Z], maxz)
            minx = min(p[stl.Dimension.X], minx)
            miny = min(p[stl.Dimension.Y], miny)
            minz = min(p[stl.Dimension.Z], minz)
        self.boundingBox = ((minx, miny, minz), (maxx, maxy, maxz))

    def align(self):
        pass

class DepthSegmentation(object):
    """description of class"""
    def __init__(self, object3D):
        self.pivot = [0, 0, 0] # 원점 좌표
        self.crossSectionVect = [0, 0, 0] # 절단면의 방향 벡터
        pass

    def setCrossSection(self, crossSectionVect, ): # 절단면의 방향 벡터 위치 설정
        self.crossSectionVect = vector

