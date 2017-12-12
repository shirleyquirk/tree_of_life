import sys
import importlib
if 'generate' in sys.modules:
    importlib.reload(sys.modules['generate'])
    
import xml.etree.ElementTree as etree
 
from vec2d import Vec2D
from cprettypath import radians
import svgwrite
from random import random,randrange,gauss,randint
#archea.
#myArchea.root
start=Vec2D(3000,3000)
from generate import metatree,Branch
from cprettypath import degrees
def myround(n,sigfigs):
    ret=int(n*(10**sigfigs))/(10**sigfigs)
    return str(ret)


#myArchea.count_terminals()
clad= {'Diaphoretickes':(46,10),'Bacteria':(19,14),'Fungi':(67,9),'Metazoa':(43,11),'Amoebozoa':(1,10)}

from multiprocessing import Process
from subprocess import call

def generate_a_tree(cladname,numbranches,numtrees,filenames_in):
    branchings=numbranches
    x=[branchings]*numtrees
    
    #t1=radians(-29)+radians(randint(-5,5))
    t1=gauss(radians(-29),radians(2))
    t1=gauss(radians(-26.8),radians(1))
    #t2=radians(75)+radians(randint(-9,9))
    t2=gauss(radians(75),radians(3))
    t2=gauss(radians(72.9),radians(1.5))
    #theta=Branch(Branch(0.68+random()*0.09,0.83+random()*0.09),Branch(1.05,0.75+random()*0.45))
    theta=Branch(Branch(gauss(0.725,0.03),gauss(0.86,0.03)),Branch(gauss(1.05,0.3),gauss(0.807,0.2)))
    length=Branch(0.79+random()*0.05,0.63+random()*0.17)
    
    theta=Branch(Branch(gauss(0.733,0.03),gauss(0.825,0.03)),Branch(gauss(0.9,0.1),gauss(0.62,0.2)))
    
    #Metazoa:t1=-31.0_t2=68.0_thet=((0.757_0.892)(1.05_0.842)_len=(0.8_0.66)
    
    t1=radians(-31)
    t2=radians(68)
    theta=Branch(Branch(0.757,0.892),Branch(1.05,0.842))
    length=Branch(0.8,0.66)
    
    #theta=Branch(Branch(0.72,0.79),Branch(0.89,0.84))
    #length=Branch(0.81,0.68)
    
    #file:///home/bwsq/Documents/TreeOfLife/processing-lite/test_15px_2*2%5E15
    #t1=-25.0,t2=82.0,thet%3A((0.75,0.87),(1.05,1.054),len=(0.83,0.7).svg
    #t1=-29.0,t2=78.0,thet:((0.718,0.873),(1.05,0.808),len=(0.81,0.65)
    #t1=radians(-28)
    #t2=radians(78)
    #theta=Branch(Branch(0.694,0.897),Branch(1.05,0.896))
    #length=Branch(0.79,0.77)
    
    import cProfile
    #cProfile.run('''
    m=metatree(start,x,10,Branch(t1,t2),theta,length,render=True,debug=False)
    #''')

    termpos=[]
    dwg=svgwrite.Drawing(size=('3600mm','3600mm'),debug=False)
    threadfilt=dwg.defs.add(svgwrite.filters.Filter())
    threadfilt.feMerge(['SourceGraphic'],result='bypass')
    for i in range(3):
        threadfilt.feTurbulence(stitchtiles='stitch',type='turbulence',baseFrequency=gauss(0.07,0.03),numOctaves=16,result='haze'+str(i),seed=randrange(193048148176))
        threadfilt.feTurbulence(stitchtiles='stitch',type='fractalNoise',baseFrequency=0.1,numOctaves=4,result='noise'+str(i),seed=randrange(109861223425))
        threadfilt.feDisplacementMap(in_='SourceGraphic',in2='haze'+str(i),scale=gauss(3.5,0.9),xChannelSelector='R',yChannelSelector='G',result="twiddle"+str(i))
        threadfilt.feColorMatrix(in_='twiddle'+str(i),result='black_twiddle'+str(i),type='matrix',values="1 0 0 0 0.7   0 1 0 0 0.7  0 0 1 0 0   0.4 0.4 0.6 0 0",debug=False)
        threadfilt.feGaussianBlur(in_='black_twiddle'+str(i),result='shadow_twiddle'+str(i),stdDeviation=0.15)
        threadfilt.feGaussianBlur(in_='twiddle'+str(i),result='hazy_twiddle'+str(i),stdDeviation=0.07)
        threadfilt.feComposite(in_='hazy_twiddle'+str(i),in2='shadow_twiddle'+str(i),result='shadowed_twiddle'+str(i),operator='over')
    threadfilt.feMerge(['shadowed_twiddle'+str(i) for i in range(3)],result='twisted_flax')
    threadfilt.feMorphology(in_='SourceGraphic',operator='dilate',radius=1.25,result='blurrr')
    threadfilt.feTurbulence(stitchtiles='stitch',type='turbulence',baseFrequency=0.1,numOctaves=4,result='noise')
    threadfilt.feDisplacementMap(in_='blurrr',in2='noise',scale=1.2,result='fuzzy')
    threadfilt.feComposite(in_='twisted_flax',in2='fuzzy',operator='in',result='reeesult')
    threadfilt.feGaussianBlur(in_='reeesult',stdDeviation=0.05)
    threadfilt.feMerge(['bypass'])

    g=dwg.g(id='topgroup',filter=threadfilt.get_funciri())
    for t in m['trees']:
        pos=tuple(float(s) for s in t['transform'][7:-1].split(',')[1:])
        termpos.append(Vec2D(*pos))
        g.add(t)
    dwg.add(g)
 

    filename= cladname+'_t1='+myround(degrees(t1),1)+'_t2='+myround(degrees(t2),1)+'_thet=(('+myround(theta.l.l,3)+'_'+myround(theta.l.r,3)+')('+myround(theta.r.l,3)+'_'+myround(theta.r.r,3)+')'+'_len=('+myround(length.l,2)+'_'+myround(length.r,2)+').svg'
    print(filename)
    with open(filename,'w') as f:
        f.write(dwg.tostring())
    with open(filenames_in,'a')as f:
        f.write(filename+'\n')
   
'''    
for numtrees in [14]:    
    ps=[]
    for i in range(8):
        ps.append(Process(target=generate_a_tree,args=('chordata'+str(numtrees),9,numtrees*2,'poobumpants')))
        ps[-1].start()
    for p in ps:
        p.join()
    filenames=[]
    with open('poobumpants','r') as f:
        filenames=f.readlines()
    for f in filenames:
        f=f.strip()
        call(['inkscape','-f',f,'-e',f+'_thumb.png','-D','-d','60'])
    with open('poobumpants','w') as f:
        f.write('')
'''
#generate_a_tree('Bacteria-final',14,19)
ps=[]
'''for i in range(14,15):
    ps.append(Process(target=generate_a_tree,args=('Arthropods_final'+str(i)+'_9',i,30,'poobumpants')))
    ps[-1].start()
for p in ps:
    p.join()
'''
with open('poobumpants','r') as f:
    filenames=f.readlines()
for f in filenames:
    f=f.strip()

    #split into lhs only
    X=etree.parse(f)
    Xr=X.getroot()
    l=len(Xr[1])
    dontwant=Xr[1][l//2:]
    for e in dontwant:
        Xr[1].remove(e)
    with open(f,'w') as g:
        g.write(etree.tostring(Xr,encoding='unicode'))
    
    call(['inkscape','-f',f,'-e',f+'_thumb.png','-D','-d','60'])
with open('poobumpants','w') as f:
    f.write('')


