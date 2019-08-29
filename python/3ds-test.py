# -*- coding: utf-8 -*-

import numpy as np
from stl import mesh

from src import DepthSegment as ds
from src import Svgfy as svg

import time

testmodel_cp = ['../test_model/토기 예시 데이터/3D 스캔 파일/토기%d.stl'%i for i in range(7)]
testmodel_c  = '../test_model/Cube.stl'
testmodel_t  = '../test_model/Torus.stl'
testmodel_tu = '../test_model/Torus-Upward.stl'

def main():
    model = testmodel_tu

    # 1st Phase

    print('D-Segmentation start.')
    start = time.time()

    m = mesh.Mesh.from_file(model)
    d = ds.DepthSegmentation(m)

    front,section,rear = d

    end = time.time()
    print('D-Segmentation done.')
    print('took %f seconds.' % (end-start))
    print()

    total_before = m.__len__()
    total_after = len(front)+len(section)+len(rear)
    diff = total_before-total_after
    print('BEFORE >>> total : %d' % total_before)
    print('AFTER  >>> total : %d [ front : %d | section : %d | rear : %d ]' % (total_after, len(front), len(section), len(rear)))
    print('* %d (%.2f%%) decreased.' % ( diff, diff/total_before*100 ))
    print()


    # 2nd Phase

    print('SVG-Converting start.')
    start = time.time()

    def create_svg_file(path,data):
        f = open(path,'w')
        f.write(data)
        f.close()

    create_svg_file('../output/svg/section.svg', svg.build_section(section))
    create_svg_file('../output/svg/front.svg',   svg.build_surface(front))
    create_svg_file('../output/svg/rear.svg',    svg.build_surface(rear) )

    end = time.time()
    print('SVG-Converting done.')
    print('took %f seconds.' % (end-start))
    print()


print('\n>>> Start.\n')
main()
print('\n>>> Done.\n')
exit()