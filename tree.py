import importlib,sys
for m in ['papplet','vec2d','prettypath','svgwrite']:
    if m in sys.modules.keys():
        importlib.reload(sys.modules[m]) 
import svgwrite
from papplet import PApplet
from vec2d import *
import numpy as np
from copy import copy,deepcopy
from prettypath import PrettyPath,_map
from random import random,randint
debug=False
from time import sleep
import math

'''
LineLen=LineLen*[0.7,0.7]
T1,1 T2,1  = [   ]  #t1 given previousbranch is t1, t2 after a t1 branch
T1,2 T2,2    [   ]  #t1 after t2 branch, t2 after t2 branch
'''


class Tree():
    def __init__(self,x,y,theta1,theta2,size,depth,thetamult,lenmult):
        self.t1=theta1
        self.t2=theta2
        self.maxdepth=depth
        self.size=size
        self.tm=thetamult
        self.lenmult=lenmult
        self.x=x
        self.y=y
    def svg(self,**args):
        self.gp=svgwrite.container.Group(**args)
        st=Vec2D(x=self.x,y=self.y)
        self._recur(self.gp,st,-self.size,radians(90),self.t1,self.t2,0)
        return self.gp
    def _line(self,group,here,l,t,w):
        group.add(svgwrite.shapes.Line(start=here.car,end=(here+Vec2D(r=l,t=t)).car,stroke='black',stroke_width=w))
    def _leaf(self,group,here,t):
        ss=2-random()*4
        se=2-random()*4
        ss,se=sorted((ss,se))
        es=4-random()*8
        ee=4-random()*8
        es,ee=sorted((es,ee))
        for i in range(4):
            p=PrettyPath(here,t,_map(i,0,3,ss,se),_map(i,0,3,es,ee))
            tp=p.taperedpath(5,stroke='green',stroke_width=0,start_width=2,fill='green',debug=debug)
        #tp=svgwrite.shapes.Ellipse(here.car,(2,4),fill='green')
        #tp.rotate(t.t,here.car)
            group.add(tp)
    def _recur(self,parent_group,here,line_length,t,t1,t2,depth,extra_branch=True):
        this_group=svgwrite.container.Group(debug=debug)
        parent_group.add(this_group)
        
        if depth>=self.maxdepth:
            self._leaf(this_group,here,Vec2D(r=line_length*2,t=t))
            self._leaf(this_group,here,Vec2D(r=line_length*2,t=t))
            return
        #length=[line_length *0.75,line_length *0.7]
        length=[line_length*self.lenmult[0],line_length*self.lenmult[1]]
        
        
        #theta=[[t1,t2],[t1,t2]]*[0.8,0.9],[1,0.9]
        #theta = [[t1*0.8,t2*0.9],[t1,t2*0.9]]
        theta=[[t1*self.tm[0][0],t2*self.tm[0][1]],[t1*self.tm[1][0],t2*self.tm[1][1]]]
        d=Vec2D(x=0,y=0)
        dt=0
        if extra_branch or depth<5:
            self._line(this_group,here,length[0],t+t1,self.maxdepth+1-depth)
            self._recur(this_group,here+Vec2D(r=length[0],t=t+t1),length[0],t+t1,theta[0][0],theta[0][1],depth+1,extra_branch=extra_branch)
            self._line(this_group,here,length[1],t+t2,self.maxdepth+1-depth)
            d=Vec2D(r=length[1],t=t+t2)
            dt=t2
        self._recur(this_group,here+d,length[1],t+dt,theta[1][0],theta[1][1],depth+1,extra_branch=extra_branch)
        
        if False:
            h=here+Vec2D(r=length[0]/2,t=t+t1)
            d=Vec2D(r=length[1]*self.lenmult[1]**2,t=t+t1+theta[0][1]*1.1)
            self._line(this_group,h,d.r,d.t,self.maxdepth-depth)
            self._recur(this_group,h+d,d.r,d.t,theta[1][0]*self.tm[1][0],theta[1][1]*self.tm[1][1],depth+2 if depth>=self.maxdepth-4 else self.maxdepth-4,extra_branch=False)
        #self._recur(here+Vec2D(r=length[1]/2,t=t+t2),length[1],t+t2,theta[1][0],theta[1][1],depth+2)
    #degx~=-24 degy~=68
def linetree(here,depths,length,t1,t2,thetamult,linemult,t=radians(-90)):
    trees=[]
    lines=[]
    n=len(depths)
    #t=radians(-90)
    i=0
    if n==2:
        delt=Vec2D(r=length*linemult[0],t=t+t1)
        #delt.y=-delt.y
        loc=here+delt
        lines.append(svgwrite.shapes.Line(here.car,loc.car,stroke_width=max(depths)+1,stroke='black',stroke_linecap='round'))
        tree=Tree(loc.x,loc.y,t1*thetamult[0][0],t2*thetamult[0][1],length*linemult[0],depths[0],thetamult,linemult).svg()
        tree.rotate(degrees(t1+t+radians(90)),loc.car)
        trees.append(tree)
        delt=Vec2D(r=length*linemult[1],t=t+t2)
        #delt.y=-delt.y
        loc=here+delt
        lines.append(svgwrite.shapes.Line(here.car,loc.car,stroke_width=max(depths)+1,stroke='black',stroke_linecap='round'))
        tree=Tree(loc.x,loc.y,t1*thetamult[1][0],t2*thetamult[1][1],length*linemult[1],depths[1],thetamult,linemult).svg()
        tree.rotate(degrees(t2+t+radians(90)),loc.car)
        trees.append(tree)
    elif n>2:
        d1=depths[:n//2]
        d2=depths[n//2:]
        loc=here+Vec2D(r=length*linemult[0],t=t+t1)
        m1=linetree(loc,d1,length*linemult[0],t1*thetamult[0][0],t2*thetamult[0][1],thetamult,linemult,t=t+t1)
        lines.append(svgwrite.shapes.Line(here.car,loc.car,stroke_width=max(d1)+n//2,stroke='black',stroke_linecap='round'))
        for tree in m1['trees']:
            #tree.rotate(degrees(t1),loc.car)
            trees.append(tree)
        for l in m1['lines']:
            #l.rotate(t1,loc.car)
            lines.append(l)
        loc=here+Vec2D(r=length*linemult[1],t=t+t2)
        m2=linetree(loc,d2,length*linemult[1],t1*thetamult[1][0],t2*thetamult[1][1],thetamult,linemult,t=t+t2)
        lines.append(svgwrite.shapes.Line(here.car,loc.car,stroke_width=max(d2)+n//2,stroke='black',stroke_linecap='round'))
        for tree in m2['trees']:
            #tree.rotate(degrees(t2),loc.car)
            trees.append(tree)
        for l in m2['lines']:
            #l.rotate(t1,loc.car)
            lines.append(l)
    return({'trees':trees,'lines':lines})
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
def f(l):

    '''oh god, i dont know its too late trust me it does something important and clever'''
    a=0        
    for i in flatten(l):
        a+=2**i
    return math.log2(a)

def mymax(x):
    return max(flatten(x))
def metatree(here,depths,length,t1,t2,thetamult,linemult,t=radians(-90),depth=0):
    
    #print("metatree: depth=",depth,"length:",length)
    trees=[]
    lines=[]
    n=len(depths)
    #t=radians(-90)
    i=0
    #length=length/(linemult[0]**(f(depths)-4))
    if n==1:
        
        if depth!=0:
            l0=length
        else:
            l0=length*linemult[0]**(-depths[0])
        #print("new length:",length)
        #elif depth==2:
        #    l0=length*math.sqrt(linemult[0]*linemult[1])**(-depths[0])
        
        if isinstance(depths[0],(list,tuple)):
            m=metatree(here,depths[0],l0,t1,t2,thetamult,linemult,t=t,depth=depth)
            for tree in m['trees']:
                #tree.rotate(degrees(t+radians(90)),here.car)
                trees.append(tree)
            for line in m['lines']:
                lines.append(line)
        else:
            tree=Tree(here.x,here.y,t1,t2,l0,depths[0],thetamult,linemult).svg(stroke_linecap="round")
            tree.rotate(degrees(t+radians(90)),here.car)
            trees.append(tree)
#    elif n==2:
#        l1=length*linemult[0]**(4-f(depths[:1]))
#        l2=length*linemult[1]**(4-f(depths[1:]))
#        delt=Vec2D(r=l1*linemult[0],t=t+t1)
#        #delt.y=-delt.y
#        loc=here+delt
#        lines.append(svgwrite.shapes.Line(here.car,loc.car,stroke_width=max(depths)+1,stroke='red'))
#        tree=Tree(loc.x,loc.y,t1*thetamult[0][0],t2*thetamult[0][1],l1*linemult[0],depths[0],thetamult,linemult).svg()
#        tree.rotate(degrees(t1+t+radians(90)),loc.car)
#        trees.append(tree)
#        delt=Vec2D(r=l2*linemult[1],t=t+t2)
        #delt.y=-delt.y
#        loc=here+delt
#        lines.append(svgwrite.shapes.Line(here.car,loc.car,stroke_width=max(depths)+1,stroke='red'))
#        tree=Tree(loc.x,loc.y,t1*thetamult[1][0],t2*thetamult[1][1],l2*linemult[1],depths[1],thetamult,linemult).svg()
#        tree.rotate(degrees(t2+t+radians(90)),loc.car)
#        trees.append(tree)
    #elif n//3==n/3:
    #    d0=depths[:n//3]
    #    d1=depths[n//3:2*n//3]
    #    d2=depths[2*n//3:]
    else:
        d1=depths[int(n/2):]
        d2=depths[:int(n/2)]
        if depth==0:
            dep1=linemult[0]**-(f(depths)+(f(d1)-f(d2))/2)
            dep2=linemult[0]**-(f(depths)+(f(d2)-f(d1))/2)
        else:
            dep1=linemult[0]**-((f(d1)-f(d2))/2)
            dep2=linemult[0]**-((f(d2)-f(d1))/2)
        l1=length*dep1*linemult[0]
        l2=length*dep2*linemult[1]
        #print("new lengths:",l1,l2)
        #t1+=(max(d1)-4)*radians(-5)
        #t2+=(max(d2)-4)*radians(5)
        loc=here+Vec2D(r=l1,t=t+t1)
        m1=metatree(loc,d1,l1,t1*thetamult[0][0],t2*thetamult[0][1],thetamult,linemult,t=t+t1,depth=depth+1)
        lines.append(svgwrite.shapes.Line(here.car,loc.car,stroke_width=mymax(d1)+n//2,stroke='red',stroke_linecap='round'))
        for tree in m1['trees']:
            #tree.rotate(degrees(t1),loc.car)
            trees.append(tree)
        for l in m1['lines']:
            #l.rotate(t1,loc.car)
            lines.append(l)
        loc=here+Vec2D(r=l2,t=t+t2)
        m2=metatree(loc,d2,l2,t1*thetamult[1][0],t2*thetamult[1][1],thetamult,linemult,t=t+t2,depth=depth+1)
        lines.append(svgwrite.shapes.Line(here.car,loc.car,stroke_width=mymax(d2)+n//2,stroke='red',stroke_linecap='round'))
        for tree in m2['trees']:
            #tree.rotate(degrees(t2),loc.car)
            trees.append(tree)
        for l in m2['lines']:
            #l.rotate(t1,loc.car)
            lines.append(l)
    return({'trees':trees,'lines':lines})
    
    
    
class sketch(PApplet):
    def __init__(self,**args):
        super().__init__(**args)
        self.theta=[[0.7,0.85],[1.05,0.85]]
        self.length=[0.8,0.65]
        self.t1=radians(-29)
        self.t2=radians(75)
        self.one=False
    def draw(self):
        start=Vec2D(self.width*0.6,self.height*0.6)
        Trees=[]
        here=start
        delt=Vec2D(150,0)
        m=metatree(start,[5,5,5,5,5,4,4,4,4,4,4,4,4,4,4,4,4,4,4,5,4,4],40,self.t1,self.t2,self.theta,self.length)
        for t in m['trees']:
           self.dwg.add(t)
        for l in m['lines']:
           self.dwg.add(l)
           
        for i in range(0):
            if i/2==i//2:
                here-=Vec2D(0,300)
            else:
                here+=Vec2D(0,300)
            s=210
            d=7
            Trees.append(Tree(here.x,here.y,self.t1,self.t2,s,d,self.theta,self.length))
            svg=Trees[i].svg()
            svg.rotate(30+random()*0-5 if i/2==i//2 else -200+random()*0-5,here.car)
            if i/2!=i//2:
                svg.scale(-1,1)
                svg.translate(-(here.x*2),0)
            
            line=svgwrite.shapes.Line((here.x-200,here.y+ ( 150 if i/2==i//2 else -150)),here.car,stroke_width=8,stroke='black')
            self.dwg.add(line)
            self.dwg.add(svg)
            here+=delt
        #entreline=svgwrite.shapes.Line((start.x-200,start.y-150),(start+delt*10-Vec2D(-200,150)).car,stroke_width=8,stroke="black")
        #elf.dwg.add(centreline)
        
        
        
        #t1=Tree(start.x,start.y,self.t1,self.t2,100,5,self.theta,self.length)
        #t2=Tree(start.x,start.y,self.t1,self.t2,100,5,self.theta,self.length)
        #t3=Tree(start.x,start.y,self.t1,self.t2,300,8,self.theta,self.length)
        #degx=(self.mouseX/self.width-0.5)*360
        #degy=(self.mouseY/self.height-0.5)*360
        degx=degrees(self.t1)
        degy=degrees(self.t2)-15
        threedeg=(self.mouseX/self.width-0.5)*360
        dy=300
        threer=(self.mouseY/self.height)*300+200
        #self.dwg.add(svgwrite.shapes.Line(start=start.car,end=(start.x,start.y-dy),transform='rotate('+str(degx)+','+str(start.x)+','+str(start.y)+')',stroke_width=8,stroke='black'))
        #self.dwg.add(svgwrite.shapes.Line(start=start.car,end=(start.x,start.y-200),transform='rotate('+str(degy)+','+str(start.x)+','+str(start.y)+')',stroke_width=8,stroke='black'))
        #self.dwg.add(t2.svg(transform="translate(0,-"+str(dy)+") rotate("+str(degx)+","+str(start.x)+","+str(start.y+dy)+")"))
        #self.dwg.add(t1.svg(transform="translate(0,-"+str(200)+") rotate("+str(degy)+","+str(start.x)+","+str(start.y+200)+")",debug=debug))
        #self.dwg.add(t3.svg(transform="translate(0,-"+str(threer)+") rotate("+str(threedeg)+","+str(start.x)+","+str(start.y+threer)+")",debug=debug))
        #s=(self.mouseX/self.width - 0.5)*20
        
        
        
        #e=(self.mouseY/self.height - 0.5)*20
        
        #self.p=PrettyPath(start,Vec2D(r=500,t=radians(-90)),s,e)
        #ap=self.p.arcpath(10,stroke='black',stroke_width=1,fill='none')
        #print(ap,type(ap))
        #assert(False)
        #self.dwg.add(ap)
        #ap2=deepcopy(ap)
        #width=20
        #width=2*||end-start||sin(t/2)
        #width/(2*||end-start||)=sin(t/2)~=t/2 t=width/|end-start|
        #d=self.p.end-self.p.start
        #print(d.pol)
        #assert(False)
        #ap2.rotate(degrees(width/abs(d.r)),self.p.end.car)
        #self.dwg.add(ap2)
        #self.p.c0=s
        #self.p.c1=e
        #tp=self.p.taperedpath(5,stroke='black',stroke_width=2,start_width=100,fill='green')
        #self.dwg.add(tp)
        #mouse=svgwrite.text.Text("Theta0:"+str(degrees(self.p.pathpoints(5)[0][2].t)),insert=(50,900),fill='black',font_size=30)
        #self.dwg.add(mouse)
        #key1=svgwrite.text.Text("Radius:"+str(threer),insert=(50,950),fill='black',font_size=30)
        #key2=svgwrite.text.Text("Theta:"+str(threedeg),insert=(50,850),fill='black',font_size=30)
        #self.dwg.add(key1)
        #self.dwg.add(key2)
    def on_keypress(self):
        if chr(self.keydown)=='q':
            self.theta[0][0]+=0.05
        elif chr(self.keydown)=='a':
            self.theta[0][0]-=0.05
        elif chr(self.keydown)=='w':
            self.theta[0][1]+=0.05
        elif chr(self.keydown)=='s':
            self.theta[0][1]-=0.05
        elif chr(self.keydown)=='e':
            self.theta[1][0]+=0.05
        elif chr(self.keydown)=='d':
            self.theta[1][0]-=0.05
        elif chr(self.keydown)=='r':
            self.theta[1][1]+=0.05
        elif chr(self.keydown)=='f':
            self.theta[1][1]-=0.05
        elif chr(self.keydown)=='u':
            self.length[0]+=0.01
        elif chr(self.keydown)=='j':
            self.length[0]-=0.01
        elif chr(self.keydown)=='i':
            self.length[1]+=0.01
        elif chr(self.keydown)=='k':
            self.length[1]-=0.01

from IPython.display import SVG
import subprocess
svg=''
import cProfile

s=sketch(height=1800,width=2600)
#s._draw()
#cProfile('''subprocess.call(pypy )
#svg=s.dwg.tostring()
#SVG(svg)l=[1,[2,3],'a']




s.start()
#svg
