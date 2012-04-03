__author__ = 'ohaas'

import numpy as ny
import matplotlib.pyplot as pp
import pop_code as pc
import neuron
from matplotlib.mlab import bivariate_normal
from scipy.signal import convolve2d

def get_gauss_kernel(sigma, size=10, res=1):
    """
    return a two dimesional gausian kernel of shape (size*(1/resolution),size*(1/resolution))
    with a std deviation of std
    """
    x,y = ny.mgrid[-size/2:size/2:res,-size/2:size/2:res]
    return bivariate_normal(x, y, sigma, sigma)

class Stage(object):
    def __init__(self, Gx, C):
        self.Gx = Gx
        self.C = C

    def do_v1(self, net_in, net_fb):
        v1_t= net_in + (self.C * net_fb * net_in)
        return v1_t

    def do_v2(self, v1_t):

        if not len (self.Gx):
            return v1_t**2

        v2_t = v1_t
        for n in ny.arange(0, 8):
            v2_t[:,:,n] = convolve2d (v2_t[:,:,n]**2, self.Gx, 'same')

        return v2_t

    def do_v3(self, v2_t):
        v3_t = (v2_t - (0.5*v2_t))/(0.01+v2_t)
        return v3_t

    def do_all(self, net_in, net_fb):
        v1_t = self.do_v1(net_in, net_fb)
        v2_t = self.do_v2(v1_t)
        v3_t = self.do_v3(v2_t)
        return v3_t


class Model(object):

    def __init__(self, main_size, square_size, start, gauss_width, time_frames, delta_t):
        self.main_size = main_size
        self.square_size = square_size
        self.gauss_width = gauss_width
        self.time_frames = time_frames
        self.delta_t = delta_t
        self.start = start


    def create_input(self):
        """
        definition of initial population codes for different time steps (is always the same one!!!)
        """
        pop_code=ny.zeros((self.main_size, self.main_size, 8, self.time_frames/self.delta_t))
        start = self.start
        for i in ny.arange(0, self.time_frames/self.delta_t):
            j = pc.Population(self.main_size, self.square_size, start, self.gauss_width)
            pop_code[:,:,:,i] = j.print_pop(j.initial_pop_code())
            start=ny.add(self.start, self.delta_t)

        return pop_code


    def run_model_full(self, t):
        p = pc.Population(self.main_size, self.square_size, self.start, self.gauss_width)

        input = self.create_input()

        V1 = Stage([], 100)
        MT = Stage(get_gauss_kernel(7), 0)

        X = ny.zeros((self.main_size, self.main_size, 8, t))
        X[:,:,:, 0] = p.initial_pop_code()

        fb = 0
        for d_t in ny.arange(1, t):
            inp = input[:,:,:,d_t]
            v1 = V1.do_all(inp, fb)
            mt = MT.do_all(v1, 0)
            X[:,:,:, d_t] = mt

            fb = mt # new feedback is old output

        return X


    def integrated_motion_direction(self):
        self.st = self.start - self.delta_t
        self.h_v_edges = ny.zeros((self.time_frames/self.delta_t,2))

        X = self.run_model_full (self.time_frames/self.delta_t)
        print X.shape

        for i in ny.arange(0,self.time_frames/self.delta_t):
            j=pc.Population(self.main_size, self.square_size, self.st+self.delta_t, self.gauss_width)
            pop_c = X[:,:,:,i]
            self.h_v_edges[i,:]=j.create_vectors(pop_c)
            pp.plot(i,self.h_v_edges[i,0],'k+')
            pp.plot(i,self.h_v_edges[i,1],'k*')
            print self.h_v_edges[i,0]

        x=ny.arange(0,self.time_frames/self.delta_t)
        y=0*x+45
        pp.plot(x,y)
        pp.xlim(-0.2,4.2)
        pp.ylim(-1,91)

if __name__ == '__main__':


    #M=Area(30,6,2,30,10,1)
    M = Model(30, 6, 2, 30, 10, 1)
    M.integrated_motion_direction()
    #p=pc.Population(30,6,2,30)
    #M.input(1)
    pp.show()

