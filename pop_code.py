__author__ = 'ohaas'

import numpy as ny
import matplotlib.pyplot as pp
from matplotlib.patches import FancyArrowPatch as fap
import stimulus
import neuron


class Population(object):


    def __init__(self, main_size, square_size, start, gauss_width):
        """
        main_size= IMAGE SIZE SQUARED (main_size x main_size), square_size=STIMULUS SIZE SQUARED,
        start=STIMULUS STARTING POINT SQUARED (lower left stimulus corner), gauss_width= WIDTH OF NEURONAL GAUSS TUNING CURVE
        """
        self.main_size = main_size
        self.square_size = square_size
        self.start = start
        self.I = stimulus.image(main_size,square_size,start)
        self.width=gauss_width

        self.vec = ny.matrix(((0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1)))

        #1) NEURONAL RESPONSES FOR NEURONS neuron.N(maximum_location_in_degrees, activation_width, Amplitude=1):
        angle = ny.arange(0.0, 360, 45.0)
        neurons = [neuron.N(degree, self.width) for degree in angle]

        #2) NEURONAL ACTIVITY AT POINT X IN DEGREES E.G.: neuron.N.activity(Neuron1,X)
        self.pop=ny.zeros((self.main_size, self.main_size, 8))

        self.pop_no=ny.zeros(8)
        self.pop_corner=[n.activity(45.0) for n in neurons]
        self.pop_vertical=[n.activity(90.0) for n in neurons]
        self.pop_horizontal=[n.activity(0.0) for n in neurons]
        self.h=ny.arange(self.start+1,self.start+self.square_size+1)


    def initial_pop_code(self):
        pop1=ny.zeros((self.main_size, self.main_size, 8))

        for x in ny.arange(0.0, self.main_size):
            for y in ny.arange(0.0, self.main_size):
                if (x,y)==(self.start,self.start) or (x,y)==(self.start,self.start+self.square_size) or (x,y)==(self.start+self.square_size,self.start) or (x,y)==(self.start+self.square_size,self.start+self.square_size):
                    pop1[x,y,:]=self.pop_corner
                elif x in self.h and y==self.start or x in self.h and y==self.start+self.square_size: #horizontal line
                    pop1[x,y,:]=self.pop_horizontal
                elif y in self.h and x==self.start or y in self.h and x==self.start+self.square_size:
                    pop1[x,y,:]=self.pop_vertical
                else:
                    pop1[x,y,:]=self.pop_no

        if self.start + self.square_size + 1 > self.main_size:
            print 'WARNING: Stimulus out of picture'

        return pop1


    def show_vectors(self, population_code, all=True):
        self.all=all
        h_v_edges = ny.zeros(2)
        for x in ny.arange(0.0,self.main_size):
            for y in ny.arange(0.0,self.main_size):
                if (x,y)==(self.start,self.start) or (x,y)==(self.start,self.start+self.square_size) or (x,y)==(self.start+self.square_size,self.start) \
                   or (x,y)==(self.start+self.square_size,self.start+self.square_size) \
                   or x in self.h and y==self.start or x in self.h and y==self.start+self.square_size \
                   or y in self.h and x==self.start or y in self.h and x==self.start+self.square_size:

                   multiple=ny.multiply(population_code[x,y,:],ny.transpose(self.vec))
                   x1=ny.sum(multiple[0,:])
                   y1=ny.sum(multiple[1,:])

                   if self.all:
                       ax=pp.gca()
                       pp.axis([0,self.main_size,0, self.main_size])
                       ax.add_patch(fap((x,y),((x+(self.square_size/4)*x1/ny.sqrt(x1**2+y1**2)),((y+(self.square_size/4)*y1/ny.sqrt(x1**2+y1**2)))), arrowstyle='->',linewidth=0.5,mutation_scale=10))
                       self.I.pic() # shows the stimulus


                   else:
                       r=ny.sqrt((x1**2)+(y1**2))
                       x3=ny.arcsin(y1/r)
                       if (x,y)==(self.start + self.square_size, self.start + (self.square_size/2)):
                           h_v_edges[0]=x3*180/ny.pi
                       elif (x,y)==(self.start + (self.square_size/2), self.start + self.square_size):
                           h_v_edges[1]=x3*180/ny.pi
        return h_v_edges




    def plot_pop(self, population_code,t):
        """
        PLOT POPULATION CODE FOR ALL PIXELS:
        """
        for a in ny.arange(0,self.main_size):
            for b in ny.arange(0,self.main_size):
                pp.plot(population_code[a,b,:])
        pp.xlabel('Neuron number')
        pp.ylabel('Neuronal activation')
        pp.suptitle('Population code after %d model cycles' %t)
        pp.show()



if __name__ == '__main__':
    p = Population(30, 6, 2, 30)
    pop=p.initial_pop_code()
    pop.show_vectors()
    pp.show()





