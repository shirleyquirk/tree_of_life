#!/usr/bin/python
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


from multiprocessing import Process
from subprocess import run


def generate_a_tree(cladname,numbranches,numtrees,filenames_in,t1,t2,theta,length):
    branchings=numbranches
    x=[branchings]*numtrees
    
    #t1=gauss(radians(-29),radians(2))
    #t1=radians(-32)

    #t2=gauss(radians(75),radians(3))
    #t2=radians(78)
    
    #theta=Branch(Branch(gauss(0.725,0.03),gauss(0.86,0.03)),Branch(gauss(1.05,0.3),gauss(0.807,0.2)))
    #theta=Branch(Branch(0.738,0.897),Branch(1.05,0.951))
    
    #length=Branch(0.79+random()*0.05,0.63+random()*0.17)
    #length=Branch(0.8,0.63)
    
    
    #print("Generating tree. t1="+str(t1)+',t2='+str(t2)+',tm='+str(theta)+',lm='+str(length))
    m=metatree(start,x,10,Branch(radians(t1),radians(t2)),theta,length,render=True,debug=False)
    
    termpos=[]
    dwg=svgwrite.Drawing(size=('3600mm','3600mm'),debug=False)
    
    '''threadfilt=dwg.defs.add(svgwrite.filters.Filter())
    threadfilt.feMerge(['SourceGraphic'],result='bypass')
    for i in range(3):
        threadfilt.feTurbulence(stitchtiles='stitch',type='turbulence',baseFrequency=gauss(0.07,0.03),numOctaves=16,result='haze'+str(i),seed=randrange(193048148176))
        threadfilt.feTurbulence(stitchtiles='stitch',type='fractalNoise',baseFrequency=0.1,numOctaves=4,result='noise'+str(i),seed=randrange(109861223425))
        threadfilt.feDisplacementMap(in_='SourceGraphic',in2='haze'+str(i),scale=gauss(3.5,0.9),xChannelSelector='R',yChannelSelector='G',result="twiddle"+str(i))
        threadfilt.feColorMatrix(in_='twiddle'+str(i),result='black_twiddle'+str(i),type='matrix',values="0.4 0 0 0 0.6   0 0.4 0 0 0.6  0 0 0.4 0 0.6   0 0 0 0.6 0",debug=False)
        threadfilt.feGaussianBlur(in_='black_twiddle'+str(i),result='shadow_twiddle'+str(i),stdDeviation=0.15)
        threadfilt.feGaussianBlur(in_='twiddle'+str(i),result='hazy_twiddle'+str(i),stdDeviation=0.09)
        threadfilt.feComposite(in_='hazy_twiddle'+str(i),in2='shadow_twiddle'+str(i),result='shadowed_twiddle'+str(i),operator='over')
    threadfilt.feMerge(['shadowed_twiddle'+str(i) for i in range(3)],result='twisted_flax')
    threadfilt.feGaussianBlur(in_='twisted_flax',stdDeviation=0.05)
    threadfilt.feMerge(['bypass'])
    '''
    #g=dwg.g(id='topgroup',filter=threadfilt.get_funciri())
    for idx,t in enumerate(m['trees']):
        #pos=tuple(float(s) for s in t['transform'][7:-1].split(',')[1:])
        #termpos.append(Vec2D(*pos))
        t['id']='choanotree_'+str(idx)
        dwg.add(t)
 

    filename= '/tmp/'+cladname+'.svg'#+'_t1='+myround(degrees(t1),1)+'_t2='+myround(degrees(t2),1)+'_thet=(('+myround(theta.l.l,3)+'_'+myround(theta.l.r,3)+')('+myround(theta.r.l,3)+'_'+myround(theta.r.r,3)+')'+'_len=('+myround(length.l,2)+'_'+myround(length.r,2)+').svg'
    
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
#t1=-30.0_t2=73.0_thet=((0.688_0.836)(1.05_1.026)_len=(0.79_0.68)
coeffs=[[-30,73,((0.688,0.836),(1.05,1.026)),(0.79,0.68)]]


    

def generate_with_coefs(c,double=False):
    lenm=Branch(*c.pop())
    thm=c.pop()
    thm=Branch(Branch(*thm[0]),Branch(*thm[1]))
    t2=c.pop()
    t1=c.pop()
    NumBranches=1
    if double:
        NumBranches*=2
    ps=[]
    for i in range(10,14):
        ps.append(Process(target=generate_a_tree,args=('Choanozoa_'+'_'.join([str(i),str(NumBranches),str(t1),str(t2),str((tuple(thm.l),tuple(thm.r))),str(tuple(lenm))]),i,NumBranches,'poobumpants',t1,t2,thm,lenm)))
        ps[-1].start()
    for p in ps:
        p.join()

    with open('poobumpants','r') as f:
        filenames=f.readlines()
    l=len(filenames)
    for f in filenames:
        f=f.strip()
        fileprefix=f[len('/tmp/'):-len('.svg')]
        run(['mkdir','Choano/'+fileprefix])
        #colorify
        X=etree.parse(f)
        Xr=X.getroot()
        if double:
            l=len(Xr[1])
            dontwant=Xr[1][l//2:]
            for e in dontwant:
                Xr[1].remove(e)
        ns={'s':'http://www.w3.org/2000/svg'}
        paths=Xr.findall('.//s:path',ns)
        for p in paths:
            p.attrib['fill']='#2c8f82'
            if 'style' in p.attrib:
                styles={s.split(':')[0]:s.split(':')[1] for s in p.attrib['style'].split(';')}
                if 'fill' in styles:
                    styles.pop('fill')
                p.attrib['style']=';'.join(':'.join((s,styles[s])) for s in styles)
        with open(f,'w') as g:
                g.write(etree.tostring(Xr,encoding='unicode'))
        print('Exporting bitmapped groups.',)
        '''if one_obj is not None:
        run(['inkscape','-f',tmpfile,'--export-id='+one_obj,'--export-id-only','--export-area-drawing','--export-png='+one_obj+'.png','--export-dpi='+DPI])#,'--export-area='+str(x0)+':'+str(y0)+':'+str(x1)+':'+str(y1)])
        quit()
        '''
        DPI='30'
        tmpfile=f
        destfile='Choano/'+fileprefix+'/'+fileprefix+'.svg'
        destdir='Choano/'+fileprefix+'/'
        names=['choanotree_'+str(idx) for idx in range(NumBranches)]
        for n in names:
            #x0=coefs[n]['x']
            #y0=coefs[n]['y']
            #x1=coefs[n]['x']+coefs[n]['w']
            #y1=coefs[n]['y']+coefs[n]['h']
            retcod=1
            loop_times=0
            while retcod:
                retcod=run(['nice','inkscape','-f',tmpfile,'--export-id='+n,'--export-id-only','--export-area-drawing','--export-png='+destdir+n+'.png','--export-dpi='+DPI]).returncode
                loop_times+=1
                if retcod:
                    print("FAILED, retrying...")
                if loop_times>10:
                    print("Giving up...")
                    break
                    
            print('...done')
        run(['nice','inkscape','-f',tmpfile,'--export-area-drawing','--export-png='+destdir+fileprefix+'.png','--export-dpi='+DPI])
        run(['mv',tmpfile,destfile])

    run(['rm','poobumpants'])

for c in coeffs:
    generate_with_coefs(c,double=False)


