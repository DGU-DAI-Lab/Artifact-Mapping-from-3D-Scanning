import cv2
import numpy as np

class Artifacts_Face():
    def __init__(self):
        self.gray_image = None
        self.bin_image = {
            'default' : None,
            'body'   : [], # Multi Layer Bin images
            'window' : []
        }
        self.contours = None

    def build_from(self, gray):
        self.gray_image = gray
        self.binarize()
        self.findContour()

    def binarize(self):
        src = self.gray_image
        r, src = cv2.threshold(src, 250, 255, cv2.THRESH_BINARY_INV)
        src = cv2.morphologyEx(src, cv2.MORPH_CLOSE,(5,5), iterations=3)
        self.bin_image['default'] = src

    def findContour(self):
        contours, hierarchy = cv2.findContours(self.bin_image['default'], cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        self.contours = contours

        for i in range(len(contours)):
            cont = contours[i]
            hier = hierarchy[0,i]
            canvas = np.zeros(self.gray_image.shape, np.uint8)
            cv2.drawContours(canvas, [cont], 0, 255, -1) # Fill

            isBody = hier[3] < 0
            if isBody:
                self.bin_image['body'].append(canvas)
            else:
                self.bin_image['window'].append(canvas)