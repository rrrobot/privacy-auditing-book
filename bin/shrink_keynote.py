#!/usr/bin/env python3
#
# shrink a keynote presentation
# 
import zipfile,os
from subprocess import call

def process(fn):
    startsize = os.path.getsize(fn)
    z = zipfile.ZipFile(fn,"a")
    doc = z.open("index.apxl").read().decode('utf-8')
    tiffs = []
    print(type(doc))
    for finfo in z.infolist():
        if finfo.filename.endswith(".tiff"):
            tiffname = finfo.filename
            pngname  = finfo.filename.replace(".tiff",".png")
            z.extract(tiffname)
            call(['convert',tiffname,pngname])
            z.write(pngname,pngname)
            printf("{} -> {} saving {} bytes".format(tiffname,pngname,os.path.getsize(tiffname)-os.path.getsize(pngname)))
            os.unlink(pngname)
            os.unlink(tiffname)
            doc=doc.replace(tiffname,pngname)
            tiffs.append(tiffname)
    if len(tiffs)==0:
        print("there were no TIFFs in {} to change to PNGs".format(fn))
        exit(0)
    f = open("index.apxl","w")
    f.write(doc)
    f.close()
    z.close()
    call(['zip','-f',fn,'index.apxl'])
    call(['zip','-d',fn] + tiffs)
    endsize = os.path.getsize(fn)
    print("Saved {:,}MB ({:6.2g}%)".format((startsize-endsize)//1000000,(startsize-endsize)*100.0/startsize))

            
if __name__=="__main__":
    import sys, time
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('keyfile',action='store',help='Keynote File to process',nargs='+')
    args = parser.parse_args()
    for fn in args.keyfile:
        process(fn)
    
    
