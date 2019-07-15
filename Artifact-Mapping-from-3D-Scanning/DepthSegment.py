from stl import mesh
import stl
import numpy as np
import math

#from numba import jit
#import numba

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

from Facet import Facet, Dimension

def DepthSegmentation(obj,axis=Dimension.Z):
    assert type(obj) is 'mesh.Mesh'
    front  = Surface()
    behind = Surface()
    slice  = Surface()
    for facet in [Facet(f) for f in obj.points]:
        # Front or behind the xy-surface
        isFront = isBehind = False
        for ax in facet.points[:,axis]:
            isFront  |= (ax >= 0)
            isBehind |= (ax <= 0)
        #  - Find slices
        if isFront and isBehind:
            slice.append(facet)
        # Viewable and non-viewables
        isViewable = (facet.direction[axis] > 0)
        if not isViewable:
            continue
        #  - Find fronts and behinds
        if isFront:
            front.append(facet)
        if isBehind:
            behind.append(facet)
    return front,slice,behind

class Surface:
    def __init__(self):
        self.facets = []

    def append(self,facet):
        assert type(facet) is 'Facet'
        self.facets.append(facet)

    def boundingBox(self):
        facet = self.facets[0]
        minx = maxx = facet.points[0,0]
        miny = maxy = facet.points[0,1]
        minz = maxz = facet.points[0,2]
        for facet in self.facets[:]:
            maxx = max(facet.points[:,0], maxx)
            minx = min(facet.points[:,0], minx)
            maxy = max(facet.points[:,1], maxy)
            miny = min(facet.points[:,1], miny)
            maxz = max(facet.points[:,2], maxz)
            minz = min(facet.points[:,2], minz)
        return {'minx':minx, 'maxx':maxx,
                'miny':miny, 'maxy':maxy,
                'minz':minz, 'maxz':maxz}

    #### FOR SVG CONVERT ###
    def decide_gradient_vector(self,facet): # Dimension.Z
        A,B,C = facet.points
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
    
    def to_svg(self):
        VERSION = 'xmlns="http://www.w3.org/2000/svg" xmlns:xlink= "http://www.w3.org/1999/xlink"'
        gradients = polygons = ''

        surface_bounds = self.boundingBox()
        color_range = surface_bounds.maxz - surface_bounds.minz
        
        n_facets = len(self.facets)
        progress = 0
        for facet in self.facets:
            # Get propertises of this triangle
            facet_bounds = facet.boundingBox
            gx,gy = self.decide_gradient_vector(facet)
            #
            width  = facet_bounds.maxx - facet_bounds.minx
            height = facet_bounds.maxy - facet_bounds.miny
            #
            if width*height == 0:
                print('\nThis is a line... :(')
                continue
            # Use relative values
            A = np.subtract(facet[0],[minx,miny,minz])
            B = np.subtract(facet[1],[minx,miny,minz])
            C = np.subtract(facet[2],[minx,miny,minz])
            # SVG Attributes
            x1 = (A[Dimension.X])   /width *100 # Relative X start
            x2 = (A[Dimension.X]+gx)/width *100 # Relative X end
            y1 = (A[Dimension.Y])   /height*100 # Relative Y start
            y2 = (A[Dimension.Y]+vy)/height*100 # Relative Y end
            colorStart = hex(round((A[Dimension.Z]/color_range)*0xFFFFFF).astype(np.uint32)).replace('0x','')
            colorEnd   = hex(round((C[Dimension.Z]/color_range)*0xFFFFFF).astype(np.uint32)).replace('0x','')
            stopColor1 = '0'*(6-len(colorStart)) + colorStart
            stopColor2 = '0'*(6-len(colorEnd))   + colorEnd
            
            # TEST
            A,B,C = np.multiply([A,B,C],10)

            # Write SVG Triangle
            polygons  += '<polygon fill="url(#g%d)" points="%lf %lf %lf %lf %lf %lf"/>'%(p,xA,yA,xB,yB,xC,yC)
            gradients += '<linearGradient id="g%d" x1="%lf%%" y1="%lf%%" x2="%lf%%" y2="%lf%%">'%(p,x1,y1,x2,y2)
            gradients +=    '<stop offset="0" stop-color="#%s"/>'%(stopColor1)
            gradients +=    '<stop offset="1" stop-color="#%s"/>'%(stopColor2)
            gradients += '</linearGradient>'
            # DEBUG
            progress += 1
            print('\r>>> Work in progress %d/%d'%(progress,points), end='')
        return '<svg '+VERSION+' style="margin:1000px"><defs>'+gradients+'</defs>'+polygons+'</svg>'

def contained_angle(vect1, vect2):
    """두 벡터의 사잇각을 구한다"""
    norm = np.linalg.norm(vect1) * np.linalg.norm(vect2)
    if (norm == 0):
        print('\nWarning: Norm is zero. Cannot calculate contained angle of the vector with norm zero.')
        return 0
    return np.arccos(np.dot(vect1,vect2) / norm)

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

def mesh_boundingBox(obj):
    p = obj.points[0] # p is a 1x9 matrix : (x1,y1,z1,x2,y2,z2,x3,...)
    maxx = max(p[0],p[3],p[6])
    minx = min(p[0],p[3],p[6])
    maxy = max(p[1],p[4],p[7])
    miny = min(p[1],p[4],p[7])
    maxz = max(p[2],p[5],p[8])
    minz = min(p[2],p[5],p[8])
    for p in obj.points[1:]:
        maxx = max(p[0],p[3],p[6], maxx)
        minx = min(p[0],p[3],p[6], minx)
        maxy = max(p[1],p[4],p[7], maxy)
        miny = min(p[1],p[4],p[7], miny)
        maxz = max(p[2],p[5],p[8], maxz)
        minz = min(p[2],p[5],p[8], minz)
    return minx,maxx,miny,maxy,minz,maxz

def create_svg(surface):
    assert type(surface) is 'Surface'
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
        stopColor1 = '0'*(6-len(colorStart)) + colorStart
        stopColor2 = '0'*(6-len(colorEnd))   + colorEnd
        # TEST
        xA,yA,zA,xB,yB,zB,xC,yC,zC = np.multiply([xA,yA,zA,xB,yB,zB,xC,yC,zC],10)

        # Write SVG Triangle
        polygons  += '<polygon fill="url(#g%d)" points="%lf %lf %lf %lf %lf %lf"/>'%(p,xA,yA,xB,yB,xC,yC)
        gradients += '<linearGradient id="g%d" x1="%lf%%" y1="%lf%%" x2="%lf%%" y2="%lf%%">'%(p,x1,y1,x2,y2)
        gradients +=    '<stop offset="0" stop-color="#%s"/>'%(stopColor1)
        gradients +=    '<stop offset="1" stop-color="#%s"/>'%(stopColor2)
        gradients += '</linearGradient>'
        # DEBUG
        progress += 1
        print('\r>>> Work in progress %d/%d'%(progress,points), end='')
    return '<svg '+version+' style="margin:1000px"><defs>'+gradients+'</defs>'+polygons+'</svg>'

# what is considers()
