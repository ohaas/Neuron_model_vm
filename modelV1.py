__author__ = 'ohaas'

import numpy as ny
import matplotlib.pyplot as pp
import pop_code as pc

class model(object):
    pass

# pc.Popultaion(main_size, square_size, start, gauss_width)

a=pc.Population(30,6,2,30)
pc.Population.show_vectors(a)