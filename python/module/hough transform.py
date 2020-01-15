import numpy as np
import cv2
from matplotlib import pyplot as plt

# ----------------

def my_drawLine(img, line):
    rho,theta = line
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 +1000*(-b))
    y1 = int(y0 +1000*(a))
    x2 = int(x0 -1000*(-b))
    y2 = int(y0 -1000*(a))
    return cv2.line(img,(x1,y1),(x2,y2),(255,0,255),2)

# ----------------

fname = 'test_model/Jonggi.png'
src = cv2.imread(fname)

size = src.shape[1::-1]
center = tuple([i//2 for i in size])

canny = cv2.Canny(src, 250, 255)
lines = cv2.HoughLines(canny, 0.64, np.pi/180, 72)

#### TODO : Select best theta

lines = lines[:,0] # Unpack unnecessary wrap

# -pi/2 ~ +pi*3/2의 범위로 조정
for i in range(len(lines)):
    theta = lines[i,1]
    if theta > np.pi * 2/3:
        lines[i,1] = theta - np.pi


lines = sorted(lines, key=lambda x: x[1])
lines = np.array(lines)

thetas = lines[:,1]
theta = np.mean(thetas[:15]) # 선택된 기울기 영역과 그 평균

[my_drawLine(src, line) for line in lines]


####

degree = theta * 180/np.pi -  90 # rad 2 deg

rmat = cv2.getRotationMatrix2D(center, degree, 1)
applied = cv2.warpAffine(src, rmat, size)

# ----------------

fig, axs = plt.subplots(2)

fig.suptitle('H. Trans.')

axs[0].plot(thetas, 'r.')
axs[0].set(xlabel='Lines', ylabel='theta (rad)')
axs[1].imshow(applied)

plt.show()