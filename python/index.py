# -*- coding: utf-8 -*-
from tkinter import filedialog as fd

from gui import Gui_2DS as g2d
from gui import Gui_3DS as g3d

def main():
    filename = fd.askopenfilename(initialdir = "../test_model/",filetypes = (("model files","*.jpg *.stl"),("all files","*.*")))
    
    ext = filename.split('.')[-1]
    if ext == 'stl':
        # 3D - D-Segmentation
        g3d.main(filename)

    else:
        # 2D - D-Segmentation
        g2d.main(filename)
    
main()