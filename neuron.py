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
    Neuron0=N(0.0,width)
    Neuron1=N(45.0,width)
    Neuron2=N(90.0,width)
    Neuron3=N(135.0,width)
    Neuron4=N(180.0,width)
    Neuron5=N(225.0,width)
    Neuron6=N(270.0,width)
    Neuron7=N(315.0,width)
    #a=N.activity(Neuron1, 10.0)
    #print(a)
    N.plot_act(Neuron0)
    N.plot_act(Neuron1)
    N.plot_act(Neuron2)
    N.plot_act(Neuron3)
    N.plot_act(Neuron4)
    N.plot_act(Neuron5)
    N.plot_act(Neuron6)
    N.plot_act(Neuron7)
    pp.show()

