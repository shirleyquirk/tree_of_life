from cvec2d import cVec2D as V
from cvec2d import degrees,radians
class Vec2D():
    @classmethod
    def fromcVec(cls,cvec):
        ret=cls()
        ret.v=cvec
        return ret
    
    def __init__(self,x=None,y=None,r=None,t=None):
        if (x !=None and y!=None):
            self.v=V(x=float(x),y=float(y))
        elif(r!=None and t!=None):
            self.v=V(r=float(r),t=float(t))
        else:
            self.v=None
    def car(self):
        return(self.v.car())
    def pol(self):
        return(self.v.pol())
    def __repr__(self):
        if self.v._pol:
            return "Vec2D(r="+str(self.v.r())+", θ="+str(degrees(self.v.t()))+"°)"
        else:
            return "Vec2D(x="+str(self.v.x())+", y="+str(self.v.y())+")"
    def __mul__(self,other):
        return Vec2D.fromcVec(self.v.__mul__(other))
    def __rmul__(self,other):
        return Vec2D.fromcVec(self.v.__mul__(other))
    def __add__(self,other):
        return Vec2D.fromcVec(self.v.__add__(other.v))
    def __sub__(self,other):
        return Vec2D.fromcVec(self.v.__sub__(other.v))
    def cross(self,other):
        return Vec2D.fromcVec(self.v.cross(other.v))
    def dot(self,other):
        return Vec2D.fromcVec(self.v.dot(other.v))
    def rotate(self,t):
        self.v.rotate(t)
    def x(self):
        return self.v.x()
    def y(self):
        return self.v.y()
    def r(self):
        return self.v.r()
    def t(self):
        return self.v.t()
