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
        self.boundingBox = [[minx, miny, minz], [maxx, maxy, maxz]]

    def translate(self, vector):
        self.mesh.x -= vector[0]
        self.mesh.y -= vector[1]
        self.mesh.z -= vector[2]

    def align(self):
        self.translate(self.center)
        # Rotation

class DepthSegmentation:
    """description of class"""
    def __init__(self, my_mesh):
        self.mesh = my_mesh

        o, i, s = self.segmentation()
        self.i = i


    def segmentation(self):
        outerPolygons = []
        innerPolygons = []
        slicePolygons = []
        isOuter = isSlice = isInner = None

        for poly in self.mesh.vector:
            isOuter = isSlice = isInner = False
            for vector in poly:
                depth = vector[1] # depth == y
                if depth >= 0:
                    isOuter = True
                if depth <= 0:
                    isInner = True
            isSlice = isOuter and isInner

            if isOuter:
                outerPolygons.append(poly)
            if isInner:
                innerPolygons.append(poly)
            if isSlice:
                slicePolygons.append(poly)
        # Convert polygons to mesh
        return [mesh.Mesh(self._polygons2mesh(poly)) for poly in [outerPolygons, slicePolygons, innerPolygons]]

    def _polygons2mesh(self, polygons):
        ret_mesh = np.array(len(polygons), dtype=mesh.Mesh.dtype)
        for i in range(len(polygons)):
            ret_mesh['vectors'][i] = np.array(polygons[i])
        return ret_mesh

    def openize(self, polygons):
        return polygons



