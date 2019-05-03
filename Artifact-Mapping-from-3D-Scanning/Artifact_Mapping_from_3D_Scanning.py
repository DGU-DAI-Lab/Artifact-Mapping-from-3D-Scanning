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

meshes = []

for i in [6]:
    m = A()
    meshes.append(m)

    m.open("E:/Git/clone repository/Artifact-Mapping-from-3D-Scanning/토기 예시 데이터/3D 스캔 파일/토기%d.stl" % i)
    print("%d번 STL파일 Mesh 개수: % 8d개" % (i, len(m.mesh)))

m = meshes[0].mesh

axes.add_collection3d(mplot3d.art3d.Poly3DCollection(m.vectors[:6000]))
pyplot.show()