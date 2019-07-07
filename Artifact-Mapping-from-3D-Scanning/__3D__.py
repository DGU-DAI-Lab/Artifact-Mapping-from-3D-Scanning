"""3D 데이터를 다루는 처리 (mesh)"""
import math
import stl
from stl import mesh
import numpy as np

from mpl_toolkits import mplot3d
from matplotlib import pyplot

class ROTATE:
    def AUTO_ALIGN(self, obj):
        """물체의 부피중심으로 부터 무게중심으로 향하는 벡터 f를 구하고, f를 z축 음의 방향(0,0,-k)으로 회전시키기 위한 변환행렬 R을 구한다."""
        if not isinstance(obj, mesh.Mesh):
            raise BaseException('NOOooOoOo Wrong file!!!')
        f = self.OBJECT_AXIS(obj)
    
        yaw = self.ANGLE_OF_ROTATION_2D(f[:2],[1,0])
        R1 = self.M_ROTATE_YAW(yaw)
    
        f1 = self.__allow_err__(np.matmul(R1, f))
        if not (f1[1] == 0):
            print('yaw', yaw/np.pi)
            print('f1', f1)
            raise BaseException('Wrong yaw rotation')

        pitch = self.ANGLE_OF_ROTATION_2D([f1[0],f1[2]], [0,1])
        R2 = self.M_ROTATE_PITCH(np.pi - pitch)

        f2 = self.__allow_err__(np.matmul(R2, f1))
        if not (f2[0] == 0 and f2[1] == 0 and f2[2] < 0):
            print('pitch', pitch/np.pi*180)
            print('f1', f1)
            print('f2', f2)
            raise BaseException('Wrong pitch rotation')
    
        R = np.matmul(R2, R1)
        obj.rotate_using_matrix(R)
        return obj

    def OBJECT_AXIS(self, obj):
        """물체의 부피중심으로 부터 무게중심으로 향하는 벡터"""
        _,cog,_ = obj.get_mass_properties() # Center of Gravity
        cob = self.BOUDING_BOX_CENTER(obj)
        return np.subtract(cog, cob) 
    
    def __allow_err__(self, err_vect):
        """지정한 만큼의 오차는 무시.."""
        eps = 0.0000000001
        for i in range(err_vect.size):
            if eps > np.abs(err_vect.item(i)):
                err_vect.itemset(i, 0)
        return err_vect

    def ANGLE_OF_ROTATION_2D(self, vector_from, vector_to):
        """두 벡터의 회전각을 구한다"""
        norm = np.linalg.norm(vector_from) * np.linalg.norm(vector_to)
        if norm == 0: # 두 벡터 중 하나라도 크기가 0일 경우.
            return 0
        sin = np.linalg.det([vector_from, vector_to]) / norm
        cos = np.dot(vector_from,vector_to) / norm
        theta = np.arccos(cos) # 두 벡터의 사잇각
        # 사잇각의 부호를 올바르게 정정하여 회전각을 구함.
        return theta if np.arcsin(sin) > 0 else -theta

    def __theta_to_sin_cos__(self, theta):
        s = np.sin(theta)
        c = np.cos(theta)
        rem = theta/np.pi % 1
        if rem == 0:
            s = 0
        elif rem == .5:
            c = 0
        return s, c

    def M_ROTATE_PITCH(self, theta):
        s, c = self.__theta_to_sin_cos__(theta)
        return np.array([
            [ c,  0,  s],
            [ 0,  1,  0],
            [-s,  0,  c]])

    def M_ROTATE_YAW(self, theta):
        s, c = self.__theta_to_sin_cos__(theta)
        return np.array([
            [ c, -s,  0],
            [ s,  c,  0],
            [ 0,  0,  1]])

    def M_ROTATE_ROLL(self, theta):
        s, c = self.__theta_to_sin_cos__(theta)
        return np.array([
            [ 1,  0,  0],
            [ 0,  c, -s],
            [ 0,  s,  c]])

def D_SEGMENT(mesh_data):
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