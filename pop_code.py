__author__ = 'ohaas'

import numpy as ny
#import matplotlib.pyplot as pp
import stimulus
import neuron

class Population(object):
    pass


#---- TO CREATE IMAGE STIMULUS (I) WITH IMAGE SIZE 30, STIMULUS SIZE 6 AND START POINT 2
#    (ALL NUMBERS ARE USED IN A SQUARED FASHION, E.G. IMAGE SIZE 30 MEANS: 30x30)-----------------
#
main_size=30
square_size=6
start=2
I = stimulus.image(main_size,square_size,start)

#---- TO SHOW THE STIMULUS IMAGE (I):-------------------------------------------------------------

#stimulus.image.show_im(I)

#---- TO PRINT A PIXEL VALUE OF THE STIMULUS IMAGE (I) AT (X,Y)=(5,6); 1=white; 0=black------------

#print stimulus.image.pix_value(I,6,6)

#---- GET STIMULUS CORNERS, WITH ll=LOWER LEFT, lr=LOWER RIGHT, ur=UPPER RIGHT, ul=UPPER LEFT
ll=stimulus.image.ll_corner(I)
lr=stimulus.image.lr_corner(I)
ur=stimulus.image.ur_corner(I)
ul=stimulus.image.ul_corner(I)


# NEURONAL RESPONSES FOR NEURONS neuron.N(maximum_location_in_degrees, activation_width, read_out_point_in_degrees, Amplitude)
Neuron1=neuron.N(0.0,10.0, 1)
Neuron2=neuron.N(45.0,10.0, 1)
Neuron3=neuron.N(90.0,10.0, 1)
Neuron4=neuron.N(135.0,10.0, 1)
Neuron5=neuron.N(180.0,10.0, 1)
Neuron6=neuron.N(225.0,10.0, 1)
Neuron7=neuron.N(270.0,10.0, 1)
Neuron8=neuron.N(315.0,10.0, 1)

# NEURONAL ACTIVITY AT POINT X IN DEGREES E.G.: neuron.N.activity(Neuron1,X)

pop=ny.zeros((main_size, main_size, 8))
pop_no=ny.zeros(8)
pop_corner=(neuron.N.activity(Neuron1,315.0), neuron.N.activity(Neuron2,315.0), neuron.N.activity(Neuron3,315.0), neuron.N.activity(Neuron4,315.0), neuron.N.activity(Neuron5,315.0), neuron.N.activity(Neuron6,315.0), neuron.N.activity(Neuron7,315.0), neuron.N.activity(Neuron8,315.0))
pop_horizontal=(neuron.N.activity(Neuron1,270.0), neuron.N.activity(Neuron2,270.0), neuron.N.activity(Neuron3,270.0), neuron.N.activity(Neuron4,270.0), neuron.N.activity(Neuron5,270.0), neuron.N.activity(Neuron6,270.0), neuron.N.activity(Neuron7,270.0), neuron.N.activity(Neuron8,270.0))
pop_vertical=(neuron.N.activity(Neuron1,0.0), neuron.N.activity(Neuron2,0.0), neuron.N.activity(Neuron3,0.0), neuron.N.activity(Neuron4,0.0), neuron.N.activity(Neuron5,0.0), neuron.N.activity(Neuron6,0.0), neuron.N.activity(Neuron7,0.0), neuron.N.activity(Neuron8,0.0))
print pop_vertical, pop_horizontal, pop_corner

# ASSIGNS A POPULATION CODE FOR EACH PIXEL IN THE IMAGE I:

for x in ny.arange(0.0,main_size):
    for y in ny.arange(0.0,main_size):
        p=stimulus.image.pix_value(I,x,y)
        if p==1:
            pop[x,y]=pop_no
        elif (x,y)==ll or (x,y)==lr or (x,y)==ur or (x,y)==ul: #corners
            pop[x,y]=pop_corner
        elif (x,y)==(x,start) or (x,y)==(x,start+square_size): #horizontal line
            pop[x,y]=pop_horizontal
        else:
            pop[x,y]=pop_vertical

#print pop[2,8,:]


