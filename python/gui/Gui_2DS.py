from tkinter import filedialog as fd
import numpy as np
import cv2

COLOR_WHITE = (0xFF, 0xFF, 0xFF)
COLOR_PRIMARY = (0xFF, 0x00, 0xFF)
COLOR_SECONDARY = (0x00, 0xFF, 0xFF)

############################################################

root = None # for tkinter

def Rotate_byBoundingBox():
    winname = 'B. Box'
    varname_mode, default_mode, max_mode = 'on/off', 1, 1
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
    varname_lineNum, default_lineNum, max_lineNum = 'line num.', None, None
    manual_width = 640
    
    onProcStart()

    img, gray = get_gray_img(width=manual_width)
    size,center = get_size_n_center(img.shape)

    canny = cv2.Canny(gray, 250, 255)
    lines = cv2.HoughLines(canny, 1, np.pi/180, 100)

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
        return cv2.line(img,(x1,y1),(x2,y2),COLOR_WHITE,1)

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
    
    default_lineNum = max_lineNum = len(lines)

    cv2.namedWindow(winname)
    cv2.createTrackbar(varname_lineNum, winname, default_lineNum, max_lineNum, update)
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

    varname_part, default_part, max_part = 'show part (front/rear/all)', 2, 2
    varname_mode, default_mode, max_mode = 'view mode (raw/no bg/partial/final)', 2, 3
    varname_winproc, default_winproc, max_winproc = '(partial) window process level', 4, 4
    varname_bodyproc, default_bodyproc, max_bodyproc = '(partial) body process level', 1, 1
    varname_mdilate, default_mdilate, max_mdilate = '(partial) mask dilation', 32, 255
    manual_width = 480

    WINDOW_CANNY_THRESH = (230,255)

    BODY_COLOR = COLOR_PRIMARY
    WINDOW_COLOR = COLOR_SECONDARY
    
    onProcStart()
    
    path = '../test_model/2ds-preproc/토기2/' #open_dir()

    # Preproc 2D-Segment.
    dseg = [get_img(path=path+'/outer.png',width=manual_width),
            get_img(path=path+'/inner.png',width=manual_width)]

    def remove_background(x):
        _,th = cv2.threshold(x, 250,255, cv2.THRESH_BINARY_INV)
        return cv2.morphologyEx(th, cv2.MORPH_CLOSE,(5,5), iterations=3)

    def sort_contours(part_binary):
        contours,hierarchy = cv2.findContours(part_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        bodies = []
        windows = []
        for i in range(len(contours)):
            cont, hier = contours[i], hierarchy[0,i]
            if (hier[3] < 0): # isBody?
                bodies.append(cont)
            else:
                windows.append(cont)
        return bodies, windows

    def draw_contours(raw, contours, color):
        canvas = np.zeros(raw.shape[0:2], dtype=np.uint8)
        canvas = cv2.drawContours(canvas, contours, -1, 255, 1) # Fill
        c_canvas = cv2.cvtColor(canvas, cv2.COLOR_GRAY2BGR)
        c_canvas[np.where((canvas != 0))] = color
        return c_canvas

    def draw_masks(raw, contours):
        canvas = np.zeros(raw.shape[0:2], dtype=np.uint8)
        canvas = cv2.drawContours(canvas, contours, -1, 255, -1) # Fill
        return canvas

    def apply_mask(raw,mask,expand):
        ksize = 2*expand +1
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(ksize,ksize))
        dilated = cv2.dilate(mask,kernel)
        return cv2.bitwise_and(raw,raw,mask=dilated) #???

    def proc_window(raw, window_contours, mask_expand, thresh=WINDOW_CANNY_THRESH):
        pallete = np.zeros(raw.shape, np.uint8)
        for roi in window_contours:
            mask = draw_masks(raw, [roi])
            masked_overfit = apply_mask(raw,mask,mask_expand+1)
            canny = cv2.Canny(masked_overfit, thresh[0],thresh[1], apertureSize=3)
            masked_fit = apply_mask(canny,mask,mask_expand)

            output = cv2.cvtColor(masked_fit, cv2.COLOR_GRAY2BGR)
            output[np.where((output!=[0,0,0]).all(axis=2))] = WINDOW_COLOR
            pallete = cv2.add(pallete,output)
        return pallete # 3-channel
    
    def proc_body(raw, body_contours):
        pallete = np.zeros(raw.shape, np.uint8)
        cv2.drawContours(pallete,body_contours,-1,BODY_COLOR,1)
        return pallete

    def update(x):
        part = cv2.getTrackbarPos(varname_part, winname)
        progress = cv2.getTrackbarPos(varname_mode, winname)
        winproc = cv2.getTrackbarPos(varname_winproc, winname)
        bodyproc = cv2.getTrackbarPos(varname_bodyproc, winname)
        mdilate = cv2.getTrackbarPos(varname_mdilate, winname)

        def process(part):
            raw = dseg[part]
            gray = cv2.cvtColor(raw,cv2.COLOR_BGR2GRAY)
            no_bg = remove_background(gray)
            b_cont, w_cont = sort_contours(no_bg)
            b_draw, w_draw = [draw_contours(raw,cont,color) for cont, color in [(b_cont,BODY_COLOR), (w_cont,WINDOW_COLOR)]]
            b_mask, w_mask = [draw_masks(raw, c) for c in [b_cont, w_cont]]
            b_maskexp, w_maskexp = [apply_mask(raw,m,mdilate) for m in [b_mask, w_mask]]
            b_proc, w_proc = [proc_body(raw,b_cont), proc_window(raw,w_cont,mdilate)]
            return {
                'raw'   : raw,
                'gray'  : gray,
                'no_bg' : no_bg,
                'contours' : {
                    'body'   : b_cont,
                    'window' : w_cont
                },
                'contours-drawn' : {
                    'body' : b_draw, # equal as b_proc
                    'window' : w_draw
                },
                'masks' : {
                    'body'   : cv2.cvtColor(b_mask,cv2.COLOR_GRAY2BGR),
                    'window' : cv2.cvtColor(w_mask,cv2.COLOR_GRAY2BGR)
                },
                'masks-expanded' : {
                    'body'   : b_maskexp,
                    'window' : w_maskexp
                },
                'proc' : {
                    'body'   : b_proc,
                    'window' : w_proc
                },
                'output' : cv2.add(b_proc, w_proc)
            }

        def prepare(part):
            res = process(part)
            pallete = None
            if progress is 0: # MODE_0 show original image
                pallete = res['raw']

            elif progress is 1: # MODE_1 show no-background area
                pallete = res['no_bg']

            elif progress is 2: # MODE_2 show detailed process
                pallete = np.zeros(res['raw'].shape, dtype=np.uint8)
                if bodyproc is 1: # show body processed
                    pallete = cv2.add(pallete, res['proc']['body'])

                if winproc is 1: # show window contours
                    pallete = cv2.add(pallete, res['contours-drawn']['window'])
                        
                elif winproc is 2: # show mask
                    pallete = cv2.add(pallete, res['masks']['window'])
                        
                elif winproc is 3: # show expanded mask
                    pallete = cv2.add(pallete, res['masks-expanded']['window'])
                        
                elif winproc is 4: # show window processed
                    pallete = cv2.add(pallete, res['proc']['window'])
    
            else: # MODE_3 show full contour
                pallete = res['output']

            return pallete.copy()

        if part is 2: # Show all
            p = [prepare(0), prepare(1)]
            pallete = None
            h0,w0 = p[0].shape[0], p[0].shape[1]
            h1,w1 = p[1].shape[0], p[1].shape[1]
            try:
                pallete = np.zeros((max(h0,h1),max(w0,w1),p[0].shape[2]),dtype=np.uint8)
                pallete[0:h0,0:w0,:] = cv2.add(pallete[0:h0,0:w0,:], p[0])
                pallete[0:h1,0:w1,:] = cv2.addWeighted(pallete[0:h1,0:w1,:], .5, p[1], .5, 0)
            except IndexError as err:
                pallete = np.zeros((max(h0,h1),max(w0,w1)),dtype=np.uint8)
                pallete[0:h0,0:w0] = cv2.add(pallete[0:h0,0:w0], p[0])
                pallete[0:h1,0:w1] = cv2.addWeighted(pallete[0:h1,0:w1], .5, p[1], .5, 0)
            finally:
                cv2.imshow(winname, pallete)
        else:
            cv2.imshow(winname, prepare(part))
    
    cv2.namedWindow(winname)
    cv2.createTrackbar(varname_part, winname, default_part, max_part, update)
    cv2.createTrackbar(varname_mode, winname, default_mode, max_mode, update)
    cv2.createTrackbar(varname_winproc, winname, default_winproc, max_winproc, update)
    cv2.createTrackbar(varname_bodyproc, winname, default_bodyproc, max_bodyproc, update)
    cv2.createTrackbar(varname_mdilate, winname, default_mdilate, max_mdilate, update)
    update(None)
        

def Mapping_DS_LocalBoxSelect():
    pass

def Mapping_DirectContour():
    winname = 'Canny Contour'
    varname_th1, default_th1, max_th1 = 'threshold1', 250, 255
    varname_th2, default_th2, max_th1 = 'threshold2', 255, 255
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