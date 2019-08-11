import numpy as np
import enum

class Dimension(enum.IntEnum):
    X = x = 0
    Y = y = 1
    Z = z = 2

## class Facet ##
def __init__(self,points):
    self.points = points if (points.shape == (3,3)) else self.parse_points(points)
    self.direction = self.__direction__()
    self.boundingBox = self.__boundingBox__()
    self.sort()

def parse_points(self,points):
    return points.reshape(3,3)

def sort(self, axis=Dimension.Z):
    # Minimalized Bubble sort for 3 items
    for i in [0,1,0]:
        if self.points[i][axis] > self.points[i+1][axis]:
            temp = self.points[i].copy()
            self.points[i] = self.points[i+1]
            self.points[i+1] = temp

def __direction__(self):
    return np.cross(np.subtract(self.points[0],self.points[1]), np.subtract(self.points[0],self.points[2]))

def __boundingBox__(self):
    minx = maxx = self.points[0,0]
    miny = maxy = self.points[0,1]
    minz = maxz = self.points[0,2]
    for p in self.points[1:]:
        maxx = max(p[0], maxx)
        minx = min(p[0], minx)
        maxy = max(p[1], maxy)
        miny = min(p[1], miny)
        maxz = max(p[2], maxz)
        minz = min(p[2], minz)
    return {'minx':minx, 'maxx':maxx,
            'miny':miny, 'maxy':maxy,
            'minz':minz, 'maxz':maxz}

Facet = type("Facet", (object,), {
        "__init__" : __init__,
        "parse_points" : parse_points,
        "sort" : sort,
        "__direction__" : __direction__,
        "__boundingBox__" : __boundingBox__
    })