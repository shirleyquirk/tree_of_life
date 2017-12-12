#layout2
from math import sqrt
rootbranches=[(3280,322,55),(2633,980,156),(3013,1311,1060),(2397,1471,690),(2050,1461,169),(2269,2326,1431),(1556,2042,60),(1751,2148,1750),\
(1861,2659,1336),(1245,2783,819),(1002,2637,244),(332,3269,-58),(684,3169,-501),(1366,2466,-633),(1777,2739,-1317),(2359,2305,-1487),(2481,1697,-1039),\
(2359,1454,-614),(3008,1335,-1079),(3086,741,-497)]

rootbranches=[(3280,322,55),\
    (2633,980,156),\
    (3013,1311,1060),\
    (2397,1471,690),\
    (2050,1561,159),\
    (2269,2326,1431),\
    (1556,2042,60),\
    (1751,2148,750),\
    (1861,2659,1336),\
    (1245,2783,819),\
    (1002,2637,244),\
    (332,3269,-58),\
    (684,3169,-501),\
    (1366,2466,-633),\
    (1777,2739,-1317),\
    (2359,2305,-1487),\
    (1838,1768,-135),\
    (2481,1697,-1039),\
    (2359,1454,-614),\
    (3008,1335,-1079),\
    (3086,741,-497)]

def get_xy(r1,r2,x,diam):
    #returns xy relative to centre
    #i.e. intersections of two circles.
    #r1^2=x^2+(y+1800)^2
    #r2^2=x^2+(y-1800)^2
    #y^2+3600y+1800^2+y^2-3600y+1800^2
    #2y^2+2*1800^2=r1^2+r2^2
    #y^2=(r1^2+r2^2-(3595)^2/2)/2
    #r1^2-r2^2=y^2+3600y+1800^2-y^2-3600y+1800^2
    diam=3595
    y=sqrt((r1*r1+r2*r2-diam*diam/2)/2) # or -sqrt...
    #x=sqrt(r1^2-(y-1800)^2)
    xys=[]
    for rr1 in range(r1-1,r1+2):
        for rr2 in range(r2-1,r2+2):
            y=sqrt((rr1*rr1+rr2*rr2-diam*diam/2)/2)
            try:
                 x1=sqrt(rr1**2-(y+diam/2)**2)
                 y1=y
            except ValueError:
                x1=sqrt(rr1**2-(-y+diam/2)**2)
                y1=-y
            try:
                 x2=sqrt(rr2**2-(y-diam/2)**2)
                 y2=y
            except ValueError:
                x2=sqrt(rr2**2-(-y-diam/2)**2)
                y2=-y
            xys.append(min([(abs(x1-x),(x1,y1)),(abs(x2-x),(x2,y2))])[1])
    xs,ys=zip(*xys)
    return (min(xs),min(ys),max(xs),max(ys))

import svgwrite
'''dwg=svgwrite.Drawing()
for r in rootbranches:
    rect=get_xy(r[0],r[1],r[2],3595)
    x=r[2]
    y=(rect[1]+rect[3])/2
    dx=5
    dy=abs(rect[1]-rect[3])/2
    #display a circle. if we knew it exactly, it'd be 50mm diameter, right? so we add  our deltax, deltay to that
    dwg.add(dwg.ellipse((x,y),(50+dx,50+dy)))
with open('holes.svg','w') as f:
    f.write(dwg.tostring())
'''    


#within inkscape:
dwg=svgwrite.Drawing('circles.svg')
for idx,r in enumerate(rootbranches):
    g=dwg.g(id='circles_'+str(idx))
    g.add(dwg.circle(('0mm','1800mm'),str(r[0])+'mm',stroke_width='10mm',fill='none',stroke='red'))
    g.add(dwg.circle(('0mm','-1800mm'),str(r[1])+'mm',stroke_width='10mm',fill='none',stroke='red'))
    g.add(dwg.line((str(r[2])+'mm','1800mm'),(str(r[2])+'mm','-1800mm'),stroke_width='10mm',stroke='red'))
    dwg.add(g)
dwg.save()
CMDS='inkscape -f circles.svg'
for r in rootbranches:
    CMDS+=' --verb EditSelectNext'
    CMDS+=' --verb SelectionUnGroup'
    CMDS+=' --verb StrokeToPath'
    CMDS+=' --verb SelectionIntersect'
#CMDS+=' --verb EditSelectAll'
#for i in range(12):
#        CMDS+=' --verb SelectionOffset'
from subprocess import run
run(CMDS.split(' '))
    
