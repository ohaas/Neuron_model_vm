import time

__author__ = 'ohaas'
import matplotlib.pyplot as pp


class Auto(object):

    #Constructor
    def __init__(self, benzin, color):
        self._tankstand = benzin
        self._color = color
        self._buydate = time.time()


    def tankstand(self):
        return self._tankstand

    def auftanken(self, benzin):
        self._tankstand += benzin

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    @property
    def age(self):
        return time.time() - self._buydate


class Cabrio(Auto):

    def __init__(self, benzin, farbe):
        super(Cabrio, self).__init__(benzin, farbe)
        self._verdeck_status = 'offen'

    @property
    def verdeck_status(self):
        return self._verdeck_status



if __name__ == '__main__':


    x = V1.do_v1()

    OlisAuto = Cabrio(10, 'green')
    LaurenceAuto = Auto(20, 'red')

    print OlisAuto, LaurenceAuto
    print OlisAuto.color
    print OlisAuto.tankstand()
    print LaurenceAuto.tankstand()

    LaurenceAuto.auftanken(15)

    print LaurenceAuto.tankstand()

    OlisAuto.color = 'red'
    print OlisAuto.color

    print OlisAuto.verdeck_status
