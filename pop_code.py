__author__ = 'ohaas'

import numpy as ny
import matplotlib.pyplot as pp
import stimulus
import neuron
#import Image, ImageDraw

class Population(object):
    pass

    # main_size= IMAGE SIZE SQUARED (main_size x main_size), square_size=STIMULUS SIZE SQUARED,
    # start=STIMULUS STARTING POINT SQUARED (lower left stimulus corner), gauss_width= WIDTH OF NEURONAL GAUSS TUNING CURVE

    def __init__(self, main_size, square_size, start, gauss_width):
        self.main_size=main_size
        self.square_size=square_size
        self.start=start
        self.I=stimulus.image(main_size,square_size,start)

        #---- GET STIMULUS CORNERS, WITH ll=LOWER LEFT, lr=LOWER RIGHT, ur=UPPER RIGHT, ul=UPPER LEFT

        self.ll=stimulus.image.ll_corner(self.I)
        self.lr=stimulus.image.lr_corner(self.I)
        self.ur=stimulus.image.ur_corner(self.I)
        self.ul=stimulus.image.ul_corner(self.I)
        self.width=gauss_width

        # NEURONAL RESPONSES FOR NEURONS neuron.N(maximum_location_in_degrees, activation_width, Amplitude)

        Neuron0=neuron.N(0.0,self.width, 1)
        Neuron1=neuron.N(45.0,self.width, 1)
        Neuron2=neuron.N(90.0,self.width, 1)
        Neuron3=neuron.N(135.0,self.width, 1)
        Neuron4=neuron.N(180.0,self.width, 1)
        Neuron5=neuron.N(225.0,self.width, 1)
        Neuron6=neuron.N(270.0,self.width, 1)
        Neuron7=neuron.N(315.0,self.width, 1)

        # NEURONAL ACTIVITY AT POINT X IN DEGREES E.G.: neuron.N.activity(Neuron1,X)

        self.pop=ny.zeros((main_size, main_size, 8))
        pop_no=ny.zeros(8)
        pop_corner=(neuron.N.activity(Neuron0,45.0), neuron.N.activity(Neuron1,45.0), neuron.N.activity(Neuron2,45.0), neuron.N.activity(Neuron3,45.0), neuron.N.activity(Neuron4,45.0), neuron.N.activity(Neuron5,45.0), neuron.N.activity(Neuron6,45.0), neuron.N.activity(Neuron7,45.0))
        pop_vertical=(neuron.N.activity(Neuron0,90.0), neuron.N.activity(Neuron1,90.0), neuron.N.activity(Neuron2,90.0), neuron.N.activity(Neuron3,90.0), neuron.N.activity(Neuron4,90.0), neuron.N.activity(Neuron5,90.0), neuron.N.activity(Neuron6,90.0), neuron.N.activity(Neuron7,90.0))
        pop_horizontal=(neuron.N.activity(Neuron0,0.0), neuron.N.activity(Neuron1,0.0), neuron.N.activity(Neuron2,0.0), neuron.N.activity(Neuron3,0.0), neuron.N.activity(Neuron4,0.0), neuron.N.activity(Neuron5,0.0), neuron.N.activity(Neuron6,0.0), neuron.N.activity(Neuron7,0.0))

        # ASSIGNS A POPULATION CODE FOR EACH PIXEL IN THE IMAGE I:

        for x in ny.arange(0.0,main_size):
            for y in ny.arange(0.0,main_size):
                p=stimulus.image.pix_value(self.I,x,y)
                if p==1:
                    self.pop[x,y]=pop_no
                elif (x,y)==self.ll or (x,y)==self.lr or (x,y)==self.ur or (x,y)==self.ul: #corners
                    self.pop[x,y]=pop_corner
                elif (x,y)==(x,start) or (x,y)==(x,start+square_size+1): #horizontal line
                    self.pop[x,y]=pop_horizontal
                else:
                    self.pop[x,y]=pop_vertical

    #---- TO SHOW THE STIMULUS IMAGE (I):-------------------------------------------------------------

    def show_stimulus(self):
        return stimulus.image.show_im(self.I)


    # ASSIGN EVERY PIXEL IN THE IMAGE I A CORRESPONDING VECTOR BASED ON ITS POPULATION CODE

    def show_vectors(self):
        vec=ny.matrix(((0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1)))
        for x in ny.arange(0.0,self.main_size):
            for y in ny.arange(0.0,self.main_size):
                p=stimulus.image.pix_value(self.I,x,y)
                if p!=1 and x%2==0 and (x,y)==(x,self.start) or p!=1 and x%2==0 and (x,y)==(x,self.start+self.square_size+1) or p!=1 and y%2==0 and (x,y)==(self.start,y) or p!=1 and y%2==0 and (x,y)==(self.start+self.square_size+1,y) or (x,y)==self.ll or (x,y)==self.lr or (x,y)==self.ur or (x,y)==self.ul:
                    multiple=ny.multiply(self.pop[x,y,:],ny.transpose(vec))
                    x1=ny.sum(multiple[0,:])
                    y1=ny.sum(multiple[1,:])
                    stimulus.image.daw__line_to_image(self.I,x,y,10*x1,10*y1)
                else:
                    pass

        stimulus.image.show_im(self.I)




    # PLOT POPULATION CODE FOR ALL PIXELS:

    def plot_pop(self):
        for a in ny.arange(0,self.main_size):
            for b in ny.arange(0,self.main_size):
                pp.plot(self.pop[a,b,:])
        pp.xlabel('Neuron number')
        pp.ylabel('Neuronal activation')
        pp.show()

    # PRINT POPULATION CODE AT PIXEL-POINT X,Y: pop[X,Y,:]

    def print_pop_xy(self, x, y):
        print self.pop[x,y,:]

    # RETURN POPULATION CODE

    def print_pop(self):
         return self.pop[:,:,:]











