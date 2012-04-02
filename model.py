__author__ = 'ohaas'

import numpy as ny
import matplotlib.pyplot as pp
import pop_code as pc
import neuron
from matplotlib.mlab import bivariate_normal
from scipy.signal import convolve2d




class Area(object):
    def __init__(self, main_size, square_size, start, gauss_width, time_frames, time_step_length):
        self.main_size=main_size
        self.square_size=square_size
        self.start=start
        self.gauss_width=gauss_width
        self.time_frames=time_frames
        self.delta_t=time_step_length


    def get_gauss_kernel(self,sigma):
        """
        return a two dimesional gausian kernel of shape (size*(1/resolution),size*(1/resolution))
        with a std deviation of std
        """

        self.size=self.main_size
        self.sigma=sigma
        self.res=1
        x,y = ny.mgrid[-self.size/2:self.size/2:self.res,-self.size/2:self.size/2:self.res]
        return bivariate_normal(x,y,sigma,sigma)

    def do_v1(self,net_in, net_fb, C):
        self.v1_t= net_in * (1 + C * net_fb)
        return self.v1_t

    def do_v2(self, Gx):

        if type(Gx).__name__=='int' :
            self.v2_t=self.v1_t**2

        else:
            v2_t=self.v1_t
            for n in ny.arange(0,8):
                #x,y = ny.mgrid[-self.size/2:self.size/2:self.res,-self.size/2:self.size/2:self.res]
                v2_t[:,:,n]=convolve2d (v2_t[:,:,n]**2,Gx, 'same')
            self.v2_t=v2_t

        return self.v2_t

    def do_v3(self):
        self.v3_t=(self.v2_t-(0.5*self.v2_t))/(0.01+self.v2_t)
        return self.v3_t

    def do_all_(self, net_in, net_fb, C, Gx):
        self.do_v1(net_in, net_fb, C)
        self.do_v2(Gx)
        v3_t = self.do_v3()
        return v3_t

    def storage(self,t):
        """
        definition of model storage variables
        """
        out=ny.zeros((self.main_size,self.main_size,8,self.time_frames/self.delta_t))
        return out[:,:,:,t]

    def input(self, t):
        """
        definition of initial population codes for different time steps
        """
        self.pop_code=ny.zeros((self.main_size,self.main_size,8,self.time_frames/self.delta_t))

        for i in ny.arange(0,self.time_frames/self.delta_t):
            j=pc.Population(self.main_size, self.square_size, self.start, self.gauss_width)
            self.pop_code[:,:,:,i]=j.print_pop(j.initial_pop_code())
            self.start=ny.add(self.start,self.delta_t)
        return self.pop_code[:,:,:,t]


if __name__ == '__main__':
    are=Area(30,6,2,30,10,2)
    V1=are.do_all_(are.input(0),0,100,0)
    MT=are.do_all_(V1,0,0,are.get_gauss_kernel(7))
    V1_1=are.do_all_(are.input(1),MT,100,0)
    MT_1=are.do_all_(V1_1,0,0,are.get_gauss_kernel(7))
    p=pc.Population(30,6,2,30)
    #p.show_vectors(p.initial_pop_code())
    #p.show_vectors(MT)
    #p.plot_pop(p.initial_pop_code())
    p.plot_pop(MT_1)
