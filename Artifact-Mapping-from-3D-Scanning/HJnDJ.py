import numpy as np
import cv2

img = cv2.imread('1.jpg')

wGauss = img.copy()
woGauss = img.copy()

wCanvas = np.zeros(img.shape, np.uint8)
woCanvas = np.zeros(img.shape, np.uint8)

wGauss = cv2.GaussianBlur(wGauss,(7,7),0)
for im, cvs in [(wGauss, wCanvas), (woGauss, woCanvas)]:
    im = cv2.Canny(im,100,200)
    c, h = cv2.findContours(im, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    cv2.drawContours(cvs, c, -1, (255,255,255), 1)
cv2.imshow('Default none', woCanvas)
cv2.imshow('Default gauss', wCanvas)
cv2.waitKey(0)

cut1=img[0:256, 0:381]
cut2=img[0:256, 381:801]
cut3=img[257:664,0:381]
cut4=img[257:664,381:801]
ret, thr=cv2.threshold(img,255,255,0)
cut_b1=thr[0:256, 0:381]
cut_b2=thr[0:256, 381:801]
cut_b3=thr[257:664,0:380]
cut_b4=thr[257:664,381:801]


blur1=cv2.bilateralFilter(cut1,3,50,50)
blur1=cv2.bilateralFilter(blur1,3,60,60)
canny1=cv2.Canny(blur1,100,200)
contours, hierachy=cv2.findContours(canny1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(cut_b1, contours, -1, (255,255,255), 1)


blur2=cv2.medianBlur(cut2,5)
blur2=cv2.medianBlur(blur2,7)
canny2=cv2.Canny(blur2,100,200)
contours2, hierachy=cv2.findContours(canny2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(cut_b2, contours2, -1, (255,255,255), 1)

blur3=cv2.GaussianBlur(cut3,(3,3),0)

blur3=cv2.GaussianBlur(blur3,(7,7),0)
canny3=cv2.Canny(blur3,40,60)
contours3, hierachy=cv2.findContours(canny3, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(cut_b3, contours3, -1, (255,255,255), 1)

blur4=cv2.medianBlur(cut4,3)
blur4=cv2.medianBlur(blur4,5)
canny4=cv2.Canny(blur4,78,188)
contours4, hierachy=cv2.findContours(canny4, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(cut_b4, contours4, -1, (255,255,255), 1)

import numpy as np
import cv2

GAUSS_KERNEL = (3,3)
GAUSS_SIGMA = 25
ITERATIONS = 4

def findContours(src): # src : single-channel image
    global GAUSS_KERNEL, GAUSS_SIGMA, ITERATIONS
    # Smoothing
    src = cv2.GaussianBlur(src, GAUSS_KERNEL, GAUSS_SIGMA)
    # Transform into a binary Image
    ret, bin_src = cv2.threshold(src, 240, 255, cv2.THRESH_BINARY_INV)
    # Morphology-OPENING operation to remove extra noises
    canvas = np.zeros(src.shape, np.uint8)

    bin_src = cv2.morphologyEx(bin_src, cv2.MORPH_OPEN, (5,5), iterations=ITERATIONS)
    contours, hierarchy = cv2.findContours(bin_src, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    print('Contours found : %d' % (len(contours)))

    for cont in contours:
        cv2.drawContours(canvas, [cont], 0, 255, 1)
    return canvas

# Default
slice = cv2.imread('1_slice.jpg', cv2.IMREAD_GRAYSCALE)
inner = cv2.imread('1_inner.jpg', cv2.IMREAD_GRAYSCALE)
outer = cv2.imread('1_outer.jpg', cv2.IMREAD_GRAYSCALE)

canvas = np.zeros(slice.shape, np.uint8)
for partial in [inner, outer, slice]:
    retval = findContours(partial)
    canvas = cv2.add(canvas, retval)

w, h = slice.shape
M = np.float32([
        [1, 0,   0],
        [0, 1, ITERATIONS * -1]
    ])
canvas = cv2.warpAffine(canvas, M, (h,w))

cv2.imshow('dj', canvas)

cv2.imshow('hj',thr)

thr = cv2.cvtColor(thr, cv2.COLOR_BGR2GRAY)
image = cv2.add(thr, canvas)
cv2.imshow('bs',image)
cv2.waitKey(0)
cv2.destroyAllWindows()



