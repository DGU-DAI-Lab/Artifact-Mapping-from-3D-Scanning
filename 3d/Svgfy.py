import numpy as np

# SVG Config.
WIDTH = HEIGHT = 8196 # SVG 이미지 크기
MULT = 6 # SVG 출력 배율 (확대)
TRAN = 640 # SVG 출력 원점이동 (가로,세로 동일)
THIC = 2 # 출력할 선의 두께
COLO = 0x0 # 출력할 선의 색상

COLOR_MAX = 0xFFFFFF # Gradient method, max color

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
    svg += create_polygons(surface, 'gradient')
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
    Ax,Ay,Bx,By = np.add(np.dot(line,MULT),TRAN)
    return '<polyline points="%f,%f %f,%f"/>'%(Ax,Ay,Bx,By)

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
    A_alt,B_alt,C_alt = _grad_by_differential(data)
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





