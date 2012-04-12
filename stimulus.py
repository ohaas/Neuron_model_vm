__author__ = 'ohaas'

import Image, ImageDraw
import matplotlib.pyplot as pp
from matplotlib.patches import FancyBboxPatch as fbp

class image(object):

      def __init__(self,main_size,square_size,start):
          self.i=Image.new("1",(main_size,main_size),1)
          draw = ImageDraw.Draw(self.i)
          self.ll=(start,start)
          self.ul=(start, start+1+square_size)
          self.lr=(start+1+square_size, start)
          self.ur=(start+1+square_size,start+1+square_size)
          draw.line((self.ll,self.lr,self.ur,self.ul,self.ll), fill=0)
          self.main_size=main_size
          self.square_size=square_size
          self.start=start
          #pp.imshow(self.i, interpolation="nearest")

      def pix_value(self,x,y):
          return self.i.getpixel((x,y))

      def pic(self):
          ax=pp.gca()
          pp.axis([0,self.main_size,0, self.main_size])
          ax.add_patch(fbp((self.start,self.start), self.square_size,self.square_size, boxstyle="square,pad=0.", facecolor='none', linewidth=4))


      @property
      def ll_corner(self):
          return self.ll

      @property
      def ul_corner(self):
          return self.ul

      @property
      def lr_corner(self):
          return self.lr

      @property
      def ur_corner(self):
          return self.ur

      def daw__line_to_image(self, x, y, x1, y1):
          draw1 = ImageDraw.Draw(self.i)
          draw1.line(((x,y),(x+x1,y+y1)), fill=0)

if __name__ == '__main__':
    im=image(20,8,5)
    im.pic()
    pp.show()