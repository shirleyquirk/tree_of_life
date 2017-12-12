import importlib,sys
for m in ['vec2d','cprettypath','papplet']:
    if m in sys.modules.keys():
        importlib.reload(sys.modules[m])
from vec2d import *
from cprettypath import radians
import math as np
import subprocess
import xml.etree.ElementTree as etree
from cprettypath import PrettyPath,get_point
class TextPath():
    def __init__(self,text,start_width,end_width,path,segs):
        self.text=text
        self.sw=start_width
        self.ew=end_width
        self.path=path
        self.segs=segs
    def text_to_svg(self):
        with open('/tmp/text.svg','w') as f:
            f.write('<svg><text font-size="20px" font-family="Vim SM">'+self.text+'</text></svg>')  
        r=subprocess.run(['/usr/bin/inkscape','-ST','/tmp/text.svg','-l','/tmp/text.svg'],stdout=subprocess.PIPE,universal_newlines=True)

        height=float(r.stdout.split('\n')[1].split(',')[4])
        width=float(r.stdout.split('\n')[1].split(',')[3])
        #self.path.t0.r=1+width*self.sw*(np.exp((self.ew-self.sw)/height*(1))-1)/(self.ew-self.sw)

        
        textpaths=etree.parse('/tmp/text.svg').getroot()[2]
        paths=[]
        for path in textpaths:
            paths.append([[float(j) for j in i.split(',')] if (',' in i) else i for i in path.get('d').split(' ')])
        #separates paths into a command list
        
        #print(paths)    
        for k in range(len(paths)):
            here=[0,0]
            prev=[0,0]
            subpath_start=[0,0]
            curve=False
            moveto=False
            clozed=False
            curvei=0
            for i in range(len(paths[k])):
                if isinstance(paths[k][i],list):#means a relative (x,y)
                    if absolute:
                        here[0]=paths[k][i][0]
                        here[1]=paths[k][i][1]
                    else:
                        here[0]=prev[0]+paths[k][i][0]
                        here[1]=prev[1]+paths[k][i][1]
                    paths[k][i]=self.do_transform(here,height,width)
                    paths[k][i]=','.join(str(j) for j in paths[k][i])
                    if curve:#we're parsing a bezier point
                        curvei=curvei+1
                        if curvei==3:#the destination of the curve
                            prev[0]=here[0]
                            prev[1]=here[1]
                            curvei=0
                    else:
                        prev[0]=here[0]
                        prev[1]=here[1]
                    if moveto:
                        subpath_start[0]=here[0]
                        subpath_start[1]=here[1]
                        moveto=False
                else:
                    if paths[k][i]==paths[k][i].upper():
                        absolute=True
                    else:
                        absolute=False
                        paths[k][i]=paths[k][i].upper()
                    curve=False
                    moveto=False
                    if paths[k][i]=='C':
                        curve=True
                        curvei=0
                        clozed=False
                    elif paths[k][i]=='Z':
                        clozed=True
                        #prev[0]=subpath_start[0]
                        #prev[1]=subpath_start[1]
                        #here[0]=subpath_start[0]
                        #here[1]=subpath_start[1]
                    elif paths[k][i]=='M':
                        moveto=True
                        if clozed:
                            pass
                            #prev[0]=0
                            #prev[1]=0
                            #here[0]=0
                            #here[1]=0
                        clozed=False
                    else:
                        clozed=False
            paths[k]=' '.join(paths[k])

        ret='<g id="text">'
        for path in paths:
            ret+='<path d="'+path+'"/>'
        ret+='</g>'
        return(ret)
    def do_transform(self,xy,height,width):
        x,y=xy
        #x+=100
        y+=height/2
        x_p=self.sw*(np.exp((self.ew-self.sw)/height*(x/width))-1)/(self.ew-self.sw)
        y_p=y*(self.sw+(self.ew-self.sw)*x_p)/height
        x_p*=width
        x_p,y_p=self.on_path(x_p,y_p)
        
        return x_p,y_p
    def on_path(self,x,y):
        #print('x:',x)
        pathpoint=get_point(self.path,self.segs,x)
        tan=Vec2D(r=y,t=pathpoint[1]+radians(90))
        #tan._update_car()
        xy=pathpoint[0]+tan
        #return x,y
        return xy.x,xy.y
linecolor='#cc1111'
p=PrettyPath(Vec2D(10,50),Vec2D(r=320,t=radians(25)),-3,7)
t=TextPath('homo sapiens',30,20,p,5)
svg=t.text_to_svg()
ps=p.taperedpath(5,34,end_width=0,fill='none',stroke_width=2,stroke=linecolor)
ps=ps.tostring()

p2=PrettyPath(Vec2D(10,50),Vec2D(r=320,t=radians(25)),3,-7)
t=TextPath('homo sapiens',30,20,p2,5)
svg2=t.text_to_svg()
ps2=p.taperedpath(5,34,end_width=0,fill='none',stroke_width=2,stroke=linecolor)
ps2=ps2.tostring()

'''p2=prettypath.PrettyPath(Vec2D(10,150),Vec2D(r=260,t=radians(-40)),3.2,-5)
t2=TextPath('pan paniscus',29,12,p2,5)
svg2=t2.text_to_svg()
ps2=p2.taperedpath(5,36,fill='none',stroke_width=2,stroke=linecolor).tostring()
p3=prettypath.PrettyPath(Vec2D(10,250),Vec2D(r=370,t=radians(0)),-1,4)
t3=TextPath('pan troglodytes',30,20,p3,5)
svg3=t3.text_to_svg()
ps3=p3.taperedpath(5,35,fill='none',stroke_width=2,stroke=linecolor).tostring()
#t.text_to_svg()
p4=prettypath.PrettyPath(Vec2D(-155,201),Vec2D(r=1,t=radians(-100)),1.9,-2.2)
p4.path_to(Vec2D(10,250),5)
ps4=p4.taperedpath(5,38,end_width=35,fill='white',stroke_width=2,stroke=linecolor).tostring()
p5=prettypath.PrettyPath(Vec2D(-350,80),Vec2D(r=1,t=radians(60)),1.5,-3)
p5.path_to(Vec2D(-150,200),5)
ps5=p5.taperedpath(5,38,end_width=38,fill='white',stroke_width=2,stroke=linecolor).tostring()

p6=prettypath.PrettyPath(Vec2D(-350,80),Vec2D(r=1,t=radians(-30)),-1.8,2.6)
p6.path_to(Vec2D(10,50),5)
ps6=p6.taperedpath(5,38,end_width=35,fill='white',stroke_width=2,stroke=linecolor).tostring()
p7=prettypath.PrettyPath(Vec2D(-150,200),Vec2D(r=1,t=radians(0)),-0.3,-1.2)
p7.path_to(Vec2D(10,150),5)
ps7=p7.taperedpath(5,38,end_width=35,fill='white',stroke_width=2,stroke=linecolor).tostring()
'''

