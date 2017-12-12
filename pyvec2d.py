from collections import namedtuple

#import numpy as np
import math as np
PYPY=True

Pol = namedtuple('Pol',['r','t'])
Car = namedtuple('Car',['x','y'])

def degrees(radians):
	return 360*radians/2/np.pi
def radians(degrees):
	return degrees*2*np.pi/360
class Vec2D():
	def __init__(self,x=None,y=None,r=None,t=None):
		#self.car=Car(x,y)
		#self.pol=Pol(r,t)
		self._pol=False
		self._car=False
		if x!=None and y!=None:
			self.x=x
			self.y=y
			self._car=True
			#self._update_pol()
		elif r!=None and t!=None:
			self.r=r
			self.t=t
			self._pol=True
			#self._update_car()
		#self.x=self.car.x
		#self.y=self.car.y
		#self.r=self.pol.r
		#self.t=self.pol.t
	def car(self):
		if not self._car:
			self._update_car()
		return (self.x,self.y)
	def pol(self):
		if not self._pol:
			self._update_pol()
		return (self.r,self.t)
	def __repr__(self):
		if self._pol:
			return "Vec2D(r="+str(self.r)+", θ="+str(degrees(self.t))+"°)"
		else:
			return "Vec2D(x="+str(self.x)+", y="+str(degrees(self.y))+")"
	def _update_car(self):
		#self.car=Car(self.pol.r*np.cos(self.pol.t),self.pol.r*np.sin(self.pol.t))
		#self.x=self.car.x
		#self.y=self.car.y
		self.x=self.r*np.cos(self.t)
		self.y=self.r*np.sin(self.t)
		self._car=True
	def _update_pol(self):
		self.r=np.sqrt(self.x**2+self.y**2)
		
		self.t=np.atan2(self.y,self.x)   #PYPY
		#self.t=np.arctan2(self.y,self.x)#cPython
		
		self._pol=True
	def __mul__(self,other):
		if not self._car:
			self._update_car()
		return Vec2D(x=self.x*other,y=self.y*other)
	def __rmul__(self,other):
		if not self._car:
			self._update_car()
		return Vec2D(x=self.x*other,y=self.y*other)
	def __add__(self,other):
		if not self._car:
			self._update_car()
		if not other._car:
			other._update_car()
		return Vec2D(x=self.x+other.x,y=self.y+other.y)
	def __sub__(self,other):
		if not self._car:
			self._update_car()
		if not other._car:
			other._update_car()
		return Vec2D(x=self.x-other.x,y=self.y-other.y)
	def cross(self,other):
		if not self._car:
			self._update_car()
		if not other._car:
			other._update_car()
		return self.x*other.y-self.y-other.x
	def dot(self,other):
		if not self._car:
			self._update_car()
		if not other._car:
			other._update_car()
		return self.x*other.x+self.y*other.y
	def rotate(self,t):
		if not self._pol:
			self._update_pol()
		self.t+=t;
		#self.pol=Pol(self.r,self.t)
		self._car=False
		self.x=None
		self.y=None
	
