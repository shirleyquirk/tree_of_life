

#from cprettypath import PrettyPath
from vec2d import Vec2D
#from wprettypath import PrettyPath
#from prettypath import PrettyPath
from cprettypath import PrettyPath,optimize,radians#,g,thetadiff
#from wvec2d import *

import math as np
'''
def degrees(radians):
	return 360*radians/2/np.pi
def radians(degrees):
	return degrees*2*np.pi/360



def thetadiff(t1,t2):
    d=degrees((t1-t2)%np.pi)
    if d>180:
        d=d-360
    return d
 
def g(p,here,**kwargs):
    t1=kwargs.pop('t1')
    t0=kwargs.pop('t0')
    end=kwargs.pop('end')
    segs=kwargs.pop('segs')
    
    p.c0=here[0]
    p.c1=here[1]
    p.path_to(end,segs)
    p.pathpoints(segs)
    return (np.sqrt(thetadiff(t1.t,p.t1.t)**2+thetadiff(t0.t,p.t0.t)**2),thetadiff(t1.t,p.t1.t),thetadiff(t0.t,p.t0.t))

def optimize(**kwargs):
    p=kwargs.pop('path')
    start=kwargs.pop('start')
    end=kwargs.pop('end')
    width=kwargs.pop('width')
    #oom=kwargs.pop('oom')
    error=kwargs.pop('error')
    t0=kwargs.pop('t0')
    t1=kwargs.pop('t1')
    segs=kwargs.pop('segs')
    bounds=kwargs.pop('bounds',5)
    
    min_dist=[999]
    centre=(0,0)
    #for order_of_mag in range(oom):
    order_of_mag=-1
    while min_dist[0]>error:
        order_of_mag+=1
        if order_of_mag>6:
            return min_dist
        if width/10**order_of_mag>bounds:
            w=bounds*10**order_of_mag
        else:
            w=width
        dists=[]
        for x in [(j-w)/(10**order_of_mag)+centre[0] for j in range(2*w+1)]:
            for y in [(k-w)/(10**order_of_mag)+centre[1] for k in range(2*w+1)]:
                h=g(p,(x,y),t1=t1,t0=t0,end=end,segs=segs)
                dists.append((h[0],(h[1],h[2]),(x,y)))
        min_dist=min(dists)
        centre=min_dist[2]
    return min_dist

def optimize(**kwargs):
    return cprettypath.optimize(**kwargs)
'''

from random import random

def profile():
    start=Vec2D(random()*1000,random()*1000)
    #start=Vec2D(21,25)
    t0=Vec2D(r=100,t=radians(random()*360))
    #t0=Vec2D(r=100,t=radians(45))
    tgoal=Vec2D(r=1,t=radians(random()*360))
    end=Vec2D(random()*1000,random()*1000)
    p=PrettyPath(start,t0,-2,2)
    #print("start",start.x,start.y)
    #print("p.start",p.start.x,p.start.y)
    #print("end",end.x,end.y)
    #p.pathpoints(5)
    #print("p.start",p.start.x,p.start.y)
    #print("p.end",p.end.x,p.end.y)
    
    #p.path_to(end,5)
    o=optimize(width=10,error=1,path=p,start=start,t0=t0,t1=tgoal,end=end,segs=5,bounds=10)
    return o
    #return 0
import cProfile
from statistics import stdev,mean
cProfile.run('''errors=[]
for k in range(100):
    errors.append(profile())
print('max error:',max(errors),'avg:',mean([e[0] for e in errors]),'stdev:',stdev([e[0] for e in errors]))''')
