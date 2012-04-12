__author__ = 'ohaas'

import numpy as ny
import matplotlib.pyplot as pp
import pop_code as pc
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

        x = v1_t**2

        if not len (self.Gx):
            return x

        v2_t = ny.zeros_like (v1_t)
        for n in ny.arange(0, v1_t.shape[2]):
            v2_t[:,:,n] = convolve2d (x[:,:,n], self.Gx, 'same')

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

    def __init__(self, cfg_file, feedback=True):

        self.do_feedback = feedback

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

        self.mt_gauss = get_gauss_kernel(mt_kernel_sigma, mt_kernel_size, mt_kernel_res)

        self.V1 = Stage([], v1_C)
        self.MT = Stage(self.mt_gauss, 0)


    def show_mt_gauss(self):
        pp.figure(1)
        pp.imshow(self.mt_gauss, interpolation='nearest')

    def create_input(self):
        """
        definition of initial population codes for different time steps (is always the same one!!!)
        """
        I = ny.zeros((self.main_size, self.main_size, 8, self.time_frames+1))
        cur_frame = self.start
        for i in ny.arange(0, self.time_frames+1):
            j = pc.Population(self.main_size, self.square_size, cur_frame, self.gauss_width)
            I[:,:,:,i] = j.initial_pop_code()
            cur_frame += self.delta_t
            #j.show_vectors(I[:,:,:,i])
        return I


    def run_model_full(self):
        self.input = self.create_input()

        X = ny.zeros((self.main_size, self.main_size, 8, self.time_frames+1))
        X[:,:,:, 0] = self.input[:,:,:,0]

        fb = 0
        for d_t in ny.arange(1, self.time_frames+1):

            inp = self.input[:,:,:,d_t-1]
            v1 = self.V1.do_all(inp, fb)
            mt = self.MT.do_all(v1, 0)
            X[:,:,:, d_t] = mt


            if self.do_feedback:
                fb = mt # new feedback is old output

        return X


    def integrated_motion_direction(self):

        #fig = pp.figure()
        h_v_edges = ny.zeros((self.time_frames+1,2))
        self.cur_frame = self.start
        X = self.run_model_full ()

        for i in ny.arange(0,self.time_frames+1):

            pop = pc.Population(self.main_size, self.square_size, self.cur_frame, self.gauss_width)
            pp.figure(1)
            pp.imshow(self.mt_gauss, interpolation='nearest')
            pp.xlabel('Pixel')
            pp.ylabel('Pixel')
           # pp.suptitle('Spatial Kernel with sigma = %d, size= %d and resolution = %d' %)

            if i>0:
                pp.figure(2)
                pop.show_vectors(self.input[:,:,:,i-1])
                pp.xlabel('Pixel')
                pp.ylabel('Pixel')
                pp.suptitle('Model input population code')
                pp.figure(3)
                pop.show_vectors(X[:,:,:,i])
                pp.xlabel('Pixel')
                pp.ylabel('Pixel')
                pp.suptitle('Model output population code')

            else:
                pp.figure(2)
                pop.show_vectors(self.input[:,:,:,i])
                pp.xlabel('Pixel')
                pp.ylabel('Pixel')
                pp.suptitle('Model input population code')

            h_v_edges[i,:]= pop.show_vectors(X[:,:,:,i],all=False)
            pp.figure(4)
            pp.plot(i, h_v_edges[i,0],'ko', markerfacecolor='None')
            pp.plot(i, h_v_edges[i,1],'k*')
            print h_v_edges[i,0],h_v_edges[i,1]

            if i>0:
                self.cur_frame += self.delta_t

        x=ny.arange(-0.2,self.time_frames+1)
        y=0*x+45
        pp.plot(x,y)
        pp.xlim(-0.2,self.time_frames+0.2)
        pp.ylim(-1,91)
        pp.xlabel('Time steps (cycles through the model)')
        pp.ylabel('Direction (degree)')
        pp.suptitle('Integrated motion direction')

if __name__ == '__main__':

    M = Model('model.cfg', feedback=False) # feedback=True
    #M.show_mt_gauss()
    M.integrated_motion_direction()
    #M.run_model_full()
    pp.show()

