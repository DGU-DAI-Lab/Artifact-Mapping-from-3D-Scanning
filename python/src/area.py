import cv2
import numpy as np
import matplotlib.pyplot as plt

MAX_IMG = 3

path = '../output/2ds/auto_window_detection/processed_windows/'

files = [cv2.cvtColor(src, cv2.COLOR_BGR2GRAY) for src in [cv2.imread(path+'window_masked_%d.png'%i) for i in range(0,MAX_IMG+1)]]

def nothing(x):
    pass

def set_imgNum(x):
    global imgNum
    imgNum = x

def set_minArea(x):
    global minArea
    minArea = x

def set_ksize(x):
    global ksize, kernel
    ksize = 2*x +1
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(ksize,ksize))

winname = 'test'

v_imgn = 'image_num'
v_mina = 'min_area'
v_ksize = 'k_size'


imgNum = 0
minArea = 30
set_ksize(0)

cv2.namedWindow(winname)
cv2.createTrackbar(v_imgn, winname, imgNum, MAX_IMG, set_imgNum)
cv2.createTrackbar(v_mina, winname, minArea, 1024, set_minArea)
cv2.createTrackbar(v_ksize, winname, 0, 32, set_ksize)

while True:
    img = files[imgNum].copy()
    frame = np.zeros(img.shape)

    proc = img
    proc = cv2.Canny(proc, 78,188)
    proc = cv2.morphologyEx(proc, cv2.MORPH_CLOSE, kernel)

    contours, hierarchy = cv2.findContours(proc, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    contour_data = []
    
    for i in range(len(contours)):
        contour_data.append({
            'contour' : contours[i],
            'hierarchy' : hierarchy[0,i],
            'area' : cv2.contourArea(contours[i])
        })

    for data in contour_data:
        if data['area'] < minArea:
            continue
        cv2.drawContours(frame, [data['contour']], -1, 255)

    areas = [d['area'] for d in contour_data]
    
    area_hist = [0] * 256
    for a in areas:
        area_hist[int(a)] += 1
    
    ###
    # PLOTTING
    plt.hist2d(range(256), area_hist, bins=256)
    plt.xlabel('contour index')
    plt.ylabel('area')
    plt.savefig('../output/area_plot.png')
    plt.close()
    ###
    print('go')

    cv2.imshow(winname, frame)
    cv2.waitKey(1)