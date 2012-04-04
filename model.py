__author__ = 'ohaas'

import numpy as ny
import matplotlib.pyplot as pp
import pop_code as pc
import neuron
from matplotlib.mlab import bivariate_normal
from scipy.signal import convolve2d
import ConfigParser as cp

def get_gauss_kernel(sigma, size=7, res=0.5):
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

    def __init__(self, cfg_file):

        cfg = cp.RawConfigParser()

        cfg.read(cfg_file)

        self.main_size = cfg.getint('Input', 'main_size')
        self.square_size = cfg.getint('Input', 'square_size')
        self.time_frames = cfg.getint('Input', 'time_frames')
        self.delta_t = cfg.getint('Input', 'delta_t')
        self.start = cfg.getint('Input', 'start')

        self.gauss_width = cfg.getfloat('PopCode', 'neuron_sigma')

        v1_C = cfg.getint('V1', 'C')
        mt_kernel_sigma =  cfg.getfloat('MT', 'kernel_sigma')
        mt_kernel_size =  cfg.getfloat('MT', 'kernel_size')
        mt_kernel_res =  cfg.getfloat('MT', 'kernel_res')

        self.V1 = Stage([], v1_C)
        self.MT = Stage(get_gauss_kernel(mt_kernel_sigma, mt_kernel_size, mt_kernel_res), 0)

    def create_input(self):
        """
        definition of initial population codes for different time steps (is always the same one!!!)
        """
        pop_code=ny.zeros((self.main_size, self.main_size, 8, self.time_frames))
        start = self.start
        for i in ny.arange(0, self.time_frames):
            j = pc.Population(self.main_size, self.square_size, start, self.gauss_width)
            pop_code[:,:,:,i] = j.print_pop(j.initial_pop_code())
            start=ny.add(self.start, self.delta_t)

        return pop_code


    def run_model_full(self, t):
        p = pc.Population(self.main_size, self.square_size, self.start, self.gauss_width)

        input = self.create_input()

        X = ny.zeros((self.main_size, self.main_size, 8, t))
        X[:,:,:, 0] = p.initial_pop_code()

        fb = 0
        for d_t in ny.arange(1, t):
            inp = input[:,:,:,d_t-1]
            v1 = self.V1.do_all(inp, fb)
            mt = self.MT.do_all(v1, 0)
            X[:,:,:, d_t] = mt

            fb = mt # new feedback is old output

        return X


    def integrated_motion_direction(self):
        start = self.start
        self.h_v_edges = ny.zeros((self.time_frames,2))

        X = self.run_model_full (self.time_frames)

        for i in ny.arange(0,self.time_frames):
            j=pc.Population(self.main_size, self.square_size, start, self.gauss_width)
            pop_c = X[:,:,:,i]
            self.h_v_edges[i,:]=j.create_vectors(pop_c)

            pp.plot(i,self.h_v_edges[i,0],'k+')
            pp.plot(i,self.h_v_edges[i,1],'k*')
            start=ny.add(self.start, self.delta_t)
            print self.h_v_edges[i,0], self.h_v_edges[i,1]

        x=ny.arange(-0.2,self.time_frames)
        y=0*x+45
        pp.plot(x,y)
        pp.xlim(-0.2,self.time_frames+0.2)
        pp.ylim(-1,91)

if __name__ == '__main__':

    M = Model('model.cfg')
    M.integrated_motion_direction()
    pp.show()

