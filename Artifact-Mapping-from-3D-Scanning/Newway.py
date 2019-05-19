import cv2
import numpy as np

class Newway():
    def __init__(self, artifact):
        self.BORDER_SIZE = 36
        self.CANNY_THRESH = (78, 188)
        self.CONTOUR_THICKNESS = 1
        self.artifact = artifact
        self.windows = {}
        self.body = {}
        self.combination = {}

        for face_name, face in self.artifact.faces.items():
            windows = self.proc_windows(face)
            body = self.proc_body(face)

            self.windows[face_name] = windows
            self.body[face_name] = body
            self.combination[face_name] = cv2.add(windows, body)

    def proc_windows(self, face):
        src = face.gray_image
        canvas = np.zeros(src.shape, np.uint8)
        for win_roi in face.bin_image['window']:
            win = self.apply_mask(src, win_roi, self.BORDER_SIZE+1)
            win = cv2.Canny(win, self.CANNY_THRESH[0], self.CANNY_THRESH[1], apertureSize=3)
            win = self.apply_mask(win, win_roi, self.BORDER_SIZE)
            canvas = cv2.add(win, canvas)
        return canvas

    def proc_body(self, face):
        src = face.gray_image
        canvas = np.zeros(src.shape, np.uint8)
        for body in face.bin_image['body']:
            contours, _ = cv2.findContours(body, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            cv2.drawContours(canvas, contours, -1, 255, self.CONTOUR_THICKNESS)
        return canvas
                
    def apply_mask(self, src, mask, borderSize):
        ksize = 2*borderSize + 1
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(ksize,ksize))
        dilation = cv2.dilate(mask,kernel)
        return cv2.bitwise_and(src, src, mask=dilation)
