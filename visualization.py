from classes import *
from ivisual import *
import numpy as np
from PIL import ImageGrab

scene = canvas(title='Ideal Gas')
scene.autoscale=True
s = isentropic()
boxsize = s.boxsize
b = box(pos=((boxsize[1]+boxsize[0])/2.,
                 (boxsize[3]+boxsize[2])/2.,
                 (boxsize[5]+boxsize[4])/2.),
            size=(boxsize[1]-boxsize[0],
                  boxsize[3]-boxsize[2],
                  boxsize[5]-boxsize[4]),
            color=color.white,
            opacity=0.1)

iteration = 1000
for i in range(iteration):
    rate(100)
    s.update(rate=10)
    b.size=(s.boxsize[1]-s.boxsize[0],
                  s.boxsize[3]-s.boxsize[2],
                  s.boxsize[5]-s.boxsize[4])
    # im = ImageGrab.grab((0,0,500,500))
    # fname = './images/test' + str(i) + '.png'
    # im.save(fname)
