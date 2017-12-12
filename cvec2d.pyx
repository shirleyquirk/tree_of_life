#import numpy as np
import math as np

def degrees(double r):
    return 360*r/2/np.pi
def radians(double d):
    return d*2*np.pi/360
class cVec2D():
    def __init__(self,*args,**kwargs):
        #self.car=Car(x,y)
        #self.pol=Pol(r,t)
        self._pol=False
        self._car=False
        cdef double _x,_y,_r,_t
        if 'x' in kwargs and 'y' in kwargs:
            self._x=kwargs['x']
            self._y=kwargs['y']
            self._car=True
            #self._update_pol()
        elif 'r' in kwargs and 't' in kwargs:
            self._r=kwargs['r']
            self._t=kwargs['t']
            self._pol=True
        else:
            self._x=args[0]
            self._y=args[1]
            self._car=True
    def car(self):
        if not self._car:
            self._update_car()
        return (self._x,self._y)
    def pol(self):
        if not self._pol:
            self._update_pol()
        return (self._r,self._t)
    def __repr__(self):
        if self._pol:
            return "cVec2D(r="+str(self._r)+", θ="+str(degrees(self._t))+"°)"
        else:
            return "cVec2D(x="+str(self._x)+", y="+str(degrees(self._y))+")"
    def _update_car(self):
        #self.car=Car(self.pol.r*np.cos(self.pol.t),self.pol.r*np.sin(self.pol.t))
        #self.x=self.car.x
        #self.y=self.car.y
        self._x=self._r*np.cos(self._t)
        self._y=self._r*np.sin(self._t)
        self._car=True
    def _update_pol(self):
        self._r=np.sqrt(self._x**2+self._y**2)
        
        self._t=np.atan2(self._y,self._x)   #PYPY
        self._pol=True
    def __mul__(self,other):
        if not self._car:
            self._update_car()
        return cVec2D(x=self._x*other,y=self._y*other)
    def __rmul__(self,other):
        if not self._car:
            self._update_car()
        return cVec2D(x=self._x*other,y=self._y*other)
    def __add__(self,other):
        if not self._car:
            self._update_car()
        if not other._car:
            other._update_car()
        return cVec2D(x=self._x+other._x,y=self._y+other._y)
    def __sub__(self,other):
        if not self._car:
            self._update_car()
        if not other._car:
            other._update_car()
        return cVec2D(x=self._x-other._x,y=self._y-other._y)
    def cross(self,other):
        if not self._car:
            self._update_car()
        if not other._car:
            other._update_car()
        return self._x*other._y-self._y-other._x
    def dot(self,other):
        if not self._car:
            self._update_car()
        if not other._car:
            other._update_car()
        return self._x*other._x+self._y*other._y
    def rotate(self,t):
        if not self._pol:
            self._update_pol()
        self._t+=t;
        self._car=False
        #self._x=None
        #self._y=None
    def x(self):
        if not self._car:
            self._update_car()
        return self._x
    def y(self):
        if not self._car:
            self._update_car()
        return self._y
    def r(self):
        if not self._pol:
            self._update_pol()
        return self._r
    def t(self):
        if not self._pol:
            self._update_pol()
        return self._t
