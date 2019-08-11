import numpy as np

# SVG Config.
WIDTH = HEIGHT = 4096
MULT = 10
TRAN = 800
THIC = 0
COLO = 0xFFFFFF

COLOR_MAX = 0xFF # Gradient method, max color

VERSION = 'xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"'
STYLES   = [
    'polyline { fill:none; stroke:#%06x; stroke-width:%f; }' % (COLO,THIC),
    'polyline["window"] { stroke:red; }', # 아직 사용하지 않음.
    'polygon { stroke:#%06x; stroke-width:%f; }' % (COLO,THIC),
    'circle { stroke:none }',
    'circle[a] { fill:lime; }',
    'circle[b_alt] { fill:blue; }',
    'circle[c_alt] { fill:red; }']

def build_section(section_cutting):
    """Section 영역을 흑백(이진) 2D SVG 이미지로 변환.
    (단면에 접하는 선분들을 polyline으로 표현)"""
    svg = ''
    svg += create_header()
    svg += create_style()
    svg += create_lines(section_cutting)
    svg += create_footer()
    return svg

def build_surface(surface):
    """Front 와 Rear 영역을 색상(깊이)정보가 있는 2D SVG 이미지로 변환.
    (각 facet을 polygon과 linear_gradient로 표현)"""
    svg = ''
    svg += create_header()
    svg += create_style()
    svg += create_polygons(surface)
    svg += create_footer()
    return svg

# Commons

def create_header():
    return '<svg %s width="%d" height="%d">' % (VERSION, WIDTH, HEIGHT)

def create_footer():
    return '</svg>'

def create_style():
    svg = '<style>'
    for s in STYLES: svg += s
    svg += '</style>'
    return svg

def create_line(line):
    A,B = np.add(np.dot(line,MULT),TRAN)
    return '<polyline points="%f,%f %f,%f"/>'%(A[0],A[1],B[0],B[1])

def create_lines(lines):
    svg = ''
    for line in lines: svg += create_line(line)
    return svg

def create_polygon(vectors,fill):
    v = np.add(np.dot(vectors,MULT),TRAN)
    return """<polygon fill="%s" points="%f,%f %f,%f %f,%f"/>
    """ % (fill, v[0,0],v[0,1], v[1,0],v[1,1], v[2,0],v[2,1])

def create_polygon_background(data, color_bandwidth, color_lowest, id='undefined',method='plain'):
    if method == 'gradient':
        return use_gradient(data, id, color_bandwidth, color_lowest)
    else:
        return use_plain(data, id, color_bandwidth, color_lowest)

def create_polygons(surface, method='auto'):
    defs = ''
    polygons = ''

    colors = np.array([data[1][:,2] for data in surface]).flatten()
    c_lowest = min(colors)
    c_bandwidth = max(colors) - c_lowest
    if c_bandwidth == 0: # TODO
        print('no depth diffrences.')
        return ''
    
    amount = len(surface)
    if method == 'auto':
        method = 'gradient' if (amount < 100000) else 'plain'
    for i in range(amount):
        data = surface[i]
        bg,f = create_polygon_background(data,c_bandwidth,c_lowest, id=i,method=method)
        polygons += create_polygon(data[1], f)
        defs += bg
    return '<defs>'+defs+'</defs>' + polygons

def use_gradient(data,id, color_bandwidth, color_lowest):
    def _grad_by_differential(data):
        _,vectors,_ = data
        # A,B,C = [vectors[order] for order in np.argsort(vectors[:,2])]
        A,B,C = _sort(vectors)
        def d(P,axis):
            return P[axis]-A[axis]
        m = (d(B,0)*d(C,2) - d(B,2)*d(C,0)) / (d(B,2)*d(C,1) - d(B,1)*d(C,2))
        m2 = m*m
        def get_alt(P):
            x = (m2*A[0] + P[0] + m*(d(P,1))) / (m2 + 1) # P'x
            y = m*x
            z = P[2]
            return [x,y,z]
        return A,get_alt(B),get_alt(C)
    def _grad_by_normal(data):
        normal,vectors,_ = data
        maxx,minx,maxy,miny,maxz,minz = _bounding_box(vectors)
        m = normal[1] / normal[0]
        m2 = m*m
        A = np.array([minx, miny]) if (m > 0) else np.array([minx, maxy])
        def get_alt(P):
            x = (m2*A[0] + P[0] + m*(P[1]-A[1])) / (m2 + 1) # P'x
            y = m*x
            z = P[2]
            return [x,y,z]
        alts = [get_alt(p) for p in vectors]
        norms = [np.linalg.norm(p[:2]) for p in alts]
        return [alts[order] for order in np.argsort(norms)]

    # create_facet과 decide_Gradient_vector가 공통으로 쓰는 값들
    maxx,minx,maxy,miny,maxz,minz = _bounding_box(data[1])
    width  = maxx - minx
    height = maxy - miny
    if width * height == 0:
        # line = (A[:2], B[:2])
        # return '', create_line(line)
        return '', ''
    # 이하 자세한 건 연구노트 참고.
    A_alt,B_alt,C_alt = _grad_by_normal(data)
    x1 = (A_alt[0] - minx) / width
    y1 = (A_alt[1] - miny) / height
    x2 = (C_alt[0] - minx) / width
    y2 = (C_alt[1] - miny) / height

    s2r = (B_alt[0]-A_alt[0]) / (C_alt[0]-A_alt[0]) # stop-point2 ratio

    sc1 = int( (A_alt[2] - color_lowest) / color_bandwidth * COLOR_MAX )
    sc2 = int( (B_alt[2] - color_lowest) / color_bandwidth * COLOR_MAX )
    sc3 = int( (C_alt[2] - color_lowest) / color_bandwidth * COLOR_MAX )

    fill = 'url(#g%d)' % id
    gradient = """
    <linearGradient id="g%d" x1="%f" y1="%f" x2="%f" y2="%f">
        <stop offset="0"  stop-color="#%06x"/>
        <stop offset="%f" stop-color="#%06x"/>
        <stop offset="1"  stop-color="#%06x"/>
    </linearGradient>
    """ % (id, x1,y1,x2,y2, sc1,s2r,sc2,sc3)
    return gradient, fill

def use_plain(data,id, color_bandwidth, color_lowest):
    vectors = data[1]
    z = vectors[:,2]
    color = int( (np.average(z) - color_lowest) / color_bandwidth * COLOR_MAX)
    return '', '#%06x' % color


def _bounding_box(vectors):
    x = vectors[:,0]
    y = vectors[:,1]
    z = vectors[:,2]
    return max(x),min(x),max(y),min(y),max(z),min(z)
# Calc methods
def _sort(vectors):
    temp = None
    for i in [0,1,0]:
        if vectors[i,2] > vectors[i+1,2]:
            temp = vectors[i].copy()
            vectors[i] = vectors[i+1]
            vectors[i+1] = temp
    return vectors





def create_facet_with_dots(data, color_bandwidth, color_lowest, id=-1):
    gradient, polygon = create_facet(data, color_bandwidth, color_lowest, id=id)
    # create_facet과 decide_Gradient_vector가 공통으로 쓰는 값들
    normal,vectors,attr = data

    # A,B,C = [vectors[order] for order in np.argsort(vectors[:,2])]
    A,B,C = _sort(vectors)

    maxx,minx,maxy,miny,maxz,minz = _bounding_box(vectors)
    width  = maxx - minx
    height = maxy - miny

    if width * height == 0:
        # line = (A[:2], B[:2])
        # return '', create_line(line)
        return '', ''

    # 이하 자세한 건 연구노트 참고.
    b = np.subtract(B,A) # distance between points B and A.
    c = np.subtract(C,A)
    #
    m = (b[0]*c[2] - b[2]*c[0]) / (b[2]*c[1] - b[1]*c[2])
    m2 = m*m
    C_altx = (m2*A[0] + C[0] + m*c[1]) / (m2 + 1)  # C'x
    C_alty = m * C_altx
    B_altx = (m2*A[0] + B[0] + m*b[1]) / (m2 + 1)  # B'x
    B_alty = m * B_altx
    #
    x1 = (A[0] - minx) / width
    y1 = (A[1] - miny) / height
    x2 = (C_altx - minx) / width
    y2 = (m*C_altx - miny) / height # C'y == m * C'x

    # OPTIONAL
    s2r = (B_altx - A[0]) / (C_altx - A[0]) # stop-point2 ratio

    sc1 = int( (A[2] - color_lowest) / color_bandwidth * 0xFFFFFF )
    sc2 = int( (B[2] - color_lowest) / color_bandwidth * 0xFFFFFF )
    sc3 = int( (C[2] - color_lowest) / color_bandwidth * 0xFFFFFF )
    
    print('box', [x1,y1,x2,y2])
    print('alts', [B_altx, C_altx])
    print('s2r', s2r)
    print('sc', [sc1,sc2,sc3])

    A,B,C = np.add(np.dot([A,B,C], MULT), TRAN)

    B_alty, C_alty = np.add(np.dot([m*B_altx,m*C_altx], MULT), TRAN)
    B_altx, C_altx = np.add(np.dot([B_altx,C_altx], MULT), TRAN)

    gradient = """
    <linearGradient id="g%d" x1="%f" y1="%f" x2="%f" y2="%f">
        <stop offset="0" stop-color="#%06x"/>
        <stop offset="%f" stop-color="#%06x"/>
        <stop offset="1" stop-color="#%06x"/>
    </linearGradient>
    """ % (id, x1,y1,x2,y2, sc1,s2r,sc2,sc3)
    polygon = """
    <polygon fill="url(#g%d)" points="%f,%f %f,%f %f,%f"/>
    """ % (id, A[0],A[1], B[0],B[1], C[0],C[1])

    dot = ''
    if id == 100:
        dot = """
        <circle a="" cx="%f" cy="%f" r="1"/>
        <circle b_alt="" cx="%f" cy="%f" r="1"/>
        <circle c_alt="" cx="%f" cy="%f" r="1"/>
        """ % (A[0],A[1], B_altx,B_alty, C_altx,C_alty)
    else:
        dot = ''
    return gradient, polygon, dot