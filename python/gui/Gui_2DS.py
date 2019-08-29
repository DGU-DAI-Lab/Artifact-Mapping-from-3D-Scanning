from tkinter import filedialog as fd
import numpy as np
import cv2

COLOR_PRIMARY = (0xFF, 0x00, 0xFF)
COLOR_SECONDARY = (0x00, 0xFF, 0xFF)

############################################################

root = None # for tkinter

def Rotate_byBoundingBox():
    winname = 'B. Box'
    varname_mode, default_mode, max_mode = 'on/off', 0, 1
    manual_width = 640
    
    onProcStart()

    img, gray = get_gray_img(width=manual_width)
    size,center = get_size_n_center(img.shape)

    _, bin_img = cv2.threshold(gray, 245, 255, cv2.THRESH_BINARY_INV)
    contour,_ = cv2.findContours(bin_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    rect = cv2.minAreaRect(contour[0])
    # Draw box (not necessary)
    box = np.int0(cv2.boxPoints(rect))
    img = cv2.drawContours(img,[box],-1,COLOR_PRIMARY)
    # Calc rotation matrix
    _,_,degree = rect
    rmat = cv2.getRotationMatrix2D(center, degree, 1)
    output = cv2.warpAffine(img, rmat, size)
    # Show on scr.
    def update(mode):
        if mode is 0:
            # Rotated
            cv2.imshow(winname, output)
        else:
            cv2.imshow(winname, img)

    cv2.namedWindow(winname)
    cv2.createTrackbar(varname_mode, winname, default_mode, max_mode, update)
    update(default_mode)

def Rotate_byHoughTransform():
    winname = 'H. Trans.'
    varname_lineNum, default_lineNum = 'line num.', 0
    manual_width = 640
    
    onProcStart()

    img, gray = get_gray_img(width=manual_width)
    size,center = get_size_n_center(img.shape)

    canny = cv2.Canny(gray, 250, 255)
    lines = cv2.HoughLines(canny, 1, np.pi/180/4, 100)

    def drawLine(img, line):
        rho,theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 +1000*(-b))
        y1 = int(y0 +1000*(a))
        x2 = int(x0 -1000*(-b))
        y2 = int(y0 -1000*(a))
        return cv2.line(img,(x1,y1),(x2,y2),COLOR_PRIMARY,1)

    def update(lineNum):
        pallete = img.copy()
        if lineNum is len(lines):
            # Show all found lines.
            for line in lines:
                drawLine(pallete, line)
            cv2.imshow(winname, pallete)
        else:
            # Rotate and show the selected line.
            drawLine(pallete, lines[lineNum])
            _,theta = lines[lineNum,0]
            degree = rad2deg(theta) - 90

            rmat = cv2.getRotationMatrix2D(center, degree, 1)
            output = cv2.warpAffine(pallete, rmat, size)
            cv2.imshow(winname, output)

    cv2.namedWindow(winname)
    cv2.createTrackbar(varname_lineNum, winname, default_lineNum, len(lines), update)
    update(default_lineNum)

def Rotate_Direct():
    winname = 'Rotate Direct'
    varname_deg, default_deg, max_deg = 'degree', 0, 360
    manual_width = 640
    
    onProcStart()
    
    img = get_img(width=manual_width)
    size,center = get_size_n_center(img.shape)

    def update(degree):
        rmat = cv2.getRotationMatrix2D(center, degree, 1)
        output = cv2.warpAffine(img, rmat, size)
        cv2.imshow(winname, output)

    cv2.namedWindow(winname)
    cv2.createTrackbar(varname_deg, winname, default_deg, max_deg, update)
    update(default_deg)

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
            cv2.drawContours(cut[i],contours,-1,COLOR_PRIMARY,1)\

        if toggle is 1:
            cv2.line(pallete,(cut_x,0),(cut_x,size[1]),COLOR_SECONDARY,1)
            cv2.line(pallete,(0,cut_y),(size[0],cut_y),COLOR_SECONDARY,1)
        cv2.imshow(winname, pallete)

    cv2.namedWindow(winname)
    cv2.createTrackbar(varname_cutX, winname, default_cutX, max_cutX, update)
    cv2.createTrackbar(varname_cutY, winname, default_cutY, max_cutY, update)
    cv2.createTrackbar(varname_showLine, winname, default_showLine, max_showLine, update)
    update(None)
    

def Mapping_DS_ClosedWindowAutoDetection():
    winname = 'Windows Auto Detection'

    varname_prog, default_prog, max_prog = 'view mode', 3, 3
    varname_winproc, default_winproc, max_winproc = 'window process level', 1, 4
    varname_bodyproc, default_bodyproc, max_bodyproc = 'body process level', 1, 1
    varname_part, default_part, max_part = 'show part (front/rear)', 0, 1
    manual_width = 640

    MASK_EXPAND = 32
    WINDOW_CANNY_THRESH = (250,255)
    
    onProcStart()
    
    path = open_dir()
    # Preproc 2D-Segment.
    dseg = [get_img(path=path+'/outer.png',width=manual_width),
            get_img(path=path+'/inner.png',width=manual_width)]

    def removeBG(x):
        _,th = cv2.threshold(x, 250,255, cv2.THRESH_BINARY_INV)
        return cv2.morphologyEx(th, cv2.MORPH_CLOSE,(5,5), iterations=3)

    def sort(part_binary):
        contours,hierarchy = cv2.findContours(part_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        bodies = []
        windows = []
        for i in range(len(contours)):
            cont, hier = contours[i], hierarchy[0,i]
            pallete = np.zeros(part.shape[0:2], np.uint8)
            cv2.drawContours(pallete, [cont], 0, 255, -1) # Fill
            if (hier[3] < 0): # isBody?
                bodies.append(pallete)
            else:
                windows.append(pallete)
        return bodies, windows

    def apply_mask(img,mask,expand):
        ksize = 2*expand +1
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(ksize,ksize))
        dilated = cv2.dilate(mask,kernel)
        return cv2.bitwise_and(img,img,mask=dilated) #???

    def proc_window(part,windows):
        pallete = np.zeros(part.shape, np.uint8)
        for roi in windows:
            overfit = apply_mask(part,roi,MASK_EXPAND+1)
            canny = cv2.Canny(overfit,WINDOW_CANNY_THRESH[0],WINDOW_CANNY_THRESH[1],apertureSize=3)
            fit = apply_mask(canny,roi,MASK_EXPAND)
            fit = cv2.cvtColor(fit,cv2.COLOR_GRAY2BGR)
            pallete = cv2.add(pallete,fit)
        return pallete
    
    def proc_body(part,bodies):
        pallete = np.zeros(part.shape, np.uint8)
        for body in bodies:
            contours,_ = cv2.findContours(body,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            cv2.drawContours(pallete,contours,-1,COLOR_PRIMARY,1)
        return pallete

    results = []
    for part in dseg:
        gray = cv2.cvtColor(part,cv2.COLOR_BGR2GRAY)
        no_bg = removeBG(gray)
        bodies,windows = sort(no_bg)
        body_proced = proc_body(part,bodies)
        window_proced = proc_window(part,windows)
        results.append({
            'raw' : part,
            'no_bg' : no_bg,
            'body' : bodies,
            'window' : windows,
            'body_proc' : body_proced,
            'window_proc' : window_proced,
            'output' : cv2.add(body_proced, window_proced)
        })

    def update(x):
        part = cv2.getTrackbarPos(varname_part, winname)
        progress = cv2.getTrackbarPos(varname_prog, winname)
        winproc = cv2.getTrackbarPos(varname_winproc, winname)
        bodyproc = cv2.getTrackbarPos(varname_bodyproc, winname)

        res = results[part]
        if progress is 0: # show original image
            cv2.imshow(winname, res['raw'])

        elif progress is 1: # show no-background area
            cv2.imshow(winname, res['no_bg'])

        elif progress is 2: # show detailed process
            pallete = np.zeros(res['raw'].shape, dtype=np.uint8)
            if bodyproc is 1: # show body processed
                pallete = cv2.add(pallete, res['body_proc'])

            if winproc is 1: # show window contours
                cont,hier = cv2.findContours(res['no_bg'], cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
                for i in range(len(cont)):
                    if hier[0,i,3] < 0: # is body?
                        continue
                    cv2.drawContours(pallete, [cont[i]], 0, COLOR_SECONDARY, 1)
                    
            elif winproc is 2: # show mask
                for roi in res['window']:
                    mask = apply_mask(res['raw'],roi,0)
                    pallete = cv2.add(pallete, mask)
                    
            elif winproc is 3: # show expanded mask
                for roi in res['window']:
                    mask = apply_mask(res['raw'],roi,MASK_EXPAND)
                    pallete = cv2.add(pallete, mask)
                    
            elif winproc is 4: # show window processed
                pallete = cv2.add(pallete, res['window_proc'])

            cv2.imshow(winname, pallete)
    
        else: # show full contour
            cv2.imshow(winname, res['output'])

    cv2.namedWindow(winname)
    cv2.createTrackbar(varname_part, winname, default_part, max_part, update)
    cv2.createTrackbar(varname_prog, winname, default_prog, max_prog, update)
    cv2.createTrackbar(varname_winproc, winname, default_winproc, max_winproc, update)
    cv2.createTrackbar(varname_bodyproc, winname, default_bodyproc, max_bodyproc, update)
    update(None)
        

def Mapping_DS_LocalBoxSelect():
    pass

def Mapping_DirectContour():
    winname = 'Canny Contour'
    varname_th1, default_th1 = 'threshold1', 250
    varname_th2, default_th2 = 'threshold2', 255
    max_th = 255
    manual_width = 640
    
    onProcStart()

    img = get_img(width=manual_width)

    def update(x):
        th1 = cv2.getTrackbarPos(varname_th1, winname)
        th2 = cv2.getTrackbarPos(varname_th2, winname)
        canny = cv2.Canny(img, th1, th2)
        cv2.imshow(winname, canny)

    cv2.namedWindow(winname)
    cv2.createTrackbar(varname_th1, winname, default_th1, max_th, update)
    cv2.createTrackbar(varname_th2, winname, default_th2, max_th, update)
    update(None)


############################################################

# SUPPORTIVES

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
    print('opeing', path)
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