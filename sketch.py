import importlib,sys
for m in ['papplet','vec2d','prettypath']:
    if m in sys.modules.keys():
        importlib.reload(sys.modules[m]) 
#sys.path.insert(0,'/usr/lib/python3.4/site-packages/svgwrite')
import svgwrite
from papplet import PApplet
from vec2d import *
import math as np
from copy import copy,deepcopy
from prettypath import PrettyPath,_map
from random import random

debug=False
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
    def svg(self,**kwargs):
        self.gp=svgwrite.container.Group(**kwargs)
        st=Vec2D(x=self.x,y=self.y)
        self._recur(st,-self.size,radians(90),self.t1,self.t2,0)
        #gp.add(svgwrite.shapes.Line(start=st.car,end=(st+Vec2D(r=50,t=radians(90))).car,stroke_width=6,stroke='black'))
        return self.gp
    def _line(self,here,l,t,w):
        self.gp.add(svgwrite.shapes.Line(start=here.car,end=(here+Vec2D(r=l,t=t)).car,stroke='black',stroke_width=w,debug=debug))
    def _leaf(self,here,t):
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
            self.gp.add(tp)
    def _recur(self,here,line_length,t,t1,t2,depth):
        if depth>=self.maxdepth:
            self._leaf(here,Vec2D(r=line_length*2,t=t))
            self._leaf(here,Vec2D(r=line_length*2,t=t))
            return
        #length=[line_length *0.75,line_length *0.7]
        length=[line_length*self.lenmult[0],line_length*self.lenmult[1]]
        
        self._line(here,length[0],t+t1,self.maxdepth+1-depth)
        
        #theta=[[t1,t2],[t1,t2]]*[0.8,0.9],[1,0.9]
        #theta = [[t1*0.8,t2*0.9],[t1,t2*0.9]]
        theta=[[t1*self.tm[0][0],t2*self.tm[0][1]],[t1*self.tm[1][0],t2*self.tm[1][1]]]
        
        self._recur(here+Vec2D(r=length[0],t=t+t1),length[0],t+t1,theta[0][0],theta[0][1],depth+1)
        self._line(here,length[1],t+t2,self.maxdepth+1-depth)
        self._recur(here+Vec2D(r=length[1],t=t+t2),length[1],t+t2,theta[1][0],theta[1][1],depth+1)
        
    #degx~=-24 degy~=68

class sketch(PApplet):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.theta=[[0.7,0.85],[1.05,0.85]]
        self.length=[0.8,0.65]
        self.t1=radians(-28)
        self.t2=radians(75)
        #self.p=PrettyPath(Vec2D(self.width/2,self.height*0.7),Vec2D(r=800,t=radians(-90)),1,1)
    def draw(self):
        #t1=Tree((self.mouseX/self.width-0.5)*2*np.pi,(self.mouseY/self.height-0.5)*2*np.pi,200,9,self.theta,self.length)
        #t2=Tree((self.mouseX/self.width-0.5)*2*np.pi,(self.mouseY/self.height-0.5)*2*np.pi,100,8,self.theta,self.length)
        start=Vec2D(self.width/2,self.height*0.7)
        
        t1=Tree(start.x,start.y,self.t1,self.t2,200,7,self.theta,self.length)
        #t2=Tree(start.x,start.y,self.t1,self.t2,200,8,self.theta,self.length)
        #degx=(self.mouseX/self.width-0.5)*360
        #degy=(self.mouseY/self.height-0.5)*360
        degx=degrees(self.t1)
        degy=degrees(self.t2)-15
        dy=300
        self.dwg.add(svgwrite.shapes.Line(start=start.car,end=(start.x,start.y-dy),transform='rotate('+str(degx)+','+str(start.x)+','+str(start.y)+')',stroke_width=8,stroke='black'))
        self.dwg.add(svgwrite.shapes.Line(start=start.car,end=(start.x,start.y-200),transform='rotate('+str(degy)+','+str(start.x)+','+str(start.y)+')',stroke_width=8,stroke='black'))
        #self.dwg.add(t2.svg(transform="translate(0,-"+str(dy)+") rotate("+str(degx)+","+str(start.x)+","+str(start.y+dy)+")"))
        self.dwg.add(t1.svg(transform="translate(0,-"+str(200)+") rotate("+str(degy)+","+str(start.x)+","+str(start.y+200)+")"))
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
        #key1=svgwrite.text.Text("Straights:"+str(self.p.straights),insert=(50,950),fill='black',font_size=30)
        key2=svgwrite.text.Text("Len-mult:"+str(self.length),insert=(50,850),fill='black',font_size=30)
        #self.dwg.add(key1)
        self.dwg.add(key2)
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

#from IPython.display import SVG

svg=''
import cProfile
s=sketch(height=1200,width=1800)
s._draw()
cProfile.run('''
svg=s.dwg.tostring()
#xml=s.dwg.get_xml()
#SVG(svg)
''')
#s.start()

import timeit

#print (timeit.timeit('svg=s.dwg.tostring','from __main__ import svg,s',number=100))
