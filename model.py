__author__ = 'ohaas'

import numpy as ny
#import matplotlib.pyplot as pp
import pop_code as pc
import neuron as n

class model(object):
    pass


    # initialize variables

    def __init__(self, main_size, square_size, start, gauss_width, time_frames, time_step_length):
        self.main_size=main_size
        self.square_size=square_size
        self.start=start
        self.gauss_width=gauss_width
        self.time_frames=time_frames
        self.delta_t=time_step_length


        # definition of initial population codes for different time steps

        self.pop_codes=ny.zeros((self.main_size,self.main_size,8,self.time_frames))
        s=self.start

        for i in ny.arange(0,self.time_frames):
            j=pc.Population(self.main_size, self.square_size, s, self.gauss_width)
            self.pop_codes[:,:,:,i]=pc.Population.print_pop(j)
            s=ny.add(s,self.delta_t)


        # definition of model storage variables

        FB=0
        v1_V1=ny.zeros((self.main_size,self.main_size,8,self.time_frames))
        v2_V1=ny.zeros((self.main_size,self.main_size,8,self.time_frames))
        v3_V1=ny.zeros((self.main_size,self.main_size,8,self.time_frames))
        v1_MT=ny.zeros((self.main_size,self.main_size,8,self.time_frames))
        v2_MT=ny.zeros((self.main_size,self.main_size,8,self.time_frames))
        v3_MT=ny.zeros((self.main_size,self.main_size,8,self.time_frames))
        dirac=n.N(0.0,0.0,1/(0*ny.sqrt(1/2*ny.pi)))
        sigma_075=n.N(0.0,0.75,1/(0.75*ny.sqrt(1/2*ny.pi)))
        G_dirac=(n.N.activity(dirac,0.0),n.N.activity(dirac,45.0),n.N.activity(dirac,90.0),n.N.activity(dirac,135.0),n.N.activity(dirac,180.0),n.N.activity(dirac,225.0),n.N.activity(dirac,270.0),n.N.activity(dirac,315.0))
        G_sigma_075=(n.N.activity(sigma_075,0.0),n.N.activity(sigma_075,45.0),n.N.activity(sigma_075,90.0),n.N.activity(sigma_075,135.0),n.N.activity(sigma_075,180.0),n.N.activity(sigma_075,225.0),n.N.activity(sigma_075,270.0),n.N.activity(sigma_075,315.0))




        # first model step in V1

        v1_V1[:,:,:,0]=pop_codes[:,:,:,0]*(1+100*FB)

        # second model step

        for x in ny.arange(0.0,30.0):
            for y in ny.arange(0.0,30.0):
                v2_V1[x,y,:,0]=(v1_V1[x,y,:,0]**2)*G_dirac*G_sigma_075 # **2 correct?



#model(30,6,2,30,10,2)