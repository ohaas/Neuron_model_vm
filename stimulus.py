__author__ = 'ohaas'

import numpy as ny
import matplotlib.pyplot as pp

class stimulus(object):
      pass


      def __init__(self,main):
          self.main=ny.ones((main, main, 3))

      def square(self, size, start):
          for s in ny.arange(start,start+1+size):
              self.main[start,s]=ny.zeros(3)
              self.main[s,start]=ny.zeros(3)
              self.main[start+size,s]=ny.zeros(3)
              self.main[s,start+size]=ny.zeros(3)
          return self.main

#stimulus(main size of stimulus picture), pic.square(size,starting point)
pic = stimulus(30)
pp.imshow(pic.square(4,6))
pp.show()
