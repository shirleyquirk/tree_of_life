#!/usr/bin/python

#DIRS=['Archaea','Archaeplastida','Ichthy','Choano','Bacteria','metazoans','Arthropods','Amoebae','Excavata','Fungi','SAR']
#DIRS=DIRS[2:]
DIRS=['Archaea','Archaeplastida','Amoebae']

#!/usr/bin/python

import sys
import time
import xml.etree.ElementTree as etree
from time import time
from subprocess import run,PIPE
from multiprocessing import Pool
try:
	filename=sys.argv[1]
except IndexError:
	print("usage: DPI ")
	quit()
DPI=sys.argv[1]


def rerender_one(filename,destdir,DPI):

    print('Parsing XML.......',)
    X=etree.parse(filename)
    print('done')
    Xr=X.getroot()
    ns={'s':'http://www.w3.org/2000/svg'}
    subs=Xr.findall('s:g',ns)

    if len(subs)==1:#topgroup
        subs=subs[0].findall('s:g',ns)


    names=[]
    has_good_ids=True
    for s in subs:
        names.append(s.get('id'))
        if names[-1]==None:
            has_good_ids=False

    #copy to tmp for faster reading?
    tmpfile=''
    if not has_good_ids:
        names=[]
        for idx,s in enumerate(subs):
            s.set('id','bitmapgp_'+str(idx))
            names.append('bitmapgp_'+str(idx))
        #save it again with new names
        print('Saving new group names...',)
        tmpfile='/tmp/tempfile.svg'
        with open(tmpfile,'w') as f:
            f.write(etree.tostring(Xr,encoding='unicode'))
        print('done')
    else:
        run(['cp',filename,'/tmp/tempfile.svg'])
        tmpfile='/tmp/tempfile.svg'

    #now get inkscape to export pngs for each of our interesting groups
    print('Exporting bitmapped groups.',)
    for n in names:
        returncode=1
        while returncode:
            returncode=run(['inkscape','-f',tmpfile,'--export-id='+n,'--export-id-only','--export-area-drawing','--export-png='+destdir+n+'.png','--export-dpi='+DPI]).returncode
            if returncode:
                print('FAILED...retrying...')
        print('...done')
    print('done')

from time import time
backup='/master/backup-'+str(int(time()))
for d in DIRS:
    run(['mkdir',d+backup])
    run(['cp','-r',d+'/master/pngs/',d+backup])
    run(['mkdir',d+'/master/'+DPI+'dpi'])
    run(['mkdir',d+'/master/'+DPI+'dpi/pngs'])
    rerender_one(d+'/master/master.svg',d+'/master/'+DPI+'dpi/pngs/',DPI)
    
