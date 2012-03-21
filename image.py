__author__ = 'ohaas'

import Image, ImageDraw
import matplotlib.pyplot as pp

class image(object):
      pass

      def __init__(self,main_size,square_size,start):
          i=Image.new("1",(main_size,main_size),1)
          draw = ImageDraw.Draw(i)
          draw.line(((start,start),(start+1+square_size, start),(start+1+square_size,start+1+square_size),(start, start+1+square_size),(start,start)), fill=0)
          pp.imshow(i, interpolation="nearest")
          pp.show()


image(30,6,6)