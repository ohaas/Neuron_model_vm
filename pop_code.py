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

print stimulus.image.pix_value(I,6,6)

ll=stimulus.image.ll_corner(I)
lr=stimulus.image.lr_corner(I)
ur=stimulus.image.ur_corner(I)
ul=stimulus.image.ul_corner(I)
print ll, lr, ur, ul

pop=ny.ones((main_size, main_size, 8))


