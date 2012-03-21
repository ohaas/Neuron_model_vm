__author__ = 'ohaas'

import numpy as ny
import matplotlib.pyplot as pp
from matplotlib.mlab import bivariate_normal

class Neuron(object):
    pass


def gauss(mu, sigma, x , A) :
    return A*25.0*((1.0/(sigma*ny.sqrt(2*ny.pi)))*ny.exp(-(x-mu)**2/(2.0*sigma**2)))

# mu IS WHERE THE MAXIMUM IS LOCATED, SIGMA SQUARED IS THE WIDTH AND A IS THE AMPLITUDE
x = ny.arange( 0.0, 360.0, 0.1 )
y = gauss( 50.0, 10.0, x , 1)
pp.plot(x,y)
pp.xlim(0,360)
pp.show()