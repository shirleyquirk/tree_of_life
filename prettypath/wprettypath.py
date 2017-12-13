from cprettypath import PrettyPath as PP
from cprettypath import _map

#from cvec2d import *
from wvec2d import *
MIN_C=0
MAXDTHETA=0.3
import math as np

class PrettyPath():
    def __init__(self,start,t0,c0,c1):
        self.t0=t0
        self.start=start
        self.c0=c0
        self.c1=c1
        self.end=None
        self.t1=None
        self.pp=PP(self.t0,self.start,self.c0,self.c1)
        print("wprettypath: self.start:",self.start,"self.pp.start",self.pp.start)
    def _cp(self,s):
        return self.pp._cp(s)
    def pathpoints(self,segs):
        t=Vec2D(r=self.t0.r(),t=self.t0.t())
        #t=self.t0
        ret=[]
        p=self.start
        #max dtheta! that's what we care about.
        c=0
        for i in range(segs):
            s=_map(i,0,segs,0,1)
            curvature=self._cp(s)
            dt=curvature*(1/segs)
            subdiv=int(abs(dt)//MAXDTHETA)+1
            jret=[]
            for j in range(subdiv):
                #print("i:",i," j:",j," t:",t)
                jret.append((p,1/c if c!=0 else None,t.t))
                s=_map(i+j/subdiv,0,segs,0,1)
                curvature=self._cp(s)
                
                dt=curvature*(1/(segs*subdiv))
                if curvature<-MIN_C or curvature>MIN_C:
                    pass
                else:
                    curvature=0
                    
                c=curvature/t.r()
                
                if curvature:
                    #r=t*(1/curvature)
                    #r._update_pol()
                    r=Vec2D(r=1/c,t=t.t())
                    delta=Vec2D(r=2*r.r()*np.sin(dt/2),t=r.t()+dt/2)
                    p=p+delta
                    #r.rotate(0.5*np.pi)
                    #p=p+r
                    #r.rotate(dt)
                    #p=p-r
                    t.rotate(dt)
                else:
                    #self.straights+=1
                    delta=t*(1/(segs*subdiv))
                    p=p+delta
            ret.append(jret)
        ret.append([(p,1/c if c!=0 else None,t.t())])
        #assert(len(ret)>1)
        self.pp.end=p
        self.end=p
        self.t1=t
        self.pp.t1=t
        return(ret)

    def path_to(self,*args):
        self.pp.path_to(*args)
        self.t0=self.pp.t0
        self.end=self.pp.end
        self.t1=self.pp.t1

'''    def pathpoints(self,*args):
        ret=self.pp.pathpoints(*args)
        self.t1=self.pp.t1
        self.end=self.pp.end
        return ret'''
