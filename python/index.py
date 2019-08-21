# -*- coding: utf-8 -*-
from tkinter import filedialog as fd

from gui import Gui_2DS as ds2
from gui import Gui_3DS as ds3

def main():
    filename = fd.askopenfilename(initialdir = "../test_model/",filetypes = (("model files","*.jpg *.stl"),("all files","*.*")))
    
    ext = filename.split('.')[-1]
    if ext == 'stl':
        # 3D - D-Segmentation
        ds3.main(filename)
    else:
        # 2D - D-Segmentation
        ds2.main(filename)
    
main()