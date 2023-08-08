import numpy as np
import random

def create_2d_affine_tranformation(a = 0.0, b = 0.0, c = 0.0, d = 0.0, e = 0.0, f = 0.0):
    return (np.array([[a, b], [c, d]]), np.array([e, f]))

f1 = create_2d_affine_tranformation(d=.16)
f2 = create_2d_affine_tranformation(.85, .04, -.04, .85, f = 1.6)
f3 = create_2d_affine_tranformation(.20, -.26, .23, .22, f = 1.6)
f4 = create_2d_affine_tranformation(-.15, .28, .26, .24, f = 0.44)

def iterator(point):
    rand = random.random()
    if rand < .01:
        return np.matmul(f1[0], point) + f1[1]
    elif rand < .86:
        return np.matmul(f2[0], point) + f2[1]
    elif rand < .93:
        return np.matmul(f3[0], point) + f3[1]
    else:
        return np.matmul(f4[0], point) + f4[1]


# defining bound of our canvas
width, height = 600, 1000 # width and height are 0 
regularIMGcartesian = create_2d_affine_tranformation(a=1.0, d=-1.0, e=0, f=height)

# over origin is at bottom center
xp, xd, yp, yd = 3, -3, 10, 0
def translate(point):
    x, y = point[0], point[1]
    if x < xd:
        x = xd
    elif x > xp:
        x = xp
    if y < yd:
        y = yd
    elif y > yp:
        y = yp
    p = np.array([(x - xd)/(xp - xd) * width, (y - yd)/(yp - yd) * height])
    return np.matmul(p, regularIMGcartesian[0]) + regularIMGcartesian[1]

# drawing svg circle for a point at specified co-ordinate and with specified color
# draw_point = lambda x, y, c: f'<circle cx="{x}" cy="{y}" r="{.1/np.sqrt(x_max*x_max + y_max*y_max)}" fill="{c}"/>\n'
draw_point = lambda x, y, c: f'<rect x="{x}" y="{y}" width="1.5" height="1.5" fill="{c}"/>'

# writing svg file
def draw_barnsley_fern(iter_func, filename = 'py_barnsley_fern.svg'):
    with open(filename, 'w') as img:
        img.write(f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">')
        
        point = np.array([0.0, 0.0])
        for _ in range(50000):
            point = iter_func(point)
            p = translate(point)
            img.write(draw_point(p[0], p[1], '#446F49'))

        img.write('</svg>')


draw_barnsley_fern(iterator)