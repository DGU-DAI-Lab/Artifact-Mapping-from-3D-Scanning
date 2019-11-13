from tkinter import filedialog as fd
import numpy as np
import cv2

import matplotlib.pyplot as plt

THICKNESS = 2
COLOR_WHITE = (0xFF, 0xFF, 0xFF)
COLOR_PRIMARY = (0xFF, 0xFF, 0x00)
COLOR_SECONDARY = (0x00, 0xFF, 0xFF)

############################################################

root = None # for tkinter

def Mapping_DS_QuadrantDivision():
    winname = 'Quadrant Div.'
    varname_cutX = 'cut_x'
    varname_cutY = 'cut_y'
    varname_showLine, default_showLine, max_showLine = 'show line (off/on)', 0, 1
    manual_width = 640
    
    onProcStart()

    img, gray = get_gray_img(width=manual_width)
    size,center = get_size_n_center(img.shape)
    default_cutX, default_cutY = center
    max_cutX, max_cutY = size

    # HJ's 구현 계획 : 마우스이벤트를 사용하여 원하는 부분만 이미지를 자르고 그 부분을 저장하여 기존 방식대로 적용.

    def update(x):
        cut_x = cv2.getTrackbarPos(varname_cutX, winname)
        cut_y = cv2.getTrackbarPos(varname_cutY, winname)
        toggle = cv2.getTrackbarPos(varname_showLine, winname)

        pallete = img.copy()
        cut = [
            pallete[0:cut_y,    cut_x+1:-1], # 제1사분면
            pallete[cut_y+1:-1, 0:cut_x   ], # 제3사분면
            pallete[0:cut_y,    0:cut_x   ], # 제2사분면
            pallete[cut_y+1:-1, cut_x+1:-1]] # 제4사분면
        blurred = [
            cv2.bilateralFilter(cut[0],3,50,50),
            cv2.medianBlur(cut[1],5),
            cv2.GaussianBlur(cut[2],(3,3),0),
            cv2.medianBlur(cut[3],3)]
        edged = [cv2.Canny(b,100,200) for b in blurred]
        results = [cv2.findContours(c, cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE) for c in edged]
        for i in [0,1,2,3]:
            #cv2.threshold(cut[i], 127, 255, cv2.THRESH_BINARY)
            contours, _ = results[i]
            cv2.drawContours(cut[i],contours,-1,COLOR_PRIMARY,1,thickness=THICKNESS)

        if toggle is 1:
            cv2.line(pallete,(cut_x,0),(cut_x,size[1]),COLOR_SECONDARY,1)
            cv2.line(pallete,(0,cut_y),(size[0],cut_y),COLOR_SECONDARY,1)
        cv2.imshow(winname, pallete)

    cv2.namedWindow(winname)
    cv2.createTrackbar(varname_cutX, winname, default_cutX, max_cutX, update)
    cv2.createTrackbar(varname_cutY, winname, default_cutY, max_cutY, update)
    cv2.createTrackbar(varname_showLine, winname, default_showLine, max_showLine, update)
    update(None)


############################################################

# SUPPORTIVES

def negativeColor(color_img):
    for i in range(color_img.size):
        color_img.itemset(i, 255 - color_img.item(i))
    return color_img

def set_root(window):
    global root
    root = window

def open_image():
    file_name = fd.askopenfilename(
        initialdir = "../test_model/2ds-preproc/",
        title = "Select Image",
        filetypes = (
            ("Image files", "*.png *.jpg"),
            ("all files", "*.*")
        ))
    return file_name

def open_dir():
    file_dir = fd.askdirectory(
        initialdir = "../test_model/2ds-preproc/",
        title = "Select Pre-D-Segmented Images")
    return file_dir

def readUnicodePath(path):
    print('opening', path)
    stream = open(path,"rb")
    bytes = bytearray(stream.read())
    numpyArray = np.asarray(bytes,dtype=np.uint8)
    img_bgr = cv2.imdecode(numpyArray, cv2.IMREAD_UNCHANGED)
    return img_bgr

def onProcStart():
    cv2.destroyAllWindows()

def get_img(path=None,width=None):
    if path is None:
        path = open_image()

    img = readUnicodePath(path)
    if width is None:
        return img

    new_size = get_new_size(width,img.shape)
    return img_resize(img, new_size)

def get_gray_img(width=None):
    img = get_img(width=width)
    return img, cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def get_new_size(new_width,shape):
    h = shape[0]
    w = shape[1]
    return (new_width, (new_width*h)//w)

def get_size_n_center(shape):
    size = (shape[1],shape[0])
    center = (size[0]//2, size[1]//2)
    return size, center

def img_resize(img, new_size):
    new_width, new_height = new_size
    return cv2.resize(
        img,
        (new_width, new_height),
        interpolation=cv2.INTER_AREA)

def rad2deg(rad):
    return rad*180/np.pi

def nothing(x):
    pass