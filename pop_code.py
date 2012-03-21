__author__ = 'ohaas'

import numpy as ny
#import matplotlib.pyplot as pp
import stimulus

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


pop=ny.zeros((main_size, main_size, 8))
pop_no=ny.zeros(8)

pop_corner=(0,1,2,3,2,1,0,0)
pop_horizontal=(3,2,1,0,0,0,1,2)
pop_vertical=(0,0,0,1,2,3,2,1)

for x in ny.arange(0,main_size):
    for y in ny.arange(0,main_size):
        p=stimulus.image.pix_value(I,x,y)
        if p==1:
            pop[x,y]=pop_no
        elif (x,y)==ll or (x,y)==lr or (x,y)==ur or (x,y)==ul: #corners
            pop[x,y]=pop_corner
        elif (x,y)==(x,start) or (x,y)==(x,start+square_size): #horizontal line
            pop[x,y]=pop_horizontal
        else:
            pop[x,y]=pop_vertical




