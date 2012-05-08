__author__ = 'ohaas'

import numpy as ny
import matplotlib.pyplot as pp
from matplotlib.patches import FancyArrowPatch as fap
import stimulus
import neuron
import math


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
        neurons = [neuron.N(self.width).neuron_gauss(degree) for degree in angle]

        #2) NEURONAL ACTIVITY AT POINT X IN DEGREES E.G.: Neuron1.neuron_gauss(X)
        self.pop=ny.zeros((self.main_size, self.main_size, 8))
        self.pop_no=ny.zeros(8)
        self.pop_corner=[(neurons[i])[45.0] for i in ny.arange(0,len(angle))]
        self.pop_vertical=[(neurons[i])[90.0] for i in ny.arange(0,len(angle))]
        self.pop_horizontal=[(neurons[i])[0.0] for i in ny.arange(0,len(angle))]
        self.h=ny.arange(self.start+2,self.start+self.square_size-1)
        self.p=(self.start+self.square_size-1,self.start+self.square_size)
        self.q=(self.start,self.start+1)
        self.r=(self.start,self.start+self.square_size)
        self.s=(self.start+1, self.start+self.square_size-1)



    def initial_pop_code(self):
        pop1=ny.zeros((self.main_size, self.main_size, 8))

        for x in ny.arange(0.0, self.main_size):
            for y in ny.arange(0.0, self.main_size):
                if x in self.q and y in self.r or x in self.p and y in self.r or x in self.r and y in self.s:
                    pop1[x,y,:]=self.pop_corner
                elif x in self.h and y in self.r: #horizontal line
                    pop1[x,y,:]=self.pop_horizontal
                elif y in self.h and x in self.r:
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
                #if not ny.any(population_code[x,y,:])==0:
                if x in ny.arange(self.start, self.start+self.square_size+1) and y in self.r \
                or x in self.r and y in ny.arange(self.start, self.start+self.square_size+1):

                   multiple=ny.multiply(population_code[x,y,:],ny.transpose(self.vec))
                   x1=ny.sum(multiple[0,:])
                   y1=ny.sum(multiple[1,:])

                   if self.all:
                       #Q=pp.quiver(x,y,x1,y1, headwidth=2, headlength=3, linewidth=0.001)

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


    def move_pop(self, population_code, delta_t):

        population_code_new=ny.zeros_like(population_code)

#        A=ny.zeros((self.main_size,self.main_size,1))
#        B=ny.zeros((self.main_size,self.main_size,1))
#        i=0
        for x in ny.arange(0.0,self.main_size):
            for y in ny.arange(0.0,self.main_size):
                if not ny.any(population_code[x,y,:])==0 and ((x+delta_t)<self.main_size,(y+delta_t)<self.main_size)==(True, True):
                    population_code_new[x+delta_t,y+delta_t,:]=population_code[x,y,:]

        return population_code_new
#                weight=ny.multiply(population_code[x,y,:],delta_t)
#                if (x,y)==(self.start,self.start):
#                    print population_code[x,y,:],x,y
#                multiple=ny.multiply(population_code[x,y,:],ny.transpose(self.vec))
#                a=ny.sum(multiple[0,:])
#                b=ny.sum(multiple[1,:])
#                #if not ny.any(population_code[x,y,:])==0 and ((x+(a*delta_t))<=self.main_size,(y+(b*delta_t))<=self.main_size)==(True, True):
#                #    population_code_new[x+(a*delta_t),y+(b*delta_t),:]=population_code[x,y,:]
#                A[x,y,:]=a
#                B[x,y,:]=b
#                if a and b !=0:
#                    i+=1
#
#        a1=ny.sum(A)*delta_t/i
#        b1=ny.sum(B)*delta_t/i
#
#        print a1,b1
#        for x in ny.arange(0.0,self.main_size):
#            for y in ny.arange(0.0,self.main_size):






    def plot_pop(self, population_code, time_frames, i):
        """
        PLOT POPULATION CODE FOR ALL PIXELS:
        """
        for x in ny.arange(0.0,self.main_size):
            for y in ny.arange(0.0,self.main_size):
                if not ny.any(population_code[x,y,:])==0:


                    multiple=ny.multiply(population_code[x,y,:],ny.transpose(self.vec))
                    x1=ny.sum(multiple[0,:])
                    y1=ny.sum(multiple[1,:])
                    # connect (0,0) with (x,y):
                    r=ny.sqrt((x1**2)+(y1**2))
                    angle=(ny.arcsin(y1/r))
                    y2=ny.arange(0,1.01,0.01)
                    x2=angle+(0.0*y2)
                    ax=pp.subplot(math.ceil(time_frames/3.0),3,i+1, polar=True)
                    ax.plot(x2,y2)
                    pp.title('After %d Model Cycles' %i)
       # pp.polar(x1,y1)
       # pp.xlabel('Neuron number')
       # pp.ylabel('Neuronal activation')
       # pp.suptitle('Population code after %d model cycles' %t)




if __name__ == '__main__':
    p = Population(30, 6, 2, 30)
    p.plot_pop(p.initial_pop_code(), 0)
    pp.show()





