__author__ = 'ohaas'

#import numpy as ny
#import matplotlib.pyplot as pp
import stimulus

class Population(object):
    pass


#---- TO CREATE IMAGE STIMULUS (I) WITH IMAGE SIZE 30, STIMULUS SIZE 6 AND START POINT 2
#    (ALL NUMBERS ARE USED IN A SQUARED FASHION, E.G. IMAGE SIZE 30 MEANS: 30x30)-----------------
#

I = stimulus.image(30,6,2)

#---- TO SHOW THE STIMULUS IMAGE (I):-------------------------------------------------------------

stimulus.image.show_im(I)

#---- TO PRINT A PIXEL VALUE OF THE STIMULUS IMAGE (I) AT (X,Y)=(5,6)----------------------------

print stimulus.image.pix_value(I,5,6)


