#!/usr/bin/env python
# A JPEG simple carver.

import mmap,sys,os.path

if __name__=="__main__":
    if len(sys.argv)<2 or not os.path.exists(sys.argv[1]):
        print("Usage: {} image.raw".format(sys.argv[0]))
        exit(1)

    counter = 1
    with open(sys.argv[1],"rb") as f:
        map = mmap.mmap(f.fileno(),length=0,access=mmap.ACCESS_READ)
        start = 0
        while True:
            start = map.find("\xff\xd8\xff",start)
            if start==-1: break
            end = map.find("\xff\xd9",start)
            if end==-1: break
            print("JPEG {} found at byte offset {} length {}".format(
                    counter,start,end-start+2))
            with open("savefile{}.jpg".format(counter),"wb") as savefile:
                savefile.write(map[start:end+1])
            counter += 1
            start = end

                
