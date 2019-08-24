from tkinter import filedialog as fd
import numpy as np
import cv2

def Rotate_byBoundingBox():
    img = get_img()
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    h,w = gray_img.shape
    _, bin_img = cv2.threshold(gray_img, 245, 255, cv2.THRESH_BINARY_INV)

    contour,_ = cv2.findContours(bin_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    rect = cv2.minAreaRect(contour[0])
    # Draw box (not necessary)
    box = np.int0(cv2.boxPoints(rect))
    img = cv2.drawContours(img,[box],-1,(0xFF, 0x00, 0xFF))
    # Calc rotation matrix
    _,_,theta = rect
    rmat = cv2.getRotationMatrix2D((w//2,h//2), theta, 1)
    output = cv2.warpAffine(img, rmat, (w,h))
    # Show on scr.
    cv2.imshow('original', img)
    cv2.imshow('rotated', output)
    cv2.waitKey()

def Rotate_byHoughTransform():
    file_name = open_image()

def Rotate_Direct():
    window_name, manual_width = 'Rotate Direct', 640
    img = get_img()
    h,w,_ = img.shape
    size = (manual_width, (manual_width*h)//w)
    center = (size[0]//2, size[1]//2)
    resized = img_resize(img, size)

    cv2.namedWindow(window_name)
    cv2.createTrackbar('theta', window_name, 0, 360, nothing)
    while True:
        theta = cv2.getTrackbarPos('theta', window_name)
        rmat = cv2.getRotationMatrix2D(center, theta, 1)
        output = cv2.warpAffine(resized, rmat, size)
        cv2.imshow(window_name, output)
        if cv2.waitKey(1) & 0xFF == 27: break

def Mapping_DS_QuadrantDivision():
    pass

def Mapping_DS_ClosedWindowAutoDetection():
    pass

def Mapping_DS_LocalBoxSelect():
    pass

def Mapping_DirectContour():
    window_name, manual_width = 'Canny Contour', 640
    default_th1, default_th2 = 250, 255

    gray_img = get_gray_img()
    h,w = gray_img.shape
    size = (manual_width, (manual_width*h)//w)
    resized_img = img_resize(gray_img, size)

    cv2.namedWindow(window_name)
    cv2.createTrackbar('threshold1', window_name, default_th1, 255, nothing)
    cv2.createTrackbar('threshold2', window_name, default_th2, 255, nothing)
    
    while True:
        th1 = cv2.getTrackbarPos('threshold1', window_name)
        th2 = cv2.getTrackbarPos('threshold2', window_name)
        canny = cv2.Canny(resized_img, th1, th2)
        cv2.imshow(window_name, canny)
        if cv2.waitKey(1) & 0xFF == 27: break



def set_root(window):
    global root
    root = window

def open_image():
    file_name = fd.askopenfilename(
        initialdir = "../test_model/",
        title = "Select Image",
        filetypes = (
            ("Image files", "*.png *.jpg"),
            ("all files", "*.*")
        ))
    return file_name

def open_dir():
    file_dir = fd.askdirectory(
        initialdir = "../test_model/",
        title = "Select Pre-D-Segmented Images")

def readUnicodePath(path):
    stream = open(path,"rb")
    bytes = bytearray(stream.read())
    numpyArray = np.asarray(bytes,dtype=np.uint8)
    img_bgr = cv2.imdecode(numpyArray, cv2.IMREAD_UNCHANGED)
    return img_bgr

def get_img():
    file_name = open_image()
    return readUnicodePath(file_name)

def get_gray_img():
    img = get_img()
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def get_bin_img(thresh):
    gray = get_gray_img()
    retval, dst = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY_INV)
    return dst

def img_resize(img, new_size):
    new_width, new_height = new_size
    return cv2.resize(
            img,
            (new_width, new_height),
            interpolation=cv2.INTER_AREA
        )

def nothing(x):
    pass