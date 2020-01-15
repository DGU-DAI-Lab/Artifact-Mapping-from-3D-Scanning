import tkinter as tk
import stl
from stl import mesh
import numpy as np

from src import DepthSegment as ds
from src import Svgfy as svg
from stl import mesh
import time


def set_root(window):
    global root
    root = window

def Rotate_UseCogCov():
    pass

def Rotate_Direct():
    pass

def Mapping_SVG_noBackground():
    pass

def Mapping_SVG_plainBackground():
    pass

def Mapping_SVG_LinearGradientByNormal():
    pass

def Mapping_SVG_LinearGradientByRatio():
    pass

def Mapping_WindowDetect():
    pass

def main(fname):
    print('3ds')
        
    obj = mesh.Mesh.from_file(fname)
    
    print('\n>>> Start.\n')
    print('D-Segmentation start.')
    start = time.time()

    d = ds.DepthSegmentation(obj)

    front,section,rear = d

    end = time.time()
    print('D-Segmentation done.')
    print('took %f seconds.' % (end-start))
    print()

    total_before = obj.__len__()
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

    print('\n>>> Done.\n')