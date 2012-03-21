__author__ = 'ohaas'

import Image, ImageDraw
import matplotlib.pyplot as pp

class image(object):
      pass

      def __init__(self,main_size,square_size,start):
          self.i=Image.new("1",(main_size,main_size),1)
          draw = ImageDraw.Draw(self.i)
          draw.line(((start,start),(start+1+square_size, start),(start+1+square_size,start+1+square_size),(start, start+1+square_size),(start,start)), fill=0)
          pp.imshow(self.i, interpolation="nearest")

      def pix_value(self,x,y):
          return self.i.getpixel((x,y))

      def show_im(self):
          pp.imshow(self.i,interpolation="nearest")
          pp.show()

