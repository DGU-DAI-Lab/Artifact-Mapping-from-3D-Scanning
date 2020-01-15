import numpy as np
import cv2

winname = 'Quadrant Div.'
varname_cutX = 'cut_x'
varname_cutY = 'cut_y'
varname_showLine, default_showLine, max_showLine = 'show line (off/on)', 0, 1
manual_width = 640

img, gray   = get_gray_img(width=manual_width)
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