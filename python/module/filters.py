import numpy as np
import cv2
from matplotlib import pyplot as plt

# ----------------

fname = 'test_model/Gobe.jpg'

src = cv2.imread(fname)
gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

ksize = 3
kernel = (3,3)
blurFilters = [
    # ('No Blur', lambda x: x),
    ('Average Filter', lambda x: cv2.filter2D(x, -1, np.ones(kernel, np.float32)/(ksize**2))),
    ('Gaussian Filter', lambda x: cv2.GaussianBlur(x, kernel, 1)),
    ('Bilateral Filter', lambda x: cv2.bilateralFilter(x, ksize, 1, 1)),
    ('Median Filter', lambda x: cv2.medianBlur(x, ksize))
]
edgeFilters = [
    ('No Edge Detect.', lambda x: x),
    ('Sobel Method', lambda x: cv2.convertScaleAbs(cv2.add(cv2.Sobel(x, cv2.CV_64F, 1, 0, ksize=ksize), cv2.Sobel(x, cv2.CV_64F, 0, 1, ksize=ksize)))),
    ('Canny Method', lambda x: cv2.Canny(x, 32, 224)),
    ('Laplacian Filter', lambda x: cv2.convertScaleAbs(cv2.Laplacian(x, ksize)))
]

bl = len(blurFilters)
el = len(edgeFilters)
inches = 8

fig, axs = plt.subplots(2,2)
fig.set_size_inches(2*inches,2*inches)

for x in [0,1]:
    for y in [0,1]:
        bn, bf = blurFilters[x*2 + y]
        a = axs[x,y]
        im = bf(gray)
        im = cv2.Canny(im, 32, 224)
        a.set(xlabel=bn)
        a.imshow(im)

# for bi in range(bl):
#     bn, bf = blurFilters[bi]
#     for ei in range(el):
#         en, ef = edgeFilters[ei]

#         a = axs[bi,ei]
#         im = ef(bf(gray))
#         a.imshow(im)

#         labels = [
#             en if bi == bl - 1 else '',
#             bn if ei == 0      else ''
#         ]

#         a.set(xlabel=labels[0],ylabel=labels[1])

# ----------------

plt.savefig('figure.png')