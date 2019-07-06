"""3D 데이터를 다루는 처리 (mesh)"""
import math
import stl
from stl import mesh
import numpy as np

from mpl_toolkits import mplot3d
from matplotlib import pyplot

def ROTATE(obj):
    """물체의 부피중심으로 부터 무게중심으로 향하는 벡터 f를 구하고,
    f를 z축 음의 방향(0,0,-k)으로 회전시키기 위한 변환행렬 R을 구한다."""
    if not isinstance(obj, mesh.Mesh):
        raise BaseException('NOOooOoOo')

    _, cog, _ = obj.get_mass_properties() # Center of Gravity
    cob = BOUDING_BOX_CENTER(obj)

    f = np.subtract(cog, cob)
    # TEST DATA
    #f = np.array([2.8422805, -5.07449328, -3.66630284])
    #f = np.array([1.57, -3.57, -5.95])
    #f = np.array([1, 1, 0])
    
    # 1
    f_orth = f[:2]
    a = V_ORTHOGONAL(f_orth, [1,0])
    R1 = M_ROTATE_YAW(-a)
    # 2
    f1 = np.matmul(R1, f)
    b = V_ORTHOGONAL([f1[0],f1[2]], [0,1])
    R2 = M_ROTATE_PITCH(np.pi - b)
    
    # 3
    R = np.matmul(R2, R1)
    
    def __chk__():
        print('f : ', f)
        print('a, b : ', a/np.pi, b/np.pi)
        print('f_orth : ', f_orth)
        print('f1 : ', f1)
        print('f2 : ', np.matmul(R2,f1))
        print('\nR1 :\n', R1)
        print('\nR2 :\n', R2)
        print('\nR :\n', R)

        print('applied : ', __apply_epsilon__(np.matmul(R,f)))
    __chk__()
    return obj

def __apply_epsilon__(err_vect):
    """지정한 만큼의 오차는 무시.."""
    eps = 0.0000000001
    for i in range(err_vect.size):
        if eps > np.abs(err_vect.item(i)):
            err_vect.itemset(i, 0)
    return err_vect

def V_DUM_ADD(matrix):
    """행렬에 더미 데이터를 추가"""
    if (matrix.ndim == 1):
        return np.append(matrix, 1)
    w,h = matrix.shape
    new_mat = np.identity(w+1)
    for x in range(w):
        for y in range(h):
            new_mat.itemset((x,y), matrix.item(x,y))
    print(matrix)
    print(new_mat)
    return new_mat

def V_DUM_DEL(matrix):
    """행렬에 존재하는 더미 데이터를 삭제"""
    if (matrix.ndim == 1):
        return matrix[:-1]
    new_shape = np.subtract(matrix.shape, 1)
    new_mat = np.zeros(new_shape)
    w,h = new_shape
    for x in range(w):
        for y in range(h):
            new_mat.itemset((x,y), matrix.item(x,y))
    return new_mat

def V_ORTHOGONAL(vect2D, unit):
    """두 벡터의 회전각을 구한다"""
    norm = np.linalg.norm(vect2D)
    if norm == 0:
        return 0

    theta = np.arccos(np.dot(vect2D,unit) / norm) #벡터 unit의 norm은 1일 것이므로 생략한다
    if (unit[0] == 1 and vect2D[1] < 0) or (unit[1] == 1 and vect2D[0] < 0):
        theta = theta * -1
    return theta

def M_TRANSLATE(matrix, vector):
    x, y, z = vector
    return np.array([
        [   1,  0,  0,  x],
        [   0,  1,  0,  y],
        [   0,  0,  1,  z],
        [   0,  0,  0,  1]])

def __theta_to_sin_cos__(theta):
    s = np.sin(theta)
    c = np.cos(theta)

    rem = theta/np.pi % 1
    if rem == 0:
        s = 0
    elif rem == .5:
        c = 0
    return s, c

def M_ROTATE_PITCH(theta):
    s, c = __theta_to_sin_cos__(theta)
    return np.array([
        [ c,  0,  s],
        [ 0,  1,  0],
        [-s,  0,  c]])

def M_ROTATE_YAW(theta):
    s, c = __theta_to_sin_cos__(theta)
    return np.array([
        [ c, -s,  0],
        [ s,  c,  0],
        [ 0,  0,  1]])

def M_ROTATE_ROLL(theta):
    s, c = __theta_to_sin_cos__(theta)
    return np.array([
        [ 1,  0,  0],
        [ 0,  c, -s],
        [ 0,  s,  c]])

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
