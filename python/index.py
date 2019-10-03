# -*- coding: utf-8 -*-

""" Required libraries.
Built using python 3.7

numpy
numpy-stl
opency-python
pillow
"""

import tkinter as tk
from tkinter import *

from gui import Gui_2DS as ds2_gui
from gui import Gui_3DS as ds3_gui

def main():

    root = tk.Tk()

    # Defines
    menubar = Menu(root)

    menu_2D = Menu(menubar)
    menu_2D_Rotate  = Menu(menu_2D)
    menu_2D_Mapping = Menu(menu_2D)

    menu_3D = Menu(menubar)
    menu_3D_Rotate = Menu(menu_3D)
    menu_3D_Mapping = Menu(menu_3D)
    menu_3D_Mapping_SVG = Menu(menu_3D_Mapping)
    menu_3D_Mapping_SVG_CreateSurfaceBG = Menu(menu_3D_Mapping_SVG)

    # - 2D Rotate
    menu_2D_Rotate.add_command(label="by Bounding Box [DH]", command=ds2_gui.Rotate_byBoundingBox)
    menu_2D_Rotate.add_command(label="by Hough Transform [DJ]", command=ds2_gui.Rotate_byHoughTransform)
    menu_2D_Rotate.add_command(label="Direct", command=ds2_gui.Rotate_Direct)

    # - 2D Mapping
    menu_2D_Mapping.add_command(label="Edge Contour (Canny만 이용)", command=ds2_gui.Mapping_DirectContour)
    menu_2D_Mapping.add_command(label="사분면 분할식 영역 특성 기반 윤곽선검출 [HJ]", command=ds2_gui.Mapping_DS_QuadrantDivision)
    menu_2D_Mapping.add_command(label="2D-Segment & 폐곡선 Contour 검색식 자동 투창 선택형 [DJ]", command=ds2_gui.Mapping_DS_ClosedWindowAutoDetection)
    menu_2D_Mapping.add_command(label="(미구현) 사각형의 투창 영역 직접 선택형 [HJ]", command=ds2_gui.Mapping_DS_LocalBoxSelect)

    # - 3D Rotate
    menu_3D_Rotate.add_command(label="Use Vector : COG - COV [DJ]", command=ds3_gui.Rotate_UseCogCov)
    menu_3D_Rotate.add_command(label="Direct", command=ds3_gui.Rotate_Direct)

    # - 3D Mapping
    menu_3D_Mapping_SVG_CreateSurfaceBG.add_command(label="No Background", command=ds3_gui.Mapping_SVG_noBackground)
    menu_3D_Mapping_SVG_CreateSurfaceBG.add_command(label="Plain Background", command=ds3_gui.Mapping_SVG_plainBackground)
    menu_3D_Mapping_SVG_CreateSurfaceBG.add_command(label="LinearGradient by normal", command=ds3_gui.Mapping_SVG_LinearGradientByNormal)
    menu_3D_Mapping_SVG_CreateSurfaceBG.add_command(label="LinearGradient by ratio", command=ds3_gui.Mapping_SVG_LinearGradientByRatio)

    menu_3D_Mapping_SVG.add_cascade(label="Create Surface Background", menu=menu_3D_Mapping_SVG_CreateSurfaceBG)
    menu_3D_Mapping_SVG.add_command(label="Window Detection", command=ds3_gui.Mapping_WindowDetect)

    # Apply
    ds2_gui.set_root(root)
    ds3_gui.set_root(root)

    menu_2D.add_cascade(label="Rotate",  menu=menu_2D_Rotate)
    menu_2D.add_cascade(label="Mapping", menu=menu_2D_Mapping)
    menubar.add_cascade(label="2D Images", menu=menu_2D)

    menu_3D_Mapping.add_cascade(label="3D-Segment & SVGfy [DJ]", menu=menu_3D_Mapping_SVG)
    menu_3D.add_cascade(label="Rotate",  menu=menu_3D_Rotate)
    menu_3D.add_cascade(label="Mapping", menu=menu_3D_Mapping)
    menubar.add_cascade(label="(미구현) 3D Objects", menu=menu_3D)


    ds2_gui.Mapping_DS_ClosedWindowAutoDetection()

    root.config(menu=menubar)
    root.mainloop()

main()