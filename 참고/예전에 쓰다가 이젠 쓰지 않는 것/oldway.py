import cv2
import numpy as np

class Oldway():
    def __init__(self, artifact):
        self.GAUSS_KERNEL_SIZE = 3
        self.GAUSS_SIGMA = 25
        self.THRESH = 240
        self.CONTOUR_THICKNESS = 1

        self.image = artifact.raw
        self.preproc()

    def preproc(self):
        kernel = (self.GAUSS_KERNEL_SIZE, self.GAUSS_KERNEL_SIZE)
        src = self.image
        src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        src = cv2.GaussianBlur(src, kernel, self.GAUSS_SIGMA)
        self.image = src

    def byEdge(self):
        src = self.image.copy()
        src = cv2.Canny(src, 50, 150, apertureSize=3)
        return self.getContours(src)

    def byThresh(self):
        src = self.image.copy()
        ret, src = cv2.threshold(src, self.THRESH, 255, cv2.THRESH_BINARY_INV)
        src = cv2.morphologyEx(src, cv2.MORPH_CLOSE, (5,5), iterations=4)
        return self.getContours(src)

    def getContours(self, bin_image):
        canvas = np.zeros(gray.shape, np.uint8)
        contours, hierarchy = cv2.findContours(bin_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(canvas, contours, -1, 255, self.CONTOUR_THICKNESS)
        return canvas