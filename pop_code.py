__author__ = 'ohaas'

import numpy as ny
import matplotlib.pyplot as pp
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


    def initial_pop_code(self):
        """
        ASSIGNS A POPULATION CODE FOR EACH PIXEL IN THE IMAGE I
        """

        #1) NEURONAL RESPONSES FOR NEURONS neuron.N(maximum_location_in_degrees, activation_width, Amplitude=1)


        angle = ny.arange(0.0, 360, 45.0)
        neurons = [neuron.N(degree, self.width) for degree in angle]

        #2) NEURONAL ACTIVITY AT POINT X IN DEGREES E.G.: neuron.N.activity(Neuron1,X)

        self.pop=ny.zeros((self.main_size, self.main_size, 8))
        self.pop_no=ny.zeros(8)
        self.pop_corner=[n.activity(45.0) for n in neurons]
        self.pop_vertical=[n.activity(90.0) for n in neurons]
        self.pop_horizontal=[n.activity(0.0) for n in neurons]

        for x in ny.arange(0.0, self.main_size):
            for y in ny.arange(0.0, self.main_size):
                p=stimulus.image.pix_value(self.I,x,y)
                if p==1:
                    self.pop[x,y]=self.pop_no
                elif (x,y)==self.I.ll or (x,y)==self.I.lr or (x,y)==self.I.ur or (x,y)==self.I.ul: #corners
                    self.pop[x,y]=self.pop_corner
                elif (x,y)==(x,self.start) or (x,y)==(x,self.start+self.square_size+1): #horizontal line
                    self.pop[x,y]=self.pop_horizontal
                else:
                    self.pop[x,y]=self.pop_vertical
        return self.pop

    def show_stimulus(self):
        """
        TO SHOW THE STIMULUS IMAGE (I)
        """
        return self.I.show_im()


    def show_vectors(self, population_code):
        """
         ASSIGN EVERY PIXEL IN THE IMAGE I A CORRESPONDING VECTOR BASED ON ITS POPULATION CODE
        """
        vec=ny.matrix(((0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1)))
        for x in ny.arange(0.0,self.main_size):
            for y in ny.arange(0.0,self.main_size):
                p=stimulus.image.pix_value(self.I,x,y)
                if p!=1 and x%2==0 and (x,y)==(x,self.start) or p!=1 and x%2==0 and (x,y)==(x,self.start+self.square_size+1) or p!=1 and y%2==0 and (x,y)==(self.start,y) or p!=1 and y%2==0 and (x,y)==(self.start+self.square_size+1,y) or (x,y)==self.I.ll or (x,y)==self.I.lr or (x,y)==self.I.ur or (x,y)==self.I.ul:
                    multiple=ny.multiply(population_code[x,y,:],ny.transpose(vec))
                    x1=ny.sum(multiple[0,:])
                    y1=ny.sum(multiple[1,:])
                    stimulus.image.daw__line_to_image(self.I,x,y,10*x1,10*y1)

        self.I.show_im()

    def create_vectors(self, population_code):
        """
        CREATES IMAGE VECTORS IN CORRESPONDING 360 DEGREE PLOT AND RETURNS VECOTS IN THE MIDDLE OF THE HORIZONTAL AND VERTICAL EDGES
        """
        self.h_v_edges=ny.zeros(2)
        self.out=ny.zeros((self.main_size,self.main_size,2))
        vec=ny.matrix(((0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1)))
        for x in ny.arange(0.0,self.main_size):
            for y in ny.arange(0.0,self.main_size):
                p=stimulus.image.pix_value(self.I,x,y)
                if p!=1:
                    multiple=ny.multiply(population_code[x,y,:],ny.transpose(vec))
                    x1=ny.sum(multiple[0,:])
                    y1=ny.sum(multiple[1,:])
                    self.out[x,y,:]=(x1,y1)
                    r=ny.sqrt((x1**2)+(y1**2))
                    x3=ny.arcsin(y1/r)
                    y3=1
                    #pp.polar((x3,x3),(0,y3))
                    if (x,y)==(self.start+self.square_size+1,self.start+(self.square_size/2)):
                        self.h=x3
                        self.h_v_edges[0]=self.h*180/ny.pi
                    elif (x,y)==(self.start+(self.square_size/2),self.start+self.square_size+1):
                        self.v=x3
                        self.h_v_edges[1]=self.v*180/ny.pi
        return self.h_v_edges
        #pp.show()

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

    def print_pop_xy(self, population_code, x, y):
        """
        PRINT POPULATION CODE AT PIXEL-POINT X,Y: pop[X,Y,:]
        """
        print population_code[x,y,:]

    # RETURN POPULATION CODE

    def print_pop(self, population_code):
        return population_code[:,:,:]


if __name__ == '__main__':
    p = Population(30, 6, 2, 30)
    p.create_vectors(p.initial_pop_code())




