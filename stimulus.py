__author__ = 'ohaas'

import numpy as ny
import matplotlib.pyplot as pp

class stimulus(object):
      pass


def __init__(self, num):
    self.background=ny.ones((num, num, 3))

def square(self, size):
    for s in ny.arange(2,2+size):
        self.background[2,s]=ny.zeros(3)
        self.background[s,2]=ny.zeros(3)
        self.background[2+size,s]=ny.zeros(3)
        self.background[s,2+size]=ny.zeros(3)
    return pp.imshow(self.background)

#stimulus(num), pic.square(size)
pic = stimulus(30)
print pic.square(4)


