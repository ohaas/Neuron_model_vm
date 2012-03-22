__author__ = 'ohaas'

import numpy as ny
import matplotlib.pyplot as pp
from matplotlib.mlab import bivariate_normal

class N(object):
    pass

# mu IS WHERE THE MAXIMUM IS LOCATED, SIGMA SQUARED IS THE WIDTH, x1 IS THE POSITION IN DEGREES OF THE READ OUT ACTIVITY VALUE
# AND A IS THE AMPLITUDE

    def __init__(self, mu, sigma, x1 , A):
        self.y=ny.zeros(361.0)
        x2=ny.arange( 0.0, 361.0, 1 )
        for x in x2:
            self.y[x]= A*25.0*((1.0/(sigma*ny.sqrt(2*ny.pi)))*(ny.exp(-(x-mu)**2/(2.0*sigma**2))+ny.exp(-(x-(mu-360))**2/(2.0*sigma**2))+ny.exp(-(x-(mu+360))**2/(2.0*sigma**2))))
        print self.y[x1]

        pp.plot(x2,self.y)
        pp.xlim(0,360)
        pp.xlabel('Spatial orientation in degree')
        pp.ylabel('Amplitude of neuronal activation')
        pp.show()



N(10.0,10.0, 0.0, 1)
