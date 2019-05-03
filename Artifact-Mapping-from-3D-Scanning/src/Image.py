import numpy as np
import cv2

class Image:
    IMAGE_COLOR = 0
    IMAGE_GRAYSCALE = 1
    IMAGE_BINARY = 2

    BLACK = 0
    WHITE = 255

    # Constructor
    def __init__(self, src):
        self.array = None
        self.type = None
        # 
        self.set(src)

    # Method for changing the image of instances.
    def set(self, src):
        self.type = self._getType(src)
        self.array = src

    # 
    def _getType(self, src):
        (w,h,channel) = src.shape

        is_color = channel is Image.IMAGE_COLOR
        if is_color:
            return Image.IMAGE_COLOR
        for i in range(src.size):
            px = src.item(i)
            is_binary = (px is BLACK) or (px is WHITE)
            if not is_binary:
                return Image.IMAGE_GRAYSCALE
        return Image.IMAGE_BINARY

    # ���͸� ����
    def filter2D(self, fliter):
        

    def _apply(self):
        Image.list.append(self)

