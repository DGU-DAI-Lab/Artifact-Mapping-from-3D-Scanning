import numpy as np
import cv2
from matplotlib import pyplot as plt

# ----------------
# 최소바운딩박스를 이용하여 회전각을 구하여 각도로 반환하는 함수
def ROTATION_mbb_deg(cv2_bgr_img):
    src_color = cv2_bgr_img.copy()
    src_gray  = cv2.cvtColor(src_color, cv2.COLOR_BGR2GRAY)

    # 전처리 I: 배경제거 - Threshold1이 244인 이유는, 이미지 압축에 따라 배경이 균일하게 255의 값을 가지고 있는 것이 아니기 때문이다.
    nobackground = cv2.threshold(src_gray, 244, 255, cv2.THRESH_TOZERO_INV)[-1]

    # 최소 바운딩 박스 검출
    contours = cv2.findContours(nobackground, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]
    maxCont  = max(contours,key=cv2.contourArea)
    minRect  = cv2.minAreaRect(maxCont)

    # 회전각 추출
    degree   = minRect[-1]
    return degree

# ----------------
if __name__ == '__main__':
    fname = 'test_model/Gobe.jpg' # 'test_model/Jonggi.png' # 
    image = cv2.imread(fname)

    degree = ROTATION_mbb_deg(image)
    
    # ---- 실험 결과를 확인하기 위한 코드
    size   = image.shape[:2]
    center = tuple([i//2 for i in size])

    newsize   = (max(size), max(size))
    newcenter = tuple([i//2 for i in newsize])

    dy,dx = [newcenter[i]-center[i] for i in range(2)]

    # 이미지를 이동/회전시키기 위한 선형 변환 행렬
    translateM = np.float32([
        [1,0,dx],
        [0,1,dy]
    ])
    rotateM = cv2.getRotationMatrix2D(newcenter, degree, 1)

    # 이미지의 형태를 정사각형으로 바꿈
    output = np.zeros(image.shape, dtype=image.dtype)
    output = cv2.resize(output, newsize)
    output[:size[0],:size[1]] = cv2.threshold(image, 244, 255, cv2.THRESH_TOZERO_INV)[-1]

    output = cv2.warpAffine(output, translateM, newsize)
    output = cv2.warpAffine(output, rotateM, newsize)

    # 바운딩 박스 표기
    contours = cv2.findContours(cv2.cvtColor(output, cv2.COLOR_BGR2GRAY), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]
    maxCont  = max(contours,key=cv2.contourArea)
    minRect  = cv2.minAreaRect(maxCont)
    minBoxPoints = np.int0(cv2.boxPoints(minRect))
    cv2.drawContours(output,[minBoxPoints],-1,(255,0,255),thickness=2)

    # ----
    fig, axs = plt.subplots(1)
    fig.suptitle('Min B.box')
    plt.imshow(output)
    plt.show()