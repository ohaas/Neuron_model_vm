__author__ = 'ohaas'

import numpy as ny
import matplotlib.pyplot as pp
import pop_code as pc
from matplotlib.mlab import bivariate_normal
from scipy.signal import convolve2d
import ConfigParser as cp
import neuron
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import math

def get_gauss_kernel(sigma, size, res):
    """
    return a two dimesional gausian kernel of shape (size*(1/resolution),size*(1/resolution))
    with a std deviation of std
    """
    x,y = ny.mgrid[-size/2:size/2:res,-size/2:size/2:res]
    b=bivariate_normal(x,y,sigma,sigma)
    A=(1/ny.max(b))
    #A=1
    return x,y,A*bivariate_normal(x, y, sigma, sigma)

def gauss(sigma=0.75, x=ny.arange( 0.0, 8.0, 1), mu=0):
    return ny.exp(-(x-mu)**2/(2.0*sigma**2))
g=gauss()+gauss(mu=8)

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

         s=v2_t.shape
         r=ny.reshape(v2_t,(s[0]*s[1],s[2]))
         m=ny.mean(r,axis=0)
         c=ny.array((0.47730912256773905, 1.0, 0.47730912256773905, 0.051903774289058222, 0.0012858809606739489, 1.4515291236951916e-05, 0.0012858809606739489, 0.051903774289058222))
         M=ny.zeros_like(v2_t)
         n=0
         for x in ny.arange(0.0,s[0]):
             for y in ny.arange(0.0,s[0]):
                 if not ny.any(v2_t[x,y,:])==0:
                     M[x,y,:]=m #mean velocity is largest at 45degree (estimation of model stage)
#                     n+=1

#         M1=M*(s[0])/(2*n) # mean taken over only not zero places

         v3_t=ny.divide(v2_t*c,0.01+ny.max(v2_t)) #since we assume we know the moving direction, we emphasize signals in the right direction
         # and weaken signals in the wrong direction. This is done in a gaussian fashion by c. If we wouldnt know the correct motion direction
         # we would have to scann the code for excitation of different velocities and therefore find step by step the correct one (less rapid converging to 45degree)

         #v3_t=ny.divide(v2_t-(v2_t*M1),0.01+(v2_t*M1))
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
        self.mt_kernel_sigma =  cfg.getfloat('MT', 'kernel_sigma')
        self.mt_kernel_size =  cfg.getfloat('MT', 'kernel_size')
        self.mt_kernel_res =  cfg.getfloat('MT', 'kernel_res')

        self.x,self.y,self.mt_gauss = get_gauss_kernel(self.mt_kernel_sigma, self.mt_kernel_size, self.mt_kernel_res)

        self.V1 = Stage([], v1_C)
        self.MT = Stage(self.mt_gauss, 0)


    def create_input(self):
        """
        definition of initial population codes for different time steps (is always the same one!!!)
        """
        I = ny.zeros((self.main_size, self.main_size, 8, self.time_frames))
        cur_frame = self.start
        for i in ny.arange(0, self.time_frames):
            j = pc.Population(self.main_size, self.square_size, cur_frame, self.gauss_width)
            I[:,:,:,i] = j.initial_pop_code()
            cur_frame += self.delta_t
            #j.show_vectors(I[:,:,:,i])

        return I


    def run_model_full(self):
        self.input = self.create_input()

        X = ny.zeros((self.main_size, self.main_size, 8, self.time_frames+1))
        FB=ny.zeros((self.main_size, self.main_size, 8, self.time_frames+1))
        X[:,:,:, 0] = self.input[:,:,:,0]


        for d_t in ny.arange(1, self.time_frames+1):

            inp = self.input[:,:,:,d_t-1]
            v1 = self.V1.do_all(inp, FB[:,:,:,d_t-1])
            mt = self.MT.do_all(v1, 0)
            X[:,:,:, d_t] = mt


            if self.do_feedback:
                pop = pc.Population(self.main_size, self.square_size, self.start, self.gauss_width)
                FB[:,:,:,d_t] = pop.move_pop(mt, self.delta_t)


        return X,FB


    def integrated_motion_direction(self):

        #fig = pp.figure()
        h_v_edges = ny.zeros((self.time_frames+1,2))
        self.cur_frame = self.start
        X,FB = self.run_model_full ()

        for i in ny.arange(0,self.time_frames+1):



            pop = pc.Population(self.main_size, self.square_size, self.cur_frame, self.gauss_width)

            if i>0:
                stimulus=ny.zeros_like(self.input[:,:,:,i-1])
                pp.figure(3)
                pop.show_vectors(stimulus)
                pp.xlabel('Pixel')
                pp.ylabel('Pixel')
                pp.title('Stimulus with picture size %.2f,\n square size %.2f and time step size %s t=%.2f in pixel.'\
                % (self.main_size, self.square_size, u'\u0394', self.delta_t) )

                pp.figure(4)
                pop.show_vectors(self.input[:,:,:,i-1])
                pp.xlabel('Pixel')
                pp.ylabel('Pixel')
                pp.title('Model input population code for spatial kernel values:\n %s=%.2f, size=%.2f, res=%.2f and neuron kernel %s=%.2f'\
                %  (u"\u03C3",self.mt_kernel_sigma, self.mt_kernel_size, self.mt_kernel_res,u"\u03C3", self.gauss_width))
                pp.figure(5)
                pop.show_vectors(X[:,:,:,i])
                pp.xlabel('Pixel')
                pp.ylabel('Pixel')
                pp.title('Model output population code for spatial kernel values:\n %s=%.2f, size=%.2f, res=%.2f and neuron kernel %s=%.2f'\
                % (u"\u03C3",self.mt_kernel_sigma, self.mt_kernel_size, self.mt_kernel_res,u"\u03C3", self.gauss_width) )
                pp.figure(6)
                pop.show_vectors(FB[:,:,:,i-1])
                pp.xlabel('Pixel')
                pp.ylabel('Pixel')
                pp.title('Model feedback population code for spatial kernel values:\n %s=%.2f, size=%.2f, res=%.2f and neuron kernel %s=%.2f'\
                %  (u"\u03C3",self.mt_kernel_sigma, self.mt_kernel_size, self.mt_kernel_res,u"\u03C3", self.gauss_width))
                pop.I.pic()

                pp.figure(7)
                pop.plot_pop(X[:,:,:,i],self.time_frames,i)

                self.cur_frame += self.delta_t
            else:
                pp.figure(7)
                pop.plot_pop(X[:,:,:,i],self.time_frames,i)
                pp.figure(4)
                pop.show_vectors(self.input[:,:,:,i])
                pp.xlabel('Pixel')
                pp.ylabel('Pixel')
                pp.title('Model input population code for spatial kernel values:\n %s=%.2f, size=%.2f, res=%.2f and neuron kernel %s=%.2f'\
                % (u"\u03C3",self.mt_kernel_sigma, self.mt_kernel_size, self.mt_kernel_res,u"\u03C3", self.gauss_width) )

            h_v_edges[i,:]= pop.show_vectors(X[:,:,:,i],all=False)
            pp.figure(8)
            pp.plot(i, h_v_edges[i,0],'ko', markerfacecolor='None')
            pp.plot(i, h_v_edges[i,1],'k*')
            ax = pp.subplot(111)
            if i==self.time_frames:
                ax.plot(i, h_v_edges[i,0],'ko', markerfacecolor='None', label='Measured at midpoint of horizontal edges')
                ax.plot(i, h_v_edges[i,1],'k*', label='Measured at midpoint of vertical edges')
                x=ny.arange(-0.2,self.time_frames+1)
                y=0*x+45
                ax.plot(x,y, label='True motion direction')
                # Shink current axis's height by 10% on the bottom
                box = ax.get_position()
                ax.set_position([box.x0, box.y0 + box.height * 0.2, box.width, box.height * 0.8])
            # Put a legend below current axis
            ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.13), fancybox=True, shadow=True, ncol=1)
            print i, h_v_edges[i,0],h_v_edges[i,1]



        pp.xlim(-0.2,self.time_frames+0.2)
        pp.ylim(-1,91)
        pp.xlabel('Time steps (cycles through the model)')
        pp.ylabel('Direction (degree)')
        pp.suptitle('Integrated motion direction for spatial kernel %s=%.2f, size=%.2f, res=%.2f, neuron kernel:\n %s=%.2f & stimulus values in pixel: size=%ix%i, square=%ix%i, velocity=%i'
        % (u"\u03C3", self.mt_kernel_sigma, self.mt_kernel_size, self.mt_kernel_res, u"\u03C3", self.gauss_width, self.main_size, self.main_size, self.square_size, self.square_size, ny.sqrt(2*(self.delta_t**2))) )

        pp.figure(1)
        Neuron=neuron.N(self.gauss_width)
        Neuron.plot_act()


        fig=pp.figure(2)
        ax = fig.gca(projection='3d')
        surf=ax.plot_surface(self.x,self.y,self.mt_gauss, rstride=1, cstride=1, cmap=cm.jet, linewidth=0, antialiased=False)
        pp.xlabel('Pixel')
        pp.ylabel('Pixel')
        pp.title('Spatial Kernel with %s=%.2f, size=%.2f, res=%.2f' % (u"\u03C3",self.mt_kernel_sigma, self.mt_kernel_size, self.mt_kernel_res))
        ax.set_zlim(ny.min(self.mt_gauss), ny.max(self.mt_gauss))
        ax.zaxis.set_major_locator(LinearLocator(10))
        ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

        pp.colorbar(surf, shrink=0.5, aspect=5)

if __name__ == '__main__':

    M = Model('model.cfg') # feedback=True
    #M.show_mt_gauss()
    M.integrated_motion_direction()

    #M.run_model_full()
    pp.show()

