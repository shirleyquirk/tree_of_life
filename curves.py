'''our path issues.

there exists some function C(s)
    simplest case: C=s
    one preferred case C=a*(e^bx-e^-bx) + c*(e^dx-e^-dx) + ...
    or alternatively C=sum[2^i*(a1,a3,...)*x^i/(i!)] for odd i
    
theta == integral(C(s),s)

and x,y parametrized as integral(cos(theta),s), integral(sin(theta),s)

which we solve by taking a taylor expansion of cos/sin.


this gives us a pretty curve.

next problem: for a given t0,t1, find the c0,c1 that will give us a curve between them

if t0 and t1 are defined relative to the line connecting them:
    for any s0,s1 on our clothoid, theta'==atan((y1-y0)/(x1-x0))  and therefore t0+theta'=theta(s0), t1+theta'=theta(s1)
    
    subtracting, t1-t0=theta(s1)-theta(s0); theta(s1)=theta(s0)+t1-t0
    
    tan(theta')==(y1-y0)/(x1-x0)
    
    and theta'==theta(s0)-t0==theta(s1)-t1
    
    so (y1-y0)/(x1-x0)= cos(theta(s0)-t0)/sin(theta(s0)-t0) =  ( cos(theta(s0))cos(t0)-sin(theta(s0))sin(t0) )/( sin(theta(s0))cos(t0) - cos(theta(s0))sin(t0) )
    = (y(s1)-y(s0))/(x(s1)-x(s0)
    = (y(s(theta(s1)))-y(s0))/(x(s(theta(s1)))-x(s0))
    = (y(s(theta(s0)+t1-t0))-y(s0))/(x(s(theta(s0)+t1-t0))-x(s0))
    
    aaand we solve for s0
    
    the sticking point is getting the inverse function of theta(s)
    
    basically we'll need an interpolating lookup table to calculate theta(s) anyway, so i guess we go from there.

    wait. so if s(theta) and theta(s) are blackbox functions
    and so is y(s), how do we solve for s0?
    don't we need s(theta)=poly(theta) (but with no sqrts lol) i'm not sure this is functional.
    
    other option: if theta(s) is a sum of exponentials, s(theta) is analytical. but less so for a/b(e^bt+e^-bt)+c/d(e^dt+e^-dt) cuz you're solving a quartic
    
    ugh.
    ok, righthandside: cos(theta(s0)) that is obvs a taylor series.  poly1(s0)/poly2(s0)
    lhs: if we had poly3(s0)/poly4(s0) then poly1(s0)*poly4(s0)=poly3(s0)*poly2(s0) ... ==> poly5(s0)-poly6(s0)=0 and numerical root find. jesus.
    so no advantage to being polynomials, then.
    depends. i mean, algorithms exist.  polynomial division exists i'd say its more an issue of the coefficients needing to be rational to maintain accuracy
    you're using 500 terms of a taylor series (still dont know why it need sthat many... and numbers like 2^500/500! crop up
    blackboxrhs(s0)== 
'''


'''
    fuck all that. absurdity, and requires numerical sol'n at the end anyway.
    
    instead.  Given blackbox x,y(s) and theta(s). 
        choose s,
        find where a ray from s and along a line theta0 away from theta(s), intersects s.
        if theta(s1)!=theta1,move along s in some direction until it does. 
        

    need: intersects(scurve,s,theta):
        #returns list of points on scurve that the line y-y(s)=tan(theta)*(x-x(s)) intersects
        
   GetIntersections(curve C1, curve C2):
        intersections = {}
        If BoundsC1 and BoundsC2 are bigger than two pixels, and they overlap, do:
            Cut C1 in half, generating subcurves S1 and S2.
            Cut C2 in half, generating subcurves S3 and S4.
            for each pair {S1, S3}, {S1, S4}, {S2, S3}, {S2, S4} do:
                intersections.merge(GetIntersections(pair))
            return intersections
        else if BoundsC1 and BoundsC2 span two pixel each, and they overlap, do:
            treat the curves as lines, and return {line intersection}
        else
            there are no intersection points between the two curves, return {}
        
'''

from operator import itemgetter,setitem
from collections import namedtuple
Point=namedtuple('Point',('x','y'))
class Rect(dict):
    def __init__(self,*args):
        #d={'x1':x1,'x2':x2,'y1':y1,'y2':y2}
        super().__init__(self)
        if len(args)==4:
            self['x0']=args[0]
            self['y0']=args[1]
            self['x1']=args[2]
            self['y1']=args[3]
        elif len(args)==1 and type(args[0]) in (list,tuple):
            args=args[0]
            self['x0']=args[0]
            self['y0']=args[1]
            self['x1']=args[2]
            self['y1']=args[3]
        elif len(args)==2 and len(args[0])==2 and len(args[1])==2:
            self['x0']=args[0][0]
            self['y0']=args[0][1]
            self['x1']=args[1][0]
            self['y1']=args[1][1]
        else:
            return None

    def _setitem_f(*args):
        def setter(s,v):
            if len(args)==1:
                v=[v]
            for v,a in zip(v,args):
                setitem(s,a,v)
        return setter
    def contains(self,point):
            if point.x>self.left and point.x<self.right and \
                point.y>self.top and point.y<self.bottom:
                return True
            else:
                return False    
    def overlaps(self,other):
        if self.left<other.right and self.right>other.left and self.top<other.bottom and self.bottom>other.top:
            return True
        return False
    def area(self):#sure we can have negative area, why not
        return (self.x1-self.x0)*(self.y1-self.y0)
    x0=property(lambda s: s.__getitem__('x0'),_setitem_f('x0'))
    x1=property(lambda s:s.__getitem__('x1'),_setitem_f('x1'))
    y0=property(lambda s:s.__getitem__('y0'),_setitem_f('y0'))
    y1=property(lambda s:s.__getitem__('y1'),_setitem_f('y1'))
    
    p0=property(lambda s:Point(s.x0,s.y0),_setitem_f('x0','y0'))
    p2=property(lambda s:Point(s.x1,s.y0))
    p1=property(lambda s:Point(s.x1,s.y1),_setitem_f('x1','y1'))
    p3=property(lambda s:Point(s.x0,s.y1))
    left=property(lambda s: min(s.x0,s.x1))
    right=property(lambda s: max(s.x0,s.x1))
    top=property(lambda s: min(s.y0,s.y1))
    bottom=property(lambda s: max(s.y0,s.y1))

from math import sqrt
def calc_box(start, curves): #TODO: modify (using de casteljau?) to work with arbitrary order beziers, (incl lines)
    P0 = start
    bounds = [[P0[0]], [P0[1]]]

    for c in curves:
        P1, P2, P3 = c

        bounds[0].append(P3[0])
        bounds[1].append(P3[1])

        for i in [0, 1]:
            f = lambda t: (
                (1-t)**3 * P0[i] 
                + 3 * (1-t)**2 * t * P1[i] 
                + 3 * (1-t) * t**2 * P2[i]
                + t**3 * P3[i])

            b = 6 * P0[i] - 12 * P1[i] + 6 * P2[i]
            a = -3 * P0[i] + 9 * P1[i] - 9 * P2[i] + 3 * P3[i]
            c = 3 * P1[i] - 3 * P0[i]

            if a == 0:
                if b == 0:
                    continue
                t = -c / b
                if 0 < t < 1: 
                    bounds[i].append(f(t))
                continue

            b2ac = b ** 2 - 4 * c * a
            if b2ac < 0: 
                continue
            t1 = (-b + sqrt(b2ac))/(2 * a)
            if 0 < t1 < 1: bounds[i].append(f(t1))
            t2 = (-b - sqrt(b2ac))/(2 * a)
            if 0 < t2 < 1: bounds[i].append(f(t2))

        P0 = P3

    x1 = min(bounds[0])
    x2 = max(bounds[0])
    y1 = min(bounds[1])
    y2 = max(bounds[1]) 
    return Rect(x1, y1, x2, y2)
#calc_box((532,333),[(117,305,28,93,265,42)])
def interp(a,b,p=0.5):
    try: 
        len(a)+len(b)
    except TypeError:
        return (a+b)*p
    return tuple((i+j)*p for i,j in zip(a,b))
def split_curve(start,curves):#splits list of beziers into two. each curve in the format [(c0x,c0y),(c1x,c1y)....(x,y)]
    if type(curves) is not list:
        curves=list(curves)
    if type(curves[0]) is not list:
        curves=[list(curve) for curve in curves]
    order=len(curves[0])
    print('order:',order)
    one=curves[:len(curves)//2]
    two=curves[len(curves)//2:]
    print('one:',one)
    print('two:',two)
    if len(one)==len(two):
        return [start]+one,[one[-1][-1]]+two
    else:#second list will be longer by one. split the first curve in the second list, add first half to list1
        one=[[start]]+one
        curve=[one[-1][-1]]+two.pop(0)
        print('splitting curve:',curve)
        coll=[]
        while curve:
            for i in range(len(curve)-1):
                coll.append(curve[i])
                curve[i]=interp(curve[i],curve[i+1])
            coll.append(curve.pop())
        front=[]
        idx=0
        for i in range(order):
            idx=idx-i-1
            front=[coll[idx]]+front
        #front=coll[-6],coll[-3],coll[-1]
        back=[]
        idx=-1
        for i in range(order):
            idx=idx-i-1
            back.append(coll[idx])
        #back=coll[-2],coll[-4],coll[-7]
        return one.pop(0)+one+[front],[front[-1]]+[back]+two
    
def lineintersect(r1,r2):
    #y-y0=(y1-y0)/(x1-x0)*(x-x0)
    #y-y2=(y3-y2)/(x3-x2)*(x-x2)
    #(y1-y0)/(x1-x0)*(x-x0)-(y3-y2)/(x3-x2)*(x-x2)=y2-y0
    #a*(x-x0)-b*(x-x2)=y2-y0
    #ax-ax0-bx+bx2=y2-y0
    #(a-b)x=y2-y0-bx2+ax0
    #x=(y2-y0-bx2+ax0)/(a-b)
    if r1.x1==r1.x0:
        #vertical r1.
        x=r1.x0
        if r2.x1==r2.x0:#parallel, possibly colinear
                if r2.x1==r1.x1:
                    y=sorted([r1.y0,r1.y1,r2.y0,r2.y1])
                    return x,(y[1]+y[2])/2
                else:
                    return False
        b=(r2.y1-r2.y0)/(r2.x1-r2.x0)
        return x,b*(x-r2.x0)+r2.y0

    a=(r1.y1-r1.y0)/(r1.x1-r1.x0)
    
    if r2.x1==r2.x0:#vertical r2
        x=r2.x0
        return x,a*(x-r1.x0)+r1.y0
    
    b=(r2.y1-r2.y0)/(r2.x1-r2.x0)
    
    if a==b:#colinear (parallel) lines. return midpoint of overlap? if they overlap, that is.
        if a*(r2.x0-r1.x0)+r1.y0==r2.y0: #colinear.
            x=sorted([r1.x0,r1.x1,r2.x0,r2.x1])
            y=sorted([r1.y0,r1.y1,r2.y0,r2.y1])
            return ((x[1]+x[2])/2,(y[1]+y[2])/2)
        else:
            return False
    x=(r2.y0-r1.y0-b*r2.x0+a*r1.x0)/(a-b)
    return x,a*(x-r1.x0)+r1.y0
            
def Intersections(path1,path2,minArea):
    b1=calc_box(path1)
    b2=calc_box(path2)
    if b1.overlaps(b2):
        if abs(b1.area)<minArea and abs(b2.area)<minArea:
            yield lineintersect(b1,b2)
        else:
            a,b=split_curve(path1)
            c,d=split_curve(path2)
            ints=[]
            for p1,p2 in [(a,c),(a,d),(b,c),(b,d)]:
                ints.extend(Intersections(p1,p2))
            for i in ints:
                yield i
    else:
        return    


'''
// Source: http://blog.hackers-cafe.net/2009/06/how-to-calculate-bezier-curves-bounding.html
// Original version: NISHIO Hirokazu
// Modifications: Timo

var pow = Math.pow,
  sqrt = Math.sqrt,
  min = Math.min,
  max = Math.max;
  abs = Math.abs;

function getBoundsOfCurve(x0, y0, x1, y1, x2, y2, x3, y3)
{
  var tvalues = new Array();
  var bounds = [new Array(), new Array()];
  var points = new Array();

  var a, b, c, t, t1, t2, b2ac, sqrtb2ac;
  for (var i = 0; i < 2; ++i)
  {
    if (i == 0)
    {
      b = 6 * x0 - 12 * x1 + 6 * x2;
      a = -3 * x0 + 9 * x1 - 9 * x2 + 3 * x3;
      c = 3 * x1 - 3 * x0;
    }
    else
    {
      b = 6 * y0 - 12 * y1 + 6 * y2;
      a = -3 * y0 + 9 * y1 - 9 * y2 + 3 * y3;
      c = 3 * y1 - 3 * y0;
    }

    if (abs(a) < 1e-12) // Numerical robustness
    {
      if (abs(b) < 1e-12) // Numerical robustness
      {
        continue;
      }
      t = -c / b;
      if (0 < t && t < 1)
      {
        tvalues.push(t);
      }
      continue;
    }
    b2ac = b * b - 4 * c * a;
    sqrtb2ac = sqrt(b2ac);
    if (b2ac < 0)
    {
      continue;
    }
    t1 = (-b + sqrtb2ac) / (2 * a);
    if (0 < t1 && t1 < 1)
    {
      tvalues.push(t1);
    }
    t2 = (-b - sqrtb2ac) / (2 * a);
    if (0 < t2 && t2 < 1)
    {
      tvalues.push(t2);
    }
  }

  var x, y, j = tvalues.length,
    jlen = j,
    mt;
  while (j--)
  {
    t = tvalues[j];
    mt = 1 - t;
    x = (mt * mt * mt * x0) + (3 * mt * mt * t * x1) + (3 * mt * t * t * x2) + (t * t * t * x3);
    bounds[0][j] = x;

    y = (mt * mt * mt * y0) + (3 * mt * mt * t * y1) + (3 * mt * t * t * y2) + (t * t * t * y3);
    bounds[1][j] = y;
    points[j] = {
      X: x,
      Y: y
    };
  }

  tvalues[jlen] = 0;
  tvalues[jlen + 1] = 1;
  points[jlen] = {
    X: x0,
    Y: y0
  };
  points[jlen + 1] = {
    X: x3,
    Y: y3
  };
  bounds[0][jlen] = x0;
  bounds[1][jlen] = y0;
  bounds[0][jlen + 1] = x3;
  bounds[1][jlen + 1] = y3;
  tvalues.length = bounds[0].length = bounds[1].length = points.length = jlen + 2;

  return {
    left: min.apply(null, bounds[0]),
    top: min.apply(null, bounds[1]),
    right: max.apply(null, bounds[0]),
    bottom: max.apply(null, bounds[1]),
    points: points, // local extremes
    tvalues: tvalues // t values of local extremes
  };
};

// Usage:
var bounds = getBoundsOfCurve(532,333,117,305,28,93,265,42);
console.log(JSON.stringify(bounds));
// Prints: {"left":135.77684049079755,"top":42,"right":532,"bottom":333,"points":[{"X":135.77684049079755,"Y":144.86387466397255},{"X":532,"Y":333},{"X":265,"Y":42}],"tvalues":[0.6365030674846626,0,1]} 
'''
