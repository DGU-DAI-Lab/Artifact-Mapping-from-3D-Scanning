"""3D 데이터를 다루는 처리 (mesh)"""
import math
import stl
from stl import mesh
import numpy as np

from mpl_toolkits import mplot3d
from matplotlib import pyplot

def ROTATE(obj):
    #_, cog, _ = obj.get_mass_properties() # Center of Gravity
    #g = [1.57, -3.57, -5.95]
    g = [0, 1, 0]
    I = [[1,0,0],
         [0,1,0],
         [0,0,1]]

    roll = V_ORTHOGONAL(g[:2],[1,0])
    g2 = M_ROTATE_ROLL(g, -roll) # XZ평면위
    yaw = V_ORTHOGONAL([g2[0], g2[2]],[0,1])
    yaw += np.pi
    
    res = M_ROTATE_ROLL(g2, -yaw) # XZ평면위
    
    print('roll :', roll/np.pi)
    print(' yaw :', yaw/np.pi)
    print('trans. :', res)
   
    return obj

def V_ORTHOGONAL(vect, unit):
    theta = np.arccos(np.dot(vect,unit) / np.linalg.norm(vect)) #벡터 unit의 norm은 1일 것이므로 생략한다
    if vect[1] < 0:
        theta = 2*np.pi - theta
    return theta

def M_TRANSLATE(matrix, vector):
    x, y, z = vector
    transform = [
        [   1,  0,  0,  x],
        [   0,  1,  0,  y],
        [   0,  0,  1,  z],
        [   0,  0,  0,  1]]
    return np.matmul(matrix, transform)

def M_ROTATE_PITCH(matrix, theta):
    c = np.cos(theta)
    s = np.sin(theta)
    return np.matmul([
        [ 1,  0,  0],
        [ 0,  c, -s],
        [ 0,  s,  c]], matrix)

def M_ROTATE_YAW(matrix, theta):
    c = np.cos(theta)
    s = np.sin(theta)
    return np.matmul([
        [ c,  0,  s],
        [ 0,  1,  0],
        [-s,  0,  c]], matrix)

def M_ROTATE_ROLL(matrix, theta):
    c = np.cos(theta)
    s = np.sin(theta)
    return np.matmul([
        [ c, -s,  0],
        [ s,  c,  0],
        [ 0,  0,  1]], matrix)

def BOUDING_BOX_CENTER(obj):
    minx, maxx, miny, maxy, minz, maxz = BOUNDING_BOX(obj)
    x = (minx + maxx)/2
    y = (miny + maxy)/2
    z = (minz + maxz)/2
    return x, y, z

def D_SEGMENT(mesh_data):
    face = cut = back = None
    return face, cut, back

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

def __chk_dtype__(source, type):
    pass
