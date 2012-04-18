__author__ = 'ohaas'

import numpy as ny
import matplotlib.pyplot as pp
import pop_code as pop

def gauss(x, mu, sigma):
    return ny.exp(-(x-mu)**2/(2.0*sigma**2))

class N(object):


    def __init__(self, mu, sigma, A=1):
        """
        mu IS WHERE THE MAXIMUM IS LOCATED, SIGMA SQUARED IS THE WIDTH AND A IS THE AMPLITUDE
        """
        self.sigma=sigma
        self.y=ny.zeros(361.0)
        self.x2=ny.arange( 0.0, 361.0, 1)
        for x in self.x2:
            self.y[x]= A*(gauss(x, mu, sigma) + gauss(x, mu-360, sigma) + gauss(x, mu+360, sigma))

    def activity(self, x1):
        """
         x1 IS THE POSITION IN DEGREES OF THE READ OUT ACTIVITY VALUE
        """
        return self.y[x1]

    def plot_act(self):
        x3=ny.arange(0,2*ny.pi,2*ny.pi/361)
        pp.polar(x3,self.y)
        pp.xlim(0,360)
        pp.xlabel('Spatial orientation in degree')
        pp.ylabel('Amplitude of neuronal activation')



if __name__ == '__main__':
    width=30
    angle = ny.arange(0.0, 360, 45.0)
    neurons = [N(degree, width) for degree in angle]
    for i in ny.arange(0,len(angle)):
        N.plot_act(neurons[i])
    pp.show()

