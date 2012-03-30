__author__ = 'ohaas'

import Image, ImageDraw
import matplotlib.pyplot as pp

class image(object):

      def __init__(self,main_size,square_size,start):
          self.i=Image.new("1",(main_size,main_size),1)
          draw = ImageDraw.Draw(self.i)
          self.ll=(start,start)
          self.ul=(start, start+1+square_size)
          self.lr=(start+1+square_size, start)
          self.ur=(start+1+square_size,start+1+square_size)
          draw.line((self.ll,self.lr,self.ur,self.ul,self.ll), fill=0)
          #pp.imshow(self.i, interpolation="nearest")

      def pix_value(self,x,y):
          return self.i.getpixel((x,y))

      def show_im(self):
          pp.imshow(self.i,interpolation="nearest")
          pp.show()

      def ll_corner(self):
          return self.ll

      def ul_corner(self):
          return self.ul

      def lr_corner(self):
          return self.lr

      def ur_corner(self):
          return self.ur

      def daw__line_to_image(self, x, y, x1, y1):
          draw1 = ImageDraw.Draw(self.i)
          draw1.line(((x,y),(x+x1,y+y1)), fill=0)

