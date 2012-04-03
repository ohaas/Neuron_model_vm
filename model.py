__author__ = 'ohaas'

import numpy as ny
import matplotlib.pyplot as pp
import pop_code as pc
import neuron
from matplotlib.mlab import bivariate_normal
from scipy.signal import convolve2d


class Stage(object):
    def __init__(self, Gx, C):
        self.Gx = Gx
        self.C = C

    def do_v1(self, net_in, net_fb):
        v1_t= net_in + (self.C * net_fb * net_in)
        return v1_t

    def do_v2(self, v1_t):

        if not self.Gx:
            return v1_t**2

        v2_t = v1_t
        for n in ny.arange(0,8):
            v2_t[:,:,n] = convolve2d (v2_t[:,:,n]**2, self.Gx, 'same')

        return v2_t

    def do_v3(self, v2_t):
        v3_t = (v2_t - (0.5*v2_t))/(0.01+v2_t)
        return v3_t

    def do_all_(self, net_in, net_fb):
        v1_t = self.do_v1(net_in, net_fb)
        v2_t = self.do_v2(v1_t)
        v3_t = self.do_v3(v2_t)
        return v3_t


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

        self.size=10
        self.sigma=sigma
        self.res=1
        x,y = ny.mgrid[-self.size/2:self.size/2:self.res,-self.size/2:self.size/2:self.res]
        return bivariate_normal(x,y,sigma,sigma)

    def do_v1(self, net_in, net_fb, C):
        self.v1_t= net_in + (C * net_fb * net_in)
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
        definition of initial population codes for different time steps (is always the same one!!!)
        """
        self.pop_code=ny.zeros((self.main_size,self.main_size,8,self.time_frames/self.delta_t))
        self.s=self.start-self.delta_t
        for i in ny.arange(0,self.time_frames/self.delta_t):
            j=pc.Population(self.main_size, self.square_size, self.s+self.delta_t, self.gauss_width)
            #j.show_stimulus()
            self.pop_code[:,:,:,i]=j.print_pop(j.initial_pop_code())
            self.start=ny.add(self.start,self.delta_t)
        return self.pop_code[:,:,:,t]

    def run_model(self, t):
        are=Area(self.main_size, self.square_size, self.start, self.gauss_width, self.time_frames, self.delta_t)
        FB=0

        if t==0:
            p=pc.Population(self.main_size, self.square_size, self.start, self.gauss_width)
            #p.plot_pop(p.initial_pop_code(),t)
            #p.create_vectors(p.initial_pop_code())
            return p.initial_pop_code()
        else:
            for d_t in ny.arange(0,t):
                V1=are.do_all_(are.input(d_t),FB,100,0)
                self.MT=are.do_all_(V1,0,0,are.get_gauss_kernel(7))
                FB=self.MT
                print d_t
            #p=pc.Population(self.main_size, self.square_size, self.start, self.gauss_width)
            #p.plot_pop(FB,t)
            #p.create_vectors(FB)
            return self.MT

    def run_model_full(self, t):
        are=Area(self.main_size, self.square_size, self.start, self.gauss_width, self.time_frames, self.delta_t)
        FB=0
        p=pc.Population(self.main_size, self.square_size, self.start, self.gauss_width)


        X = ny.zeros((self.main_size, self.main_size, 8, t))
        X[:,:,:, 0] = p.initial_pop_code()

        for d_t in ny.arange(1, t):
            V1=are.do_all_(are.input(d_t), FB, 100, 0)
            self.MT=are.do_all_(V1, 0, 0, are.get_gauss_kernel(7))
            FB=self.MT
            X[:,:,:, d_t] = FB

        return X

    def integrated_motion_direction(self):
        are=Area(self.main_size, self.square_size, self.start, self.gauss_width, self.time_frames, self.delta_t)
        self.st=self.start-self.delta_t
        self.h_v_edges=ny.zeros((self.time_frames/self.delta_t,2))

        X = self.run_model_full(self.time_frames/self.delta_t)
        print X.shape

        for i in ny.arange(0,self.time_frames/self.delta_t):
            j=pc.Population(self.main_size, self.square_size, self.st+self.delta_t, self.gauss_width)
            pop_c = X[:,:,:,i]
            self.h_v_edges[i,:]=j.create_vectors(pop_c)
            pp.plot(i,self.h_v_edges[i,0],'+')
            pp.plot(i,self.h_v_edges[i,1],'*')
            print self.h_v_edges[i,0]

#        for i in ny.arange(0,self.time_frames/self.delta_t):
#            j=pc.Population(self.main_size, self.square_size, self.st+self.delta_t, self.gauss_width)
#            M=are.run_model(i)
#            self.h_v_edges[i,:]=j.create_vectors(M)
#            pp.plot(i,self.h_v_edges[i,0],'+')
#            pp.plot(i,self.h_v_edges[i,1],'*')

        x=ny.arange(0,self.time_frames/self.delta_t)
        y=0*x+45
        pp.plot(x,y)
        pp.xlim(-0.2,4.2)
        pp.ylim(-1,91)







if __name__ == '__main__':


    M=Area(30,6,2,30,10,1)
    M.integrated_motion_direction()
    #p=pc.Population(30,6,2,30)
    #M.input(1)
    pp.show()

