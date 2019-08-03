import numpy as np
from stl import mesh

from src import DepthSegment as ds

testmodel_cp = ['../test_model/토기 예시 데이터/3D 스캔 파일/토기%d.stl'%i for i in range(7)]
testmodel_c  = '../test_model/Cube.stl'
testmodel_t  = '../test_model/Torus.stl'
testmodel_tu = '../test_model/Torus Upward.stl'

def main():
    model = testmodel_cp[2]

    m = mesh.Mesh.from_file(model)
    d = ds.DepthSegmentation(m)

    o,s,i = [len(_d) for _d in d]
    print(o, s, i, o+i+s)

    # SVG Config.
    WIDTH = HEIGHT = 2048
    MULT = 5
    TRAN = 600
    THIC = .5

    svg_file = '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="%d" height="%d">\n' % (WIDTH, HEIGHT)
    
    li = d[1]
    if True:
        for A,B in li:
            A = np.add(np.dot(A,MULT),TRAN)
            B = np.add(np.dot(B,MULT),TRAN)
            svg_file += '<polyline points="%lf,%lf %lf,%lf" style="fill:none;stroke:black;stroke-width:%f"/>'%(A[0],A[1],B[0],B[1],THIC)
    else:
        svg_file+='<polyline points="'
        li = ds._sort_to_connected_list(li)
        for i in range(0,li.size,2):
            svg_file += '%lf,%lf '%(li.item(i),li.item(i+1))
        svg_file += '" style="fill:none;stroke:black;stroke-width:%f" />'%(THIC)
    svg_file += '</svg>'

    f = open('../output/section.svg','w')
    f.write(svg_file.replace(' "','"'))
    f.close()

print('\n>>> Start.\n')
main()
print('\n>>> Done.\n')
exit()