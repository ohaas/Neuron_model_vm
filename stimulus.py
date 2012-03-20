__author__ = 'ohaas'

import numpy as ny
import matplotlib.pyplot as pp

class stimulus(object):
      pass


      def __init__(self,main):
          self.main=ny.ones((main, main, 3))

      def square(self, size):
          for s in ny.arange(2,2+size):
              self.main[2,s]=ny.zeros(3)
              self.main[s,2]=ny.zeros(3)
              self.main[2+size,s]=ny.zeros(3)
              self.main[s,2+size]=ny.zeros(3)
          return self.main

#stimulus(main), pic.square(size)
pic = stimulus(30)
pp.imshow(pic.square(4))
pp.show()
