__author__ = 'ohaas'

import numpy as ny
import matplotlib.pyplot as pp

class N(object):
    pass

# mu IS WHERE THE MAXIMUM IS LOCATED, SIGMA SQUARED IS THE WIDTH, x1 IS THE POSITION IN DEGREES OF THE READ OUT ACTIVITY VALUE
# AND A IS THE AMPLITUDE

    def __init__(self, mu, sigma, A):
        self.y=ny.zeros(361.0)
        self.x2=ny.arange( 0.0, 361.0, 1 )
        for x in self.x2:
            self.y[x]= A*((ny.exp(-(x-mu)**2/(2.0*sigma**2))+ny.exp(-(x-(mu-360))**2/(2.0*sigma**2))+ny.exp(-(x-(mu+360))**2/(2.0*sigma**2))))


    def activity(self, x1):
        return self.y[x1]

    def plot_act(self):
        x3=ny.arange(0,2*ny.pi,2*ny.pi/361)
        pp.plot(x3,self.y)
        pp.xlim(0,360)
        pp.xlabel('Spatial orientation in degree')
        pp.ylabel('Amplitude of neuronal activation')
      #  pp.show()

width=30.0

#Neuron0=N(0.0,width, 1)
#Neuron1=N(45.0,width, 1)
#Neuron2=N(90.0,width, 1)
#Neuron3=N(135.0,width, 1)
#Neuron4=N(180.0,width, 1)
#Neuron5=N(225.0,width, 1)
#Neuron6=N(270.0,width, 1)
#Neuron7=N(315.0,width, 1)
#a=N.activity(Neuron1, 10.0)
#print(a)
#N.plot_act(Neuron0)
#N.plot_act(Neuron1)
#N.plot_act(Neuron2)
#N.plot_act(Neuron3)
#N.plot_act(Neuron4)
#N.plot_act(Neuron5)
#N.plot_act(Neuron6)
#N.plot_act(Neuron7)
#pp.show()

