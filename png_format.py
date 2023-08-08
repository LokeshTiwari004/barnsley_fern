from random import random
from numba import njit
from numpy import zeros, uint8
from PIL import Image as im

f1 = (0, 0, 0, .16, 0, 0)
f2 = (.85, .04, -.04, .85, 0, 1.6)
f3 = (.20, -.26, .23, .22, 0, 1.6)
f4 = (-.15, .28, .26, .24, 0, 0.44)
f = (f1, f2, f3, f4)

@njit
def iterator(x, y, r):
    global f
    if r < 0.01:
        a = f[0]
        x = a[0] * x + a[1] * y + a[4]
        y = a[2] * x + a[3] * y + a[5]
    elif r < 0.86:
        a = f[1]
        x = a[0] * x + a[1] * y + a[4]
        y = a[2] * x + a[3] * y + a[5]
    elif r < 0.93:
        a = f[2]
        x = a[0] * x + a[1] * y + a[4]
        y = a[2] * x + a[3] * y + a[5]
    else:
        a = f[3]
        x = a[0] * x + a[1] * y + a[4]
        y = a[2] * x + a[3] * y + a[5]
    return x, y


x, y = 0, 0
xr, yr = (-3,3), (0, 10)
width, height = 3840, 2160 # 4k resolution
# width, height = 2400, 4000 # 4k resolution


xrl, yrl = xr[1] - xr[0], yr[1] - yr[0]
ex_fac = min(width // xrl, height // yrl)
center = ((width - xrl * ex_fac) // 2 - xr[0] * ex_fac , (height - yrl * ex_fac) // 2 + yr[1] * ex_fac)
img_affine  = (ex_fac, 0, 0, -ex_fac, center[0], center[1])


@njit
def regularIMGcartesian(x, y):
    return int(x * img_affine[0] + y * img_affine[1] + img_affine[4]), int(x * img_affine[2] + y * img_affine[3] + img_affine[5]) 

x, y = 0, 0
img = zeros((height, width, 3), dtype=uint8)
for _ in range(5000000):
    px, py = regularIMGcartesian(x, y)
    if -1 < px < width and  -1 < py < height:
        img[py, px] = [186, 254, 1]

    r = random()
    x, y = iterator(x, y, r)

im.fromarray(img).save('py_bernsley_fern.png')