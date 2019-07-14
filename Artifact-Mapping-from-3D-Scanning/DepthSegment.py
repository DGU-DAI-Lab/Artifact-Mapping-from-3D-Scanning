from stl import mesh
import stl
import numpy as np

from numba import jit
import numba

import math
import enum

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

class Dimension(enum.Enum):
    X = x = 0
    Y = y = 1
    Z = z = 2

def DepthSegmentation(obj):
    assert type(obj) is 'mesh.Mesh'
    for f in obj.points:
        facet = Facet(f)
        pass
    return Surface

class Surface:
    def cut_mesh_into_surfaces(self):
        pass

class Facet:
    def __init__(self,facet):

        pass

    def a:
        pass

    def sort_in_order(self,axis=Dimension.Z):
        """"""
        A = B = C = 0 # A < B < C
        for i in [0,1,2]:
            A = i if point.item(3*i+2) < point.item(3*A+2) else A # min
            C = i if point.item(3*i+2) > point.item(3*C+2) else C # max
        B = (3-A-C) if A != C else B
        return np.array([[point.item(3*A+i) for i in [0,1,2]],
                         [point.item(3*B+i) for i in [0,1,2]],
                         [point.item(3*C+i) for i in [0,1,2]]])

    def decide_gradient(self):
        pass

def rotate_angle(vector_from, vector_to):
    """두 벡터의 회전각을 구한다"""
    norm = np.linalg.norm(vector_from) * np.linalg.norm(vector_to)
    if norm == 0:
        print('\nWarning: Norm is zero. Cannot calculate contained angle of the vector with norm zero.')
        return 0
    sin = np.linalg.det([vector_from, vector_to]) / norm
    cos = np.dot(vector_from,vector_to) / norm
    rad = np.arccos(cos) # 두 벡터의 사잇각
    # 사잇각의 부호를 올바르게 정정하여 회전각을 구함.
    return rad if (np.arcsin(sin) > 0) else -rad


def create_svg(obj):
    version = 'xmlns="http://www.w3.org/2000/svg" xmlns:xlink= "http://www.w3.org/1999/xlink"'
    gradients = polygons = ''
    # Get propertises of this model
    points = len(obj.points)
    minx,maxx,miny,maxy,minz,maxz = boundingBox(obj)
    bandwidth = maxz-minz
    # Chk Err
    if bandwidth == 0:
        raise BaseException('No depth differs. WHY!')
    progress = 0
    print('Building svg...')
    for p in range(len(obj.points)):
        tri = align(obj.points[p])
        # Get propertises of this triangle
        startX,endX,startY,endY,startZ,endZ = triangle_start_end(tri)
        vx,vy = decide_gradient_vector(tri)
        # Use relative values
        xA,yA,zA = np.subtract(tri[0],[minx,miny,minz])
        xB,yB,zB = np.subtract(tri[1],[minx,miny,minz])
        xC,yC,zC = np.subtract(tri[2],[minx,miny,minz])
        width  = endX-startX
        height = endY-startY
        # SVG Attributes
        if width*height == 0:
            print('\nThis is a line... :(')
            continue
        else:
            x1 = (xA)/width*100     # Relative X start
            x2 = (xA+vx)/width*100  # Relative X end
            y1 = (yA)/height*100    # Relative Y start
            y2 = (yA+vy)/height*100 # Relative Y end
        colorStart = hex(round((zA/bandwidth)*0xFFFFFF).astype(np.uint32)).replace('0x','')
        colorEnd   = hex(round((zC/bandwidth)*0xFFFFFF).astype(np.uint32)).replace('0x','')
        # TEST
        xA,yA,zA,xB,yB,zB,xC,yC,zC = np.multiply([xA,yA,zA,xB,yB,zB,xC,yC,zC],10)

        # Write SVG Triangle
        polygons  += '<polygon fill="url(#g%d)" points="%lf %lf %lf %lf %lf %lf"/>'%(p,xA,yA,xB,yB,xC,yC)
        gradients += '<linearGradient id="g%d" x1="%f%%" y1="%f%%" x2="%f%%" y2="%f%%">'%(p,x1,y1,x2,y2)
        gradients +=    '<stop offset="0" stop-color="#%s"/>'%('0'*(6-len(colorStart))+colorStart)
        gradients +=    '<stop offset="1" stop-color="#%s"/>'%('0'*(6-len(colorEnd))+colorEnd)
        gradients += '</linearGradient>'
        # DEBUG
        progress += 1
        print('\r>>> Work in progress %d/%d'%(progress,points), end='')
    return '<svg '+version+' style="margin:1000px"><defs>'+gradients+'</defs>'+polygons+'</svg>'

def contained_angle(vect1, vect2):
    norm = np.linalg.norm(vect1) * np.linalg.norm(vect2)
    if (norm == 0):
        print('\nWarning: Norm is zero. Cannot calculate contained angle of the vector with norm zero.')
        return 0
    return np.arccos(np.dot(vect1,vect2) / norm)

def decide_gradient_vector(tri):
    A = tri[0]
    B = tri[1]
    C = tri[2]
    # Calc Euclid distance of AB, AC
    d1 = math.sqrt((A[0]-B[0])**2+(A[1]-B[1])**2) # AB
    d2 = math.sqrt((A[0]-C[0])**2+(A[1]-C[1])**2) # AC
    # Calc the size of contained angles A, C
    a = contained_angle(np.subtract(A,B),np.subtract(A,C)) # A
    r = contained_angle(np.subtract(C,A),np.subtract(C,B)) # C
    # Substitution for some values which are expensive to calc.
    x = d1*(C[2]-A[2]) * math.cos(a)*(-1)
    c = d1*(C[2]-A[2]) * math.sin(a) + d2*(B[2]-A[2])
    # Calc theta and the length of AC'
    theta = np.arctan((x*np.tan(r)+c)/(x/np.tan(r)+c))
    ACp = d2*math.sin(theta+r) # AC'
    # Y-axis
    # Return AC' as a 2D vector
    return np.array([math.sin(theta)*ACp, math.cos(theta)*(-ACp)])


def triangle_start_end(tri):
    startX = endX = tri[0][0]
    startY = endY = tri[0][1]
    startZ = endZ = tri[0][2]
    for p in tri[1:]:
        startX = min(p[0],startX)
        startY = min(p[1],startY)
        startZ = min(p[1],startZ)
        endX = max(p[0],endX)
        endY = max(p[1],endY)
        endZ = max(p[1],endZ)
    return startX,endX,startY,endY,startZ,endZ

def boundingBox(obj):
    minx = maxx = obj.points[0,0]
    miny = maxy = obj.points[0,1]
    minz = maxz = obj.points[0,2]
    for p in obj.points[1:]:
        maxx = max(p[0], maxx)
        minx = min(p[0], minx)
        maxy = max(p[1], maxy)
        miny = min(p[1], miny)
        maxz = max(p[2], maxz)
        minz = min(p[2], minz)
    return minx, maxx, miny, maxy, minz, maxz



# what is considers()
