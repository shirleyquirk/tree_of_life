import svgwrite
from vec2d import *
import math as np
from copy import copy,deepcopy
from cprettypath import PrettyPath,_map,radians,degrees
from random import random,randint
debug=False

from operator import itemgetter
class Branch(tuple):
    def __new__(self,l,r):
        return tuple.__new__(self,(l,r))
    def __add__(self,other):
        if type(other)==Branch or (type(other)==tuple and len(other)==2) or \
                (type(other)==list and len(other)==2):
            return Branch(self[0]+other[0],self[1]+other[1])
        elif type(other)==float or type(other)==int:
            return Branch(self[0]+other,self[1]+other)
    def __repr__(self):
        return "Bch(l="+str(self.l)+",r="+str(self.r)+")"
    def __radd__(self,other):
        return self.__add__(other)
    def __mul__(self,other):
        if type(other)==Branch:
            return Branch(self.l*other.l,self.r*other.r)
        elif type(other)==int or type(other)==float:
            return Branch(self.l*other,self.r*other)
        else:
            raise TypeError("Can't multiply Branch by type "+str(type(other)))
    def __rmul__(self,other):
        return self.__mul__(other)
    def setl(newl):
        self=Branch(newl,self[1])
    def setr(newr):
        self=Branch(self[0],newr)
    l=property(itemgetter(0),setl)
    r=property(itemgetter(1),setr)

linecolor='green'

'''
LineLen=LineLen*[0.7,0.7]
T1,1 T2,1  = [   ]  #t1 given previousbranch is t1, t2 after a t1 branch
T1,2 T2,2    [   ]  #t1 after t2 branch, t2 after t2 branch
'''
stroke_mult=3

def prettyline(start,end,**kwargs):
    dt0=kwargs.pop('dt0',radians(30))
    dt1=kwargs.pop('dt1',radians(30))
    start_width=kwargs.pop('start_width')
    end_width=kwargs.pop('end_width',0)
    render=kwargs.pop('render',False)
    t=(end-start).t
    t0=t+dt0
    t1=t+dt1
    
    if render:
        p=PrettyPath(start,Vec2D(1,0),0,0,tightness=1)
        #print("optimizing...")
        p.optimize(t0=t0,t1=t1,end=end,segs=5)
        kwargs['end_width']=end_width

        return p.taperedpath(5,start_width,**kwargs)
    else:
        kwargs['stroke_width']=start_width
        if kwargs['fill']=='none':
            kwargs['stroke']='#00aa00'
        return svgwrite.shapes.Line(start.car,end.car,**kwargs)

    
class Tree():
    #def __init__(self,x,y,theta1,theta2,size,depth,thetamult,lenmult):
    def __init__(self,here,theta,size,depth,thetamult,lenmult,**kwargs):
        #self.t1=theta1
        #self.t2=theta2
        self.t=theta
        self.maxdepth=depth
        self.size=size
        self.tm=thetamult
        self.lm=lenmult
        #self.x=x
        #self.y=y
        self.here=here
        self.render=kwargs.pop('render',False)
    def svg(self,**args):
        self.gp=svgwrite.container.Group(**args)
        #st=Vec2D(x=self.x,y=self.y)
        self._recur(self.gp,self.here,-self.size,radians(90),self.t,0)
        #gp.add(svgwrite.shapes.Line(start=st.car,end=(st+Vec2D(r=50,t=radians(90))).car,stroke_width=6,stroke='black'))
        return self.gp
    def _line(self,group,here,l,t,w,dt0=0,dt1=0):
        #group.add(svgwrite.shapes.Line(start=here.car,end=(here+Vec2D(r=l,t=t)).car,stroke='black',stroke_width=w))
        group.add(prettyline(here,here+Vec2D(r=l,t=t),dt0=dt0,dt1=dt1,stroke=linecolor,start_width=w*stroke_mult,end_width=(w-1)*stroke_mult,fill=linecolor,render=self.render))
    def _leaf(self,group,here,t,dt):
        ss=2-random()*4
        se=2-random()*4
        ss,se=sorted((ss,se))
        es=4-random()*8
        ee=4-random()*8
        es,ee=sorted((es,ee))
        N=8
        for i in range(N+1):
            p=PrettyPath(here,Vec2D(r=t.r*(1.1-0.2*random()),t=t.t+_map(i,0,N,dt.l,dt.r)),_map(i,0,N,ss,se),_map(i,0,N,es,ee))
            tp=p.taperedpath(5,stroke='green',stroke_width=0,start_width=5,fill='green',debug=debug)
        #tp=svgwrite.shapes.Ellipse(here.car,(2,4),fill='green')
        #tp.rotate(t.t,here.car)
            group.add(tp)
    def _recur(self,parent_group,here,line_length,t0,dt,depth):
        this_group=svgwrite.container.Group(debug=debug)
        parent_group.add(this_group)
        
        if depth>=self.maxdepth:
            self._leaf(this_group,here,Vec2D(r=line_length*2,t=t0),dt)
            #self._leaf(this_group,here,Vec2D(r=line_length*2,t=t0+dt.r))
            return
        #length=[line_length *0.75,line_length *0.7]
        length=self.lm*line_length
        
        
        #theta=[[t1,t2],[t1,t2]]*[0.8,0.9],[1,0.9]
        #theta = [[t1*0.8,t2*0.9],[t1,t2*0.9]]
        #theta=Branch(Branch(self.tm.l.l*dt.l,Branch(self.tm.l.r)*dt.r),Branch(self.tm.r.l*dt.l,self.tm.r.r*dt.r))
        theta=Branch(self.tm.l*dt,self.tm.r*dt)
        #theta=[[t1*self.tm[0][0],t2*self.tm[0][1]],[t1*self.tm[1][0],t2*self.tm[1][1]]]
        
        d=Branch(Vec2D(r=length.l,t=t0+dt.l),Vec2D(r=length.r,t=t0+dt.r))
        curves=Branch(((dt.r-dt.l)/2,dt.l*self.tm.l.l+(dt.r*self.tm.l.r-dt.l*self.tm.l.l)/2),\
            ((dt.l-dt.r)/2,dt.l*self.tm.r.l+(dt.r*self.tm.r.r-dt.l*self.tm.r.l)/2))
        
        self._line(this_group,here,length.l,t0+dt.l,(self.maxdepth+1-depth),dt0=curves.l[0],dt1=curves.l[1])
        self._recur(this_group,here+d.l,length[0],t0+dt.l,theta.l,depth+1)
        
        self._line(this_group,here,length.r,t0+dt.r,(self.maxdepth+1-depth),dt0=curves.r[0],dt1=curves.r[1])
        self._recur(this_group,here+d.r,length.r,t0+dt.r,theta.r,depth+1)
        
def mean(l):
    return float(sum(l))/max(len(l),1)
def flatten(l):
    r=[]
    for i in l:
        if isinstance(i,(list,tuple)):
            r.extend(flatten(i))
        else:
            r.extend([i])
    return r
def listadd_inplace(l,a):
    for i in range(len(l)):
        if isinstance(l[i],list):
            listadd_inplace(l[i],a)
        else:
            l[i]+=a
def listadd(l,a):
    ret=[]
    for i in l:
        if isinstance(i,list):
            ret.append(listadd(i,a))
        else:
            ret.append(i+a)
    return ret
def listmult_inplace(l,a):
    for i in range(len(l)):
        if isinstance(l[i],list):
            listmult_inplace(l[i],a)
        else:
            l[i]*=a
def listmult(l,a):
    ret=[]
    for i in l:
        if isinstance(i,list):
            ret.append(listmult(i,a))
        else:
            ret.append(i*a)
    return ret
from copy import copy
def tripadj(l,a):
    ret=[]
    if isinstance(l,list):
        if len(l)==3:
            l=listadd(l,a)
        for i in l:
                ret.append(tripadj(i,a))
        return ret
    else:
        return l
def f(l):

    '''oh god, i dont know its too late trust me it does something important and clever'''
    a=0        
    for i in flatten(l):
        a+=2**i
    return math.log2(a)
def mymax(x):
    #adjust for triples
    return max(flatten(tripadj(x,math.log2(3))))

def metatree(here,depths,length,dt,tm,lm,t0=radians(-90),depth=0,**kwargs):
    trees=[]
    lines=[]
    n=len(depths)
    
    if n==1:    
        if depth!=0:
            l0=length
        else:#first time
            l0=length*lm.l**(-f(depths))
            
        if isinstance(depths[0],(list,tuple)):
            m=metatree(here,depths[0],l0,dt,tm,lm,t0=t0,depth=depth,**kwargs)
            for tree in m['trees']:
                trees.append(tree)
            for line in m['lines']:
                lines.append(line)
        else:
            int_depth=int(depths[0])
            tree=Tree(here,dt,l0,int_depth,tm,lm,**kwargs).svg(stroke_linecap="round")
            tree.rotate(degrees(t0+radians(90)),here.car)
            trees.append(tree)
            
    elif n==3:#if n//3==n/3:#?
        d0=depths[:1]#:n//3
        d1=depths[1:2]#n//3:2*n//3
        d2=depths[2:]#2*n//3:
        
        if depth==0:
            dx=lm.l**-f(depths)
        else:
            dx=1
        
        dep0=dx*lm.l**-((f(d0)-f([d1,d2]))/2+0.22)
        dep12=dx*lm.l**-((f([d1,d2])-f(d0))/2-0.28)
        dep1=lm.l**-((f(d1)-f(d2))/2+0.0)
        dep2=lm.l**-((f(d2)-f(d1))/2-0.12)
        
        l0=length*dep0*lm.r
        l12=length*dep12*lm.l
        #make left branches a tad shorter
        l12*=0.92
        
        #middle branch, i.e. left then right
        l1=l12*dep1*lm.r
        #left then left--leftmost branch
        l2=l12*dep2*lm.l
        
        ms=[]
        #curl right branches a tad more, left ones a bit more too
        dt*=Branch(1.08,1.08)
        
        #and make left left curl over more
        tm=Branch(Branch(tm.l.l+0.05,tm.l.r),tm.r)
        
        curves=Branch(((dt.r-dt.l)/2,dt.l*tm.l.l+(dt.r*tm.l.r-dt.l*tm.l.l)/2),\
            ((dt.l-dt.r)/2,dt.l*tm.r.l+(dt.r*tm.r.r-dt.l*tm.r.l)/2))
        
        
        loc=here+Vec2D(r=l0,t=t0+dt.r)#rightmost branch
        
        ms.append(metatree(loc,d0,l0,dt*tm.r,tm,lm,t0=t0+dt.r,depth=depth+1,**kwargs))
        lines.append(prettyline(here,loc,dt0=curves.r[0],dt1=curves.r[1],start_width=stroke_mult*(mymax(d0)+n//2),end_width=stroke_mult*(mymax(d0)+n//2-1),stroke=linecolor,stroke_width=2,fill='none',**kwargs))
        
        loc=here+Vec2D(r=l12,t=t0+dt.l)#first left branch
        lines.append(prettyline(here,loc,dt0=curves.l[0],dt1=curves.l[1],start_width=stroke_mult*(mymax([d1,d2])+n//2),end_width=stroke_mult*(mymax([d1,d2])+n//2-1),stroke=linecolor,stroke_width=2,fill='none',**kwargs))
        
        here=loc
        t0+=dt.l
        #t1*=thetamult[0][0]
        #t2*=thetamult[0][1]
        dt*=tm.l
        
        curves=Branch(((dt.r-dt.l)/2,dt.l*tm.l.l+(dt.r*tm.l.r-dt.l*tm.l.l)/2),\
            ((dt.l-dt.r)/2,dt.l*tm.r.l+(dt.r*tm.r.r-dt.l*tm.r.l)/2))
        
        loc=here+Vec2D(r=l1,t=t0+dt.r)
        ms.append(metatree(loc,d1,l1,dt*tm.r,tm,lm,t0=t0+dt.r,depth=depth+2,**kwargs))
        lines.append(prettyline(here,loc,dt0=curves.r[0],dt1=curves.r[1],start_width=stroke_mult*(mymax(d1)+n//2),end_width=stroke_mult*(mymax(d1)+n//2-1),stroke=linecolor,stroke_width=2,fill='none',**kwargs))
        
        loc=here+Vec2D(r=l2,t=t0+dt.l)
        ms.append(metatree(loc,d2,l2,dt*tm.l,tm,lm,t0=t0+dt.l,depth=depth+2,**kwargs))
        lines.append(prettyline(here,loc,dt0=curves.l[0],dt1=curves.l[1],start_width=stroke_mult*(mymax(d1)+n//2),end_width=stroke_mult*(mymax(d1)+n//2-1),stroke=linecolor,stroke_width=2,fill='none',**kwargs))
        
        
        for m in ms:
            for tree in m['trees']:
                trees.append(tree)
            for line in m['lines']:
                lines.append(line)
    else:
                       #reversed: not sure why.
        d1=depths[int(n/2):]
        d2=depths[:int(n/2)]
        if depth==0:
            d0=lm.l**-f(depths)
        else:
            d0=1
        dep1=d0*lm.l**-((f(d1)-f(d2))/2)
        dep2=d0*lm.l**-((f(d2)-f(d1))/2)
        ll=length*dep1*lm.l
        lr=length*dep2*lm.r
          
                       
        curves=Branch(((dt.r-dt.l)/2,dt.l*tm.l.l+(dt.r*tm.l.r-dt.l*tm.l.l)/2),\
            ((dt.l-dt.r)/2,dt.l*tm.r.l+(dt.r*tm.r.r-dt.l*tm.r.l)/2))
        
        ms=[]               
        loc=here+Vec2D(r=ll,t=t0+dt.l)
        #print("dt is ",type(dt),", tm.l is ",type(tm.l))
        #print(dt,tm.l,dt*tm.l)
        ms.append(metatree(loc,d1,ll,dt*tm.l,tm,lm,t0=t0+dt.l,depth=depth+1,**kwargs))
        #lines.append(svgwrite.shapes.Line(here.car,loc.car,stroke_width=mymax(d1)+n//2,stroke='red',stroke_linecap='round'))
        lines.append(prettyline(here,loc,dt0=curves.l[0],dt1=curves.l[1],start_width=(mymax(d1)+n//2)*stroke_mult,end_width=(mymax(d1)+n//2-1)*stroke_mult,stroke=linecolor,stroke_width=2,fill='none',**kwargs))
                       
        loc=here+Vec2D(r=lr,t=t0+dt.r)
        ms.append(metatree(loc,d2,lr,dt*tm.r,tm,lm,t0=t0+dt.r,depth=depth+1,**kwargs))
        lines.append(prettyline(here,loc,dt0=curves.r[0],dt1=curves.r[1],start_width=(mymax(d2)+n//2)*stroke_mult,end_width=(mymax(d2)+n//2)*stroke_mult,stroke=linecolor,stroke_width=2,fill='none',**kwargs))
        
        for m in ms:
            for tree in m['trees']:
                trees.append(tree)
            for l in m['lines']:
                lines.append(l)
    return({'trees':trees,'lines':lines})
