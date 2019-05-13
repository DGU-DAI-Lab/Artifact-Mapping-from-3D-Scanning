from tkinter import filedialog as fd


import cv2
import numpy as np
from stl import mesh

class A:
    def __init__(self):
        pass

    def open(self, path=""):
        #path = fd.askopenfilename()
        self.mesh = mesh.Mesh.from_file(path)

    def rotate(self, rMat=[.0, .5, .0], rRad=90):
        self.mesh.rotate(rMat, math.radians(rRad))

    def moveto(self, x, y, z):
        self.mesh.x += x
        self.mesh.y += y
        self.mesh.z += z


from mpl_toolkits import mplot3d
from matplotlib import pyplot

figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)

m = A()
m.open("E:/Git/clone repository/Artifact-Mapping-from-3D-Scanning/토기 예시 데이터/3D 스캔 파일/토기1.stl")
print("Mesh 개수: % 8d개" % (len(m.mesh)))

from DepthSegmentation import *
obj = Obj3D(m.mesh)
obj.align()

m = obj.mesh

axes.add_collection3d(mplot3d.art3d.Poly3DCollection(m.vectors[:6000]))
pyplot.show()