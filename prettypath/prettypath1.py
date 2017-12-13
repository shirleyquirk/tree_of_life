from vec2d import Vec2D
#from cvec2d import *
import svgwrite
import math as np
#import numpy as np

def degrees(radians):
    return 360*radians/2/np.pi
def radians(degrees):
    return degrees*2*np.pi/360


def thetadiff(t1,t2):
    #d=degrees(t1%(2*np.pi)-t2%(2*np.pi))
    d=degrees(abs(t1-t2))
    #if d>180:
    #    d=d-360
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

def optimize2(**kwargs):
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
    cdef int w,j,k
    cdef double x,y
    while min_dist[0]>error:
        order_of_mag+=1
        if order_of_mag>6:
            return min_dist
        if width/10**order_of_mag>bounds:
            w=bounds*10**order_of_mag
        else:
            w=width
        dists=[]
        #x=0
        #y=0
        #j=0
        #k=0
        x,y=(0,0)
        s2=1.41412135623730951
        for direction in [(-1,-1),(-s2,0),(-1,1),(0,-s2),(0,1.414),(1,-1),(s2,0),(1,1)]:
            pass
        
        #i believe there should be multiple solutions corresponding to t0+npi t1+npi
        #what we should specify is not t1, but deltat.
        '''
        for x in [(j-w)/(10**order_of_mag)+centre[0] for j in range(2*w+1)]:
            for y in [(k-w)/(10**order_of_mag)+centre[1] for k in range(2*w+1)]:
                h=g(p,(x,y),t1=t1,t0=t0,end=end,segs=segs)
                dists.append((h[0],(h[1],h[2]),(x,y)))
        '''
        min_dist=min(dists)
        centre=min_dist[2]
    return min_dist

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
    cdef int w,j,k
    cdef double x,y
    while min_dist[0]>error:
        order_of_mag+=1
        if order_of_mag>6:
            return min_dist
        if width/10**order_of_mag>bounds:
            w=bounds*10**order_of_mag
        else:
            w=width
        dists=[]
        #x=0
        #y=0
        #j=0
        #k=0
        for x in [(j-w)/(10**order_of_mag)+centre[0] for j in range(2*w+1)]:
            for y in [(k-w)/(10**order_of_mag)+centre[1] for k in range(2*w+1)]:
                h=g(p,(x,y),t1=t1,t0=t0,end=end,segs=segs)
                dists.append((h[0],(h[1],h[2]),(x,y)))
        min_dist=min(dists)
        centre=min_dist[2]
    return min_dist




from copy import copy
def _map(i,a,b,c,d):
    return( (i-a)/(b-a) * (d-c) + c )
MIN_C=0
MAXDTHETA=0.3
#about 30degrees
A=3
debug=False

def flatten(l):
    r=[]
    for i in l:
        if isinstance(i,(list,tuple)):
            r.extend(flatten(i))
        else:
            r.extend([i])
    return r
    
def get_point(p,segs,xpos):
    #accepts pathpoints object, returns position, tangent
    #xpos from 0 to t0.r
    s=xpos/p.t0.r
    path=p.pathpoints(segs)
    assert(s<1)
    segs=len(path)-1
    pathi=int(s*segs)
    lowersegs=len(path[pathi])
    loweri=int((s-pathi/segs)*lowersegs*segs)
    lowerpoint=path[pathi][loweri]
    lower_s=pathi/segs+loweri/(segs*lowersegs)  
    
    upper_pathi=pathi
    upperi=loweri+1
    if upperi==len(path[pathi]):
        upperi=0
        upper_pathi+=1
        
    upperpoint=path[upper_pathi][upperi]
    upper_s=upper_pathi/segs+upperi/(segs*lowersegs)
    #print('s=',s,'lowerpoint:',(pathi,loweri),'upperpoint:',(upper_pathi,upperi))
    interp=(s-lower_s)/(upper_s-lower_s)
    #print(interp,lower_s,upper_s)
    t1=upperpoint[2]
    t0=lowerpoint[2]
    t=interp*(t1-t0)
    r=upperpoint[1]
    lowerx=lowerpoint[0].x
    lowery=lowerpoint[0].y
    upperx=upperpoint[0].x
    uppery=upperpoint[0].y
    if r==None:#line
        p=Vec2D(lowerx+interp*(upperx-lowerx),lowery+interp*(uppery-lowery))
    else:
        delt=Vec2D(r=2*r*np.sin(t/2),t=t0+t/2)
        #delt._update_car
        #print(delt)
        p=Vec2D(lowerx,lowery)+delt
    return(p,t0+t)
class PrettyPath():
    def __init__(self,start,t0,c0,c1,tightness=0):
        self.start=start
        self.t0=t0
        self.c0=c0
        self.c1=c1
        self.t1=None
        self.end=None
        self.straights=0
        self.tightness=tightness
        ret=[]
    def _cp(self,s):
        #y"(0) positive, y(0)=0, y(1)=-y(-1)
        #y(0)=self.c0, y(1)=self.c1
        #y(0)=(c0^3+c0)/2
        #y(1)=(c1^3+c1)/2
        sm=_map(s,0,1,self.c0,self.c1)
        if sm<0:
            return(-self.tightness*np.sqrt(-sm)+0.1*sm*sm*sm+0.9*sm)
        else:
            return(self.tightness*np.sqrt(sm)+0.1*sm*sm*sm+0.9*sm)
        
    '''        
    def _c(self,s):
        #A=np.e-1
        if self.c1>self.c0:#increasing
            if self.c1<0:#negative to neg
                return (np.exp(-(self.c0+(self.c1-self.c0)*s))-1)/(-A)
            elif self.c0<0:#negative to positive
                if s<self.c0/(self.c0-self.c1):
                    return (np.exp(-(self.c0+(self.c1-self.c0)*s))-1)/(-A)
                else:
                    return (np.exp(self.c0+(self.c1-self.c0)*s)-1)/(A)
            else:#pos to pos
                return (np.exp(self.c0+(self.c1-self.c0)*s)-1)/(A)
        else:#c0>=c1 decreasing or the same
            if self.c0<0:#negative, decreasing or same
                return (np.exp(-(self.c0+(self.c1-self.c0)*s))-1)/(-A)
            elif self.c1<0:#positive,decreasing to neg
                if s<self.c0/(self.c0-self.c1):
                    return (np.exp(self.c0+(self.c1-self.c0)*s)-1)/(A)
                else:
                    return (np.exp(-(self.c0+(self.c1-self.c0)*s))-1)/(-A)
            else:#pos decrease to pos or same
                return (np.exp(self.c0+(self.c1-self.c0)*s)-1)/(A)
    '''

    def _ds(self,c):
        #A=np.e-1goal=end-start

        if c<0:
            return (-A)/(((A)*c-1)*(self.c1-self.c0))
        else:
            return (A)/(((A)*c+1)*(self.c1-self.c0))

    def path_to(self,end,segs):
        #print(delta)
        self.t0.pol=(1,0)
        self.pathpoints(segs)
        delta=self.end-self.start
        goal=end-self.start
        self.t0.pol=(goal.r/delta.r,goal.t-delta.t)
        #return self.pathpoints(segs)
    def path_between(self,end,theta0,theta1,segs):
        pass
        #c1 changes until we get t1 at the end?
    def pathpoints(self,int segs):
        cdef int i=0
        cdef int j=0
        cdef int subdiv
        #self.straights=0
        
        t=Vec2D(r=self.t0.r,t=self.t0.t)
        delta=Vec2D()
        ret=[]
        p=Vec2D(self.start.x,self.start.y)
        #max dtheta! that's what we care about.
        c=0
        cdef double dt
        #print('segs:',segs)
        for i in range(segs):
            s=_map(i,0,segs,0,1)
            curvature=self._cp(s)
            dt=curvature*(1/float(segs))
            subdiv=int(abs(dt)//MAXDTHETA)+1
            #print('subdiv:',subdiv)
            jret=[]
            for j in range(subdiv):
                #print("i:",i," j:",j," t:",t)
                #print(p.x,p.y)
                
                jret.append((Vec2D(p.x,p.y),1/c if c!=0 else None,t.t))
                
                
                s=_map(i+j/float(subdiv),0,segs,0,1)
                curvature=self._cp(s)
                #print("curvature: ",curvature)
                dt=curvature*(1/float(segs*subdiv))
                #print('dt:',dt)
                if curvature<-MIN_C or curvature>MIN_C:
                    pass
                else:
                    curvature=0
                    
                c=curvature/t.r
                
                if curvature:
                    #r.pol=(1/c,t.t)
                    
                    delta.pol=(2/c*np.sin(dt/2),t.t+dt/2)
                    #print("delta:",delta)
                    p.add(delta)
                    t.rotate(dt)
                    
                    
                else:
                    #self.straights+=1
                    delta=t*(1/float(segs*subdiv))
                    #print("delta:",delta)
                    p.add(delta)
            ret.append(jret)
        #print(p.x,p.y)
        ret.append([(Vec2D(p.x,p.y),1/c if c!=0 else None,t.t)])
        #assert(len(ret)>1)
        self.end=p
        #self.t1=t
        self.t1=Vec2D(r=t.r,t=t.t)
        
        
        return(ret)
    '''def path(self,dcurve,**kwargs):
        kwargs['debug']=debug
        p=svgwrite.path.Path(**kwargs)
        bez=catmull2bezier(self.pathpoints(dcurve))
        for b in bez:
            p.push(['M',b[0]car])
            p.push(['C',b[1].x,b[1].y,b[2].x,b[2].y,b[3].x,b[3].y])
        return p'''
    def taperedpath(self,segs,start_width,**kwargs):
        kwargs['debug']=debug
        end_width=kwargs.pop('end_width',0)
        closed=kwargs.pop('closed',False)
        p=svgwrite.path.Path(**kwargs)
        points=[]
        for i in self.pathpoints(segs):
            points.extend(i)
        
        left=[]
        right=[]
        for i in range(len(points)):
            pt=points[i]
            width=_map(i,0,len(points)-1,start_width,end_width)
            left.append((pt[0]+Vec2D(r=width/2,t=(pt[2]-np.pi*0.5)),pt[1]+width/2 if pt[1] else None,pt[2]))
            right.append((pt[0]+Vec2D(r=width/2,t=(pt[2]+np.pi*0.5)),pt[1]-width/2 if pt[1] else None,pt[2]))
        right.reverse()
        points=left+right
        p.push(['M',left[0][0].car])
        #p.push(['M',self.right[0][0].car])
        #p.push(['L',self.left[0][0].car])
        down=False
        for i in range(1,len(points)):
            pt=points[i]
            if i==len(left):
                down=True
                if end_width!=0:
                    if True:#closed:
                        p.push(['L',pt[0].car])
                    else:
                        p.push(['M',pt[0].car])
            else:
                if (not down and pt[1]) or (down and points[i-1][1]):
                    deltat=pt[2]- points[i-1][2]
                    a='+' if deltat>0 else '-'
                    p.push_arc(pt[0].car,0,abs(points[i-1][1]) if down else abs(pt[1]),large_arc=False,angle_dir=a,absolute=True)
                else:
                    p.push(['L',pt[0].car])
        if closed:
            p.push(['Z'])
        return p

    def g(self,here,**kwargs):
        cdef double t1=kwargs.pop('t1')
        cdef double t0=kwargs.pop('t0')
        end=kwargs.pop('end')
        cdef int segs=kwargs.pop('segs')
        
        self.c0=here[0]
        self.c1=here[1]
        self.path_to(end,segs)
        self.pathpoints(segs)
        return (np.sqrt(thetadiff(t1,self.t1.t)**2+thetadiff(t0,self.t0.t)**2),thetadiff(t1,self.t1.t),thetadiff(t0,self.t0.t))

    def optimize(self,**kwargs):
        end=kwargs.pop('end')
        width=kwargs.pop('width',10)
        #oom=kwargs.pop('oom')
        error=kwargs.pop('error',1)
        cdef double t0=kwargs.pop('t0')
        cdef double t1=kwargs.pop('t1')
        segs=kwargs.pop('segs')
        bounds=kwargs.pop('bounds',10)
        
        min_dist=[999]
        centre=(0,0)
        #for order_of_mag in range(oom):
        order_of_mag=-1
        cdef int w,j,k
        cdef double x,y
        while min_dist[0]>error:
            order_of_mag+=1
            if order_of_mag>6:
                return min_dist
            if width/10**order_of_mag>bounds:
                w=bounds*10**order_of_mag
            else:
                w=width
            dists=[]
            #x=0
            #y=0
            #j=0
            #k=0
            for x in [(j-w)/(10**order_of_mag)+centre[0] for j in range(2*w+1)]:
                for y in [(k-w)/(10**order_of_mag)+centre[1] for k in range(2*w+1)]:
                    h=self.g((x,y),t1=t1,t0=t0,end=end,segs=segs)
                    dists.append((h[0],(h[1],h[2]),(x,y)))
            min_dist=min(dists)
            centre=min_dist[2]
        #return min_dist
        self.c0=min_dist[2][0]
        self.c1=min_dist[2][1]
        ###OR -min_dist[2][0],-min_dist[2][1]!!!
        self.path_to(end,segs)
        
      
    
def parse_prettypaths(ElementTree):
    def s():
        for g in ElementTree.findall('.//svg:g',ns):
            if g.get('id').startswith('prettypath'):
                yield g
    for g in s():
        widths=[]
        pathstuff={}
        paths=g.findall('svg:path',ns)
        for p in paths:
            d=p.get('d').split(' ')
            r=[]
            for i in d:
                r.extend(i.split(','))
            d=r
            if len(d)==5:#width line
                st=Vec2D(*d[1:3])
                en=Vec2D(*d[3:5])
                w=(st-en).r
                m=(st+en)*0.5
                widths.append(w,m)
            else:#path
                assert(d.pop(0)=='M')#will not work if relative coordinates
                st=Vec2D(d.pop(0),d.pop(0))
                assert(d.pop(0)=='C')
                tan0=Vec2D(d.pop(0),d.pop(0))
                tan1=Vec2D(d.pop(0),d.pop(0))
                en=Vec2D(d.pop(0),d.pop(0))
                assert(len(d)==0)#should be it
                pathstuff['start']=st
                pathstuff['end']=en
                pathstuff['theta0']=tan0-st
                pathstuff['theta1']=tan1-en

        pathstuff['width0']=min(((w[1]-pathstuff['start']).r,w[0]) for w in widths)[1]
        pathstuff['width1']=max(((w[1]-pathstuff['end']).r,w[0]) for w in widths)[1]

        yield pathstuff

def cubic_approx(points):
    A=[(t**3,t**2,t,1) for t in [i/(len(points)-1) for i in range(len(points))]]
    B=[point.car for point in points]
    X=np.linalg.lstsq(A,B)[0]
    X=list(zip(*X))
    M=[[-1,3,-3,1],\
       [3,-6,3,0],\
       [-3,3,0,0],\
       [1,0,0,0]]
    return list(zip(*(np.linalg.solve(M,x) for x in X)))
def cubic_approx_clamped(points,p0):
    A=[(t**3,t**2,t) for t in [i/(len(points)-1) for i in range(len(points))]]
    B=[(point-p0).car for point in points]
    X=np.linalg.lstsq(A,B)[0]
    X+=np.array(p0.car)*np.array(((1,),(-3,),(3)))
    X=list(zip(*X))
    M=[[3,-3,1],\
       [-6,3,0],\
       [3,0,0]]
    return list(zip(*(np.linalg.solve(M,x) for x in X)))
def convert_to_beziers(pathfun,numbezs=1,s0=0,s1=1,fitpoints=20)
    coefs=[]
    for n in range(1,numbezs+1):
        points=[pathfun(s0+(s1-s0)*i/fitpoints*n/numbezs) for i in range(fitpoints+1)]
        if n==1:
            coefs.extend(cubic_approx(points))
        else:
            coefs.extend(cubic_approx_clamped(points,coefs[-1])
    return coefs

