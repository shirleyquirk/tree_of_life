#!/usr/bin/python
import requests
import sys
import urllib
import pathlib
import os
search=sys.argv[1]


url='https://web.archive.org/cdx/search'
payload={'url':search,'output':'json','matchType':'prefix','filter':'!statuscode:[45]..','collapse':'urlkey'}
r=requests.get(url,params=payload)
resp=r.json()
urls=[{i:j for i,j in zip(resp[0],r)} for r in resp[1:]]

print('Found ',len(urls),' resources at ',search)
print('Downloading...')
for u in urls:
    rr=requests.get('https://web.archive.org/web/'+u['timestamp']+'/'+u['original'])
    path=urllib.parse.urlparse(u['original'])
    path=path.netloc+path.path
    #sometimes a webpage is actually a directory
    #e.g. noisemachine.com/talk1
    #later might want noisemachine.com/talk1/1.html
    #in that case, move noisemachine.com/talk1 to noisemachine.com/talk1/index.html
    
    #if there's a trailing /, add index.html anyway
    if path[-1]=='/':
        path+='index.html'
    
    #create all parent directories, moving files as necessary
    try:
        pathlib.Path(path).parent.mkdir(parents=True,exist_ok=True)
    #get either a FileExistsError or a NotADirectoryError
    except(FileExistsError):
        #directory already exists as a file, so move it
        problem=str(pathlib.Path(path).parent)
        with open(problem,'r') as f:
            tmpfl=f.read()
        os.remove(problem)
        os.mkdir(problem)
        with open(problem+'/index.html','w') as f:
            f.write(tmpfl)

    #Now try writing the file
    #will overwrite things, but hey ho
    try:
        with open(path,'w') as f:
            f.write(rr.text)
    except IsADirectoryError:
        #trying to write to a directory
        #add /index.html and try again
        path+='/index.html'
        with open(path,'w') as f:
            f.write(rr.text)

