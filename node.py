from cprettypath import radians,degrees,_map
import math as np
from vec2d import Vec2D
class Spring():
    def __init__(self,fr,to,**kwargs):
        self.fr=fr
        self.to=to
        self.k=kwargs.pop('k',2)
        self.l=kwargs.pop('l',1)
        self.c=kwargs.pop('c',2)#times m
    def __repr__(self):
        return "Spr("+str(hex(id(self)))+" fr:"+str(hex(id(self.fr)))+",to:"+str(hex(id(self.to)))+")"
def diff(t1,t2):
    diff=(t1-t2)%(2*np.pi)
    if diff>np.pi:
        diff-=2*np.pi
    if diff<-np.pi:
        diff+=2*np.pi
    return diff

class Node():
    def __repr__(self):
        return("Node("+str(hex(id(self)))+")")
    def __init__(self,here,**kwargs):
        self.here=here
        self.parent=kwargs.pop('parent',None)
        self.children=[]
        self.mass=kwargs.pop('mass',1)
        self.vel=Vec2D(0,0)
        self.acc=Vec2D(0,0)
        self.root=kwargs.pop('root')
        self.fixed=kwargs.pop('fixed',False)
        self.theta={}
        self.tr=kwargs.pop('tr',radians(40))
        self.tl=kwargs.pop('tl',radians(-20))
    def add_child(self,loc,**kwargs):
        newnode=Node(root=self.root,here=loc)
        newspring=Spring(self,newnode,**kwargs)
        #now update parent
        newnode.parent=(self,newspring)
        newnode.root=self.root
        self.children.append((newnode,newspring))
        #decide where we want them to be.
        if len(self.children)>1:
            for i in range(len(self.children)):
                self.theta[self.children[i][0]]=_map(i,0,len(self.children)-1,self.tr,self.tl)
        else:
            self.theta[self.children[0][0]]=self.tl#if there's just one child,passempandeleftanside
        #return (newnode,newspring)
        self.root.nodelist.append(newnode)
        self.root.springlist.append(newspring)
    def forces(self):
        F=Vec2D(0,0)
        if self.parent!=None:
            nodes=[self.parent]+self.children
        else:
            nodes=self.children
        for nd,spr in nodes:
            x=(nd.here-self.here)
            x.r=x.r-spr.l
            #print("x=",x)
            v=(self.vel-nd.vel).proj((nd.here-self.here))
            #v=self.vel
            #print("v=",v)
            F+=spr.k*x-spr.c*v
        #couloumb repulsionshit i dont care about the root, i need a list of all the nodes.
        C=Vec2D(0,0)
        for nd in self.root.nodelist:
            if nd!=self:
                x=(nd.here-self.here)
                x.r=-self.root.C*self.mass*nd.mass/(x.r*x.r)
                C+=x
        if C.r>200:#if deltat is too large, this can be very large
            C.r=200*np.atan(np.pi*C.r/400)
        F+=C
        #friction
        F+=-0.2*self.vel
        #torque with respect to parent
        if self != self.root:
            if self.parent[0] != self.root:
                t0=(self.parent[0].here-self.parent[0].parent[0].here).t
            else:
                t0=radians(-90)
                #children should be spread out between tr and tl
            tang=(self.here-self.parent[0].here)
            tgoal=(t0+self.parent[0].theta[self])#%(2*np.pi)
            #tdelt=diff(tgoal,tang.t)#parent knows where we should be
            tdelt=diff(tang.t,tgoal)
            #tv.car=(-tv.y,tv.x)#rotate -90, (same as (x,y)->(-y,x))
            tang.rotate(radians(-90))
            w=(self.vel-self.parent[0].vel).dot(tang)/(tang.dot(tang))*tang.r
            #w=(self.vel-self.parent[0].vel).proj(tang)#component in the tangent direction times r
            k=2000
            c=100
            
            T=k*tdelt-c*w#torque exerted by parent
            F+=Vec2D(r=T/tang.r,t=tang.t)
            #print('x',self.here,'parent',self.parent[0].here)
            #print('torque on',self,Vec2D(r=T/tv.r,t=tv.t))
        #print('total F on',self,F)
        if F.r>400:
            F.r=400*np.atan(np.pi*F.r/800)
        self.acc=F*(1/self.mass)
    
    def move(self,dt):
        if not self.fixed:
            self.forces()#update acceleration
            self.here+=self.vel*dt+self.acc*dt*dt*0.5
            self.vel+=self.acc*dt
        
class Root(Node):
    def __init__(self,here,**kwargs):
        super().__init__(here,root=self,**kwargs)
        self.nodelist=[self]
        self.springlist=[]
        self.C=kwargs.pop('C',10000)
    def add_child(self,loc,**kwargs):
        newnode=Node(root=self,here=loc)
        newspring=Spring(self,newnode,**kwargs)
        #now update parent
        newnode.parent=(self,newspring)
        newnode.root=self
        self.children.append((newnode,newspring))
        self.nodelist.append(newnode)
        self.springlist.append(newspring)
        #return (newnode,newspring)
        #decide where we want them to be.
        if len(self.children)>1:
            for i in range(len(self.children)):
                self.theta[self.children[i][0]]=_map(i,0,len(self.children)-1,self.tr,self.tl)
        else:
            self.theta[self.children[0][0]]=self.tl#if there's just one child,passempandeleftanside

    def move(self,dt):
        super().move(dt)
        for nd in self.nodelist[1:]:#not including the root, or infinite loop
            nd.move(dt)    
