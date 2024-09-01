import svgwrite
#from papplet import *
from vec2d import *
import numpy as np
from copy import copy,deepcopy
from cprettypath import PrettyPath,_map,radians,degrees
from random import random,randint
debug=False
from time import sleep
import math

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
    l=property(itemgetter(0))
    r=property(itemgetter(1))

linecolor='green'

'''
LineLen=LineLen*[0.7,0.7]
T1,1 T2,1  = [   ]  #t1 given previousbranch is t1, t2 after a t1 branch
T1,2 T2,2    [   ]  #t1 after t2 branch, t2 after t2 branch
'''
stroke_mult=0.1
from random import gauss

def colerp(a,b,p):
    a=(a>>16,(a>>8)&0xff,a&0xff)
    b=(b>>16,(b>>8)&0xff,b&0xff)
    r=tuple(int(i+(j-i)*p+0.5) for i,j in zip(a,b))
    return (r[0]<<16)+(r[1]<<8)+r[2]

def cheaptaperedpath(start,theta0,theta1,end,startwidth,endwidth):
    """ given a start ray(x,y,theta) and an end ray,
        as well as start/end widths, construct an svg string which:
        is a filled path outlining the equivalent of a cubic spline between those two poiints
        but with a steadily tapering strokewidth
        """
    #encol=0x87b2ed
    #startcol=0x2c8f82
    #startcol=0x458a94
    #stcol=0x003f4b
    #stcol=0x0000ff
    '''encol=0x2c8f82 2c/45 8a/8f 94/82
    '''
    #z=[0,0.1,0.19,0.27,0.33,0.38,0.41,0.44,0.47,0.49,0.5,0.51,0.53,0.56,0.59,0.65,0.73,0.81,0.9,1]
    g=svgwrite.container.Group(debug=False)
        #for i in range(1,21):
        #sw=startwidth*(1-i/20)
        #ew=endwidth*(1-i/20)
        #fl='#'+hex(colerp(stcol,encol,i/20))[2:]
        #fl='#458a94'
        #fl='#3f7d86'
        #fl='#857aa3'
    fl='#0000ff'
    sw=startwidth
    ew=endwidth
    norm0=Vec2D(r=sw/2,t=theta0+math.pi/2)
    norm1=Vec2D(r=ew/2,t=theta1+math.pi/2)
    p0_0=start+norm0
    p0_1=start-norm0
    p3_0=end+norm1
    p3_1=end-norm1
    d=end-start
    d0=Vec2D(r=gauss(0.3,0.05)*d.r,t=theta0)
    p1_0=p0_0+d0
    p1_1=p0_1+d0
    d1=Vec2D(r=gauss(0.2,0.05)*d.r,t=theta1+math.pi)
    p2_0=p3_0+d1
    p2_1=p3_1+d1
        
        #radial gradient:
        #color1=pantone7474u=
        #startcol=0x458a94
        #tinybit darker
        #startcol=0x3f7d86
        #pantone 2249u
        #endcol=0x2c8f82
        #tinybit lighter
        #endcol=0x2e998b
            
    g.add(svgwrite.path.Path(d=['M',p0_0.car,'C',p1_0.car,p2_0.car,p3_0.car,'L',p3_1.car,'C',p2_1.car,p1_1.car,p0_1.car,'Z'],fill=fl,stroke='none',debug=False))
    return g
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
        #p=PrettyPath(start,Vec2D(1,0),0,0,tightness=1)
        #p.optimize(t0=t0,t1=t1,end=end,segs=5)
        kwargs['end_width']=end_width
        return cheaptaperedpath(start,t0,t1,end,start_width,end_width)
        #return p.taperedpath(5,start_width,**kwargs)
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
        self.gp=svgwrite.container.Group(debug=False,**args)
        #st=Vec2D(x=self.x,y=self.y)
        self._recur(self.gp,self.here,-self.size,radians(90),self.t,0)
        #gp.add(svgwrite.shapes.Line(start=st.car,end=(st+Vec2D(r=50,t=radians(90))).car,stroke_width=6,stroke='black'))
        return self.gp
    def _line(self,group,here,l,t,w,dt0=0,dt1=0):
        #group.add(svgwrite.shapes.Line(start=here.car,end=(here+Vec2D(r=l,t=t)).car,stroke='black',stroke_width=w))
        #group.add(prettyline(here,here+Vec2D(r=l,t=t),dt0=dt0,dt1=dt1,stroke=linecolor,start_width=w*stroke_mult,end_width=(w-1)*stroke_mult,fill=linecolor,render=self.render))
        group.add(prettyline(here,here+Vec2D(r=l,t=t),dt0=dt0,dt1=dt1,stroke=linecolor,start_width=stroke_mult*2**(w/2),end_width=stroke_mult*2**((w-1)/2),fill=linecolor,render=self.render))
        
    def _leaf(self,group,here,t,dt):
        if False:
            ss=2-random()*4
            se=2-random()*4
            ss,se=sorted((ss,se))
            es=4-random()*8
            ee=4-random()*8
            es,ee=sorted((es,ee))
            N=8
            for i in range(N+1):
                p=PrettyPath(here,Vec2D(r=t.r*(1.1-0.2*random()),t=t.t+_map(i,0,N,dt.l,dt.r)),_map(i,0,N,ss,se),_map(i,0,N,es,ee))
                tp=p.taperedpath(5,stroke='green',stroke_width=0,start_width=5,fill='green',debug=False)
            #tp=svgwrite.shapes.Ellipse(here.car,(2,4),fill='green')
            #tp.rotate(t.t,here.car)
                group.add(tp)
    def _recur(self,parent_group,here,line_length,t0,dt,depth):
        this_group=svgwrite.container.Group(debug=False)
        parent_group.add(this_group)
        
        if depth>=self.maxdepth:
            self._leaf(this_group,here,Vec2D(r=line_length*2,t=t0),dt)
            #self._leaf(this_group,here,Vec2D(r=line_length*2,t=t0+dt.r))
            return
        #length=[line_length *0.75,line_length *0.7]
        length=gauss(self.lm,0.01)*line_length
        
        
        #theta=[[t1,t2],[t1,t2]]*[0.8,0.9],[1,0.9]
        #theta = [[t1*0.8,t2*0.9],[t1,t2*0.9]]
        #theta=Branch(Branch(self.tm.l.l*dt.l,Branch(self.tm.l.r)*dt.r),Branch(self.tm.r.l*dt.l,self.tm.r.r*dt.r))
        theta=Branch(gauss(self.tm.l,0.03)*dt,gauss(self.tm.r,0.03)*dt)
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
        lines.append(prettyline(here,loc,dt0=curves.r[0],dt1=curves.r[1],start_width=stroke_mult*(mymax(d0)+n//2),end_width=stroke_mult*(mymax(d0)+n//2),stroke=linecolor,stroke_width=2,fill='green',**kwargs))
        
        loc=here+Vec2D(r=l12,t=t0+dt.l)#first left branch
        lines.append(prettyline(here,loc,dt0=curves.l[0],dt1=curves.l[1],start_width=stroke_mult*(mymax([d1,d2])+n//2),end_width=stroke_mult*(mymax([d1,d2])+n//2-1),stroke=linecolor,stroke_width=2,fill='green',**kwargs))
        
        here=loc
        t0+=dt.l
        #t1*=thetamult[0][0]
        #t2*=thetamult[0][1]
        dt*=tm.l
        
        curves=Branch(((dt.r-dt.l)/2,dt.l*tm.l.l+(dt.r*tm.l.r-dt.l*tm.l.l)/2),\
            ((dt.l-dt.r)/2,dt.l*tm.r.l+(dt.r*tm.r.r-dt.l*tm.r.l)/2))
        
        loc=here+Vec2D(r=l1,t=t0+dt.r)
        ms.append(metatree(loc,d1,l1,dt*tm.r,tm,lm,t0=t0+dt.r,depth=depth+2,**kwargs))
        lines.append(prettyline(here,loc,dt0=curves.r[0],dt1=curves.r[1],start_width=stroke_mult*(mymax(d1)+n//2),end_width=stroke_mult*(mymax(d1)+n//2-1),stroke=linecolor,stroke_width=2,fill='green',**kwargs))
        
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

from random import randint

def movetree(t,x,y):
    tfmlist=[[j[0],list(float(s) for s in j[1].split(','))] for j in [i.split('(') for i in t['transform'].split(')')[:-1]]]
    if tfmlist[0][0]=='translate':
        pos=tfmlist[1][1][1:]
        tfmlist[0][1]=(x-pos[0],y-pos[1])
        ret=[]
        for i in tfmlist:
            ret.append('('.join((i[0],','.join(str(s) for s in i[1]))))
        t['transform']=')'.join(ret+[''])
    else:
        pos=tfmlist[0][1][1:]
        t['transform']='translate('+str(x-pos[0])+','+str(y-pos[1])+') '+t['transform']
def selectree(t):
    print('TREE SELECTED')
'''
class sketch(PApplet):
    def __init__(self,**args):
        super().__init__(**args)
        #self.theta=[[0.7,0.85],[1.05,0.85]]
        #self.theta=Branch(Branch(0.7,0.85),Branch(1.05,0.85))
        self.theta=Branch(Branch(0.73,0.87),Branch(1.05,0.97))
        self.count=0
        self.length=Branch(0.79,0.69)
        #self.length=[0.8,0.65]
        self.t1=radians(-29)
        self.t2=radians(75)
        self.render=False
        self.density=4
        self._depth=30
        self.selectables=[]
        self.selected=None
    def setup(self):
        start=Vec2D(self.width*0.6,self.height*0.6)
        Trees=[]
        
        
        #x=['red algae',['green algae',['charalians',['mosses','liverworts','hornworts',['lycophytes',['ferns&horsetails',['cycads','conifers',['Amborella',['water lillies',[[[['rosids','asterids','cacti'],'poppies'],['laurels','magnolias']],['lillies','orchids',['palms','grasses']]]]]]]]]]]]
        subtrees={'chordata':[2]*20,'slimythings':[2]*18,'insects':[5]*24,'fungi, mold, sponges':[3]*18,'plants':[3]*22,'bacteria,archaea,etc':[4]*29}
        x=[self.density]*(self._depth)
        
        #or just split it up reasonably equally, and connect the dots.
        #20+18+24+18+22+29=26ish.
        #we could do five domains: animals, fungi, plants, protists, and bacteria?
        theta=Branch(Branch(0.68+random()*0.05,0.83+random()*0.05),Branch(1.05,0.75+random()*0.25))
        length=Branch(0.79+random()*0.02,0.63+random()*0.07)
        m=metatree(start,x,50,Branch(self.t1+radians(randint(-3,3)),self.t2+radians(randint(-5,5))),theta,length,render=self.render)
        
        for t in m['trees']:
            self.dwg.add(t)
            pos=tuple(float(s) for s in t['transform'][7:-1].split(',')[1:])
            self.selectables.append({'selectionbox':(pos[0]+10,pos[1]+10,pos[0]-10,pos[1]-10),'object':t,'callback':movetree,'select_callback':selectree})
        #for l in m['lines']:
        #    self.dwg.add(l)
        self.dwg.add(svgwrite.text.Text('TreeDensity:'+str(self.density),insert=(50,500),font_size=30,stroke='black'))
        self.dwg.add(svgwrite.text.Text('TreeDepth:'+str(self._depth),insert=(50,550),font_size=30,stroke='black'))
    def draw(self):
        #self.dwg.add(svgwrite.text.Text('LineMult:'+str(self.length),insert=(50,500),font_size=30,stroke='black'))
        #self.dwg.add(svgwrite.text.Text('ThetaMul:'+str(self.theta),insert=(50,550),font_size=30,stroke='black'))
        pass
    def on_mousedown(self):
        for selectable in self.selectables:
            if is_in(self.mouseX,self.mouseY,selectable['selectionbox']):
                self.selected=selectable
                selectable['select_callback'](selectable['object'])
            
    def mousemove(self):
        if self.mousedown:
            self.selected['callback'](self.selected['object'],self.mouseX,self.mouseY)
    def on_keypress(self):
        if chr(self.keydown)=='q':
            self.theta=Branch(Branch(self.theta.l.l+0.01,self.theta.l.r),Branch(self.theta.r.l,self.theta.r.r))
        elif chr(self.keydown)=='a':
            self.theta=Branch(Branch(self.theta.l.l-0.01,self.theta.l.r),Branch(self.theta.r.l,self.theta.r.r))
        elif chr(self.keydown)=='w':
            self.theta=Branch(Branch(self.theta.l.l,self.theta.l.r+0.01),Branch(self.theta.r.l,self.theta.r.r))
        elif chr(self.keydown)=='s':
            self.theta=Branch(Branch(self.theta.l.l,self.theta.l.r-0.01),Branch(self.theta.r.l,self.theta.r.r))
        elif chr(self.keydown)=='e':
            self.theta=Branch(Branch(self.theta.l.l,self.theta.l.r),Branch(self.theta.r.l+0.01,self.theta.r.r))
        elif chr(self.keydown)=='d':
            self.theta=Branch(Branch(self.theta.l.l,self.theta.l.r),Branch(self.theta.r.l-0.01,self.theta.r.r))
        elif chr(self.keydown)=='r':
            self.theta=Branch(Branch(self.theta.l.l,self.theta.l.r),Branch(self.theta.r.l,self.theta.r.r+0.01))
        elif chr(self.keydown)=='f':
            self.theta=Branch(Branch(self.theta.l.l,self.theta.l.r),Branch(self.theta.r.l,self.theta.r.r-0.01))
        elif chr(self.keydown)=='u':
            self.length=Branch(self.length.l+0.01,self.length.r)
        elif chr(self.keydown)=='j':
            self.length=Branch(self.length.l-0.01,self.length.r)
        elif chr(self.keydown)=='i':
            self.length=Branch(self.length.l,self.length.r+0.01)
        elif chr(self.keydown)=='k':
            self.length=Branch(self.length.l,self.length.r-0.01)
        elif chr(self.keydown)=='z':
            self.render=True
        elif chr(self.keydown)=='t':self.density+=1
        elif chr(self.keydown)=='g':self.density-=1
        elif chr(self.keydown)=='y':self._depth+=1
        elif chr(self.keydown)=='h':self._depth-=1
from IPython.display import SVG

import cProfile
'''
#s=sketch(height=1800,width=2600)
#svg=[]

'''cProfile.run('''
'''for i in range(5):
    s._draw()
    g=svgwrite.container.Group(debug=False)
    g.add(s.dwg)
    g.translate((0,-500))
    g.rotate(72*i,(2600*0.6,1800*0.6))
    
    svg.append(g.tostring())
'''''')
import os
export=['fiverandom','.svg']
i=1
while os.path.isfile(export[0]+str(i)+export[1]):
    i+=1
with open(export[0]+str(i)+export[1],'w') as f:
    f.write('<svg>'+'\n'.join(svg)+'</svg>')

'''

#s.start()
