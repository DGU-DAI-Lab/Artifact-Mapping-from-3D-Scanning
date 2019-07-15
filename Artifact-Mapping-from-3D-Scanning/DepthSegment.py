from stl import mesh
import stl
import numpy as np
import math

from Facet import Facet,Dimension

def DepthSegmentation(obj,axis=Dimension.Z):
    assert isinstance(obj,mesh.Mesh)
    front  = Surface()
    behind = Surface()
    slice  = Surface()
    # ProgressBar
    print('D-Segmentation start.')
    n_points = len(obj.points)
    progress = 0
    for f in obj.points:
        # ProgressBar
        progress += 1
        print('\r>>> Work in progress %d/%d\t'%(progress,n_points), end='')

        facet = Facet(f)
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
    print('D-Segmentation done.')
    return front,slice,behind

class Surface:
    def __init__(self):
        self.facets = []

    def append(self,facet):
        assert isinstance(facet,Facet)
        self.facets.append(facet)

    def boundingBox(self):
        p = self.facets[0].points
        minx = maxx = p[0,0]
        miny = maxy = p[0,1]
        minz = maxz = p[0,2]
        for facet in self.facets:
            for p in facet.points:
                maxx = max(p[0], maxx)
                minx = min(p[0], minx)
                maxy = max(p[1], maxy)
                miny = min(p[1], miny)
                maxz = max(p[2], maxz)
                minz = min(p[2], minz)
        return {'minx':minx, 'maxx':maxx,
                'miny':miny, 'maxy':maxy,
                'minz':minz, 'maxz':maxz}

    #### FOR SVG CONVERT ###
    def decide_gradient_vector(self,facet,theta=False): # Dimension.Z
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
        thet = np.arctan((x*np.tan(r)+c)/(x/np.tan(r)+c))
        ACp = d2*math.sin(thet+r) # AC'
        # Y-axis
        # Return AC' as a 2D vector
        if theta:
            return np.array([math.sin(thet)*ACp, math.cos(thet)*(-ACp), thet])
        return np.array([math.sin(thet)*ACp, math.cos(thet)*(-ACp)])
    
    def to_svg(self):
        VERSION = 'xmlns="http://www.w3.org/2000/svg" xmlns:xlink= "http://www.w3.org/1999/xlink"'
        SCALE = 2
        COLOR_SCALE = 0xFF
        gradients = polygons = ''
        # Get propertises of the surface
        surface_bounds = self.boundingBox()
        s_mins = [surface_bounds[a] for a in ['minx','miny','minz']]
        s_maxs = [surface_bounds[a] for a in ['maxx','maxy','maxz']]
        color_range = s_maxs[Dimension.Z] - s_mins[Dimension.Z]
        # ProgressBar
        print('Start converting Surface into SVG...')
        n_facets = len(self.facets)
        progress = 0
        for facet in self.facets:
            # ProgressBar
            progress += 1
            print('\r>>> Work in progress %d/%d\t'%(progress,n_facets), end='')
            # Get propertises of this facet
            A,B,C = facet.points
            facet_bounds = facet.boundingBox
            f_mins = [facet_bounds[a] for a in ['minx','miny','minz']]
            f_maxs = [facet_bounds[a] for a in ['maxx','maxy','maxz']]
            gx,gy,theta = self.decide_gradient_vector(facet,theta=True)
            # Use relative values
            width  = f_maxs[Dimension.X] - f_mins[Dimension.X]
            height = f_maxs[Dimension.Y] - f_mins[Dimension.Y]
            # For Lines ### TODO
            if width*height == 0:
                print('This is a line... :(')
                continue
                #A,B,C = np.multiply([np.subtract(p,s_mins) for p in [A,B,C]],SCALE) # TRANSLATE & SCALE
                #points = '%lf %lf %lf %lf %lf %lf' % (
                #    A[Dimension.X],A[Dimension.Y],
                #    B[Dimension.X],B[Dimension.Y],
                #    C[Dimension.X],C[Dimension.Y])
                #polygons  += '<polyline style="fill:none;stroke:black;stroke-width:1" points="%s"/>'%(points)
            # For Triangles
            else:
                d = A[Dimension.X]-f_mins[Dimension.X]
                colorStart = round(((A[Dimension.Z]-s_mins[Dimension.Z]) / color_range)*COLOR_SCALE).astype(np.uint32)
                colorEnd   = round(((C[Dimension.Z]-s_mins[Dimension.Z]) / color_range)*COLOR_SCALE).astype(np.uint32)
                # SVG Attributes
                x1 = ( d * math.sin(theta)**2) / width  * 100  # Relative X start
                y1 = (-d * math.sin(theta)*math.cos(theta)) / height * 100  # Relative Y start
                x2 = x1 + (gx / width  * 100) # Relative X end
                y2 = y1 + (gy / height * 100) # Relative Y end
                A,B,C = np.multiply([np.subtract(p,s_mins) for p in [A,B,C]],SCALE) # TRANSLATE & SCALE
                points = '%lf %lf %lf %lf %lf %lf' % (
                    A[Dimension.X],A[Dimension.Y],
                    B[Dimension.X],B[Dimension.Y],
                    C[Dimension.X],C[Dimension.Y])
                stopColor1 = 'rgb(%d,%d,%d)'%(colorStart,colorStart,colorStart)
                stopColor2 = 'rgb(%d,%d,%d)'%(colorEnd,  colorEnd,  colorEnd)
                # Write SVG Triangle
                polygons  += '<polygon fill="url(#g%d)" points="%s"/>'%(progress,points)
                gradients += '<linearGradient id="g%d" x1="0%%" y1="0%%" x2="%lf%%" y2="%lf%%">'%(progress,x2,y2)
                gradients +=    '<stop offset="0" stop-color="%s"/>'%(stopColor1)
                gradients +=    '<stop offset="1" stop-color="%s"/>'%(stopColor2)
                gradients += '</linearGradient>'
        print('SVG converting done!')
        return '<svg '+VERSION+' style="margin:32px"><defs>'+gradients+'</defs>'+polygons+'</svg>'

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

# what is considers()