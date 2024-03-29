__author__ = 'ohaas'

import numpy as ny
import matplotlib.pyplot as pp
import pop_code as pop

def gauss(x, mu, sigma):
    return ny.exp(-(x-mu)**2/(2.0*sigma**2))

class N(object):


    def __init__(self, sigma, A=1):
        """
        mu IS WHERE THE MAXIMUM IS LOCATED, SIGMA SQUARED IS THE WIDTH AND A IS THE AMPLITUDE
        """
        self.sigma=sigma
        self.A=A


    def neuron_gauss(self, mu):
        y=ny.zeros(361.0)
        x2=ny.arange( 0.0, 361.0, 1)
        for x in x2:
            y[x]= self.A*(gauss(x, mu, self.sigma) + self.A*gauss(x, mu-360, self.sigma) + self.A*gauss(x, mu+360, self.sigma))
        return y


    def plot_act(self):
        angle = ny.arange(0.0, 360, 45.0)
        neurons = [N(self.sigma).neuron_gauss(degree) for degree in angle]
        x3=ny.arange(0,2*ny.pi,2*ny.pi/361)
        ax = pp.subplot(111,polar=True)
        for i in ny.arange(0,len(angle)):
            ax.plot(x3,neurons[i], label='$neuron$ $%i$ $(\mu=%i\degree)$' %(i+1,i*45))
        pp.xlim(0,360)
        y=ny.arange(0,1.01,0.01)
        x=0.0*y

        # Shink current axis by 20%
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])


        pp.polar(x,y,color='blue', ls='--', lw=3, label='$Amplitude$\n$of$ $neuronal$\n$activation')
        pp.xlabel('Spacial orientation in degree with neuron %s=%.2f' % (u"\u03C3",self.sigma))
        pp.title('Neuronal tuning curves')

        # Put a legend to the right of the current axis
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))




if __name__ == '__main__':
#    width=30
#    angle = ny.arange(0.0, 360, 45.0)
#    neurons = [N(degree, width) for degree in angle]
#    for i in ny.arange(0,len(angle)):
#        N.plot_act(neurons[i])
    Neuron=N(30)
    Neuron.plot_act()
    pp.show()

