#!/usr/bin/python
##########################################################################
# vizdiff.py,  (c) Copyright 2014 by Golden G. Richard III.
#
# Port of vizdiff.pl to Python.
#
# Visualize cumulative differences in binary data (e.g., disk images).
# For each cluster in a set of identically-sized binary blobs,
# cumulatively identify differences in the blobs using color:
#
# Blue areas:  zeroed clusters
# Green areas: non-zero, matching clusters (or just non-zero, in baseline)
# Red areas: non-matching clusters
#
# v1.0: first release, 8/2014.
##########################################################################
from __future__ import print_function
import os,sys,math
from stat import *
try:
    # for Python2.x
    from Tkinter import *
except ImportError:
    # for Python3.x
    from tkinter import *

class VizDiff:

    DEBUG=1
    VERSION="vizdiff v1.0"

    def __init__(self, root, filesize, clustersize, width):
        self.root = root
        self.clustersize = clustersize
        self.width = width
        self.filesize = filesize
        self.diffs_size = int(math.ceil(float(self.filesize) / 
                                        float(self.clustersize)))
        self.baseline = ['B'] * self.diffs_size
        self.diffs = ['G'] * self.diffs_size
        self.dim = math.ceil(math.sqrt(float(self.filesize) / 
                                       float(self.clustersize)))
        self.zero = ['\0'] * self.clustersize
    

    # produce baseline visualization of first disk image, illustrating
    # zeroed and non-zeroed clusters
    def display_baseline(self, filename):
        idx=0
        window = self.root            # Toplevel()                  
        window.title("Baseline: " + filename)
        drawing = Canvas(window)
        drawing.config(width=self.width, 
                       height=self.width, 
                       background="white")
        drawing.pack(fill=BOTH)

        f = open(filename, "rb")
        while True:
            data = f.read(self.clustersize)
            if not data:
                break
            if data != self.zero[0:len(data)]:
                self.baseline[idx] = 'G'
                if (self.DEBUG):
                    print("\"" + filename + "\": non-zero cluster", idx)

            drawing.create_rectangle(
               int(idx % self.dim) * (self.width / self.dim), # x1
               int(idx / self.dim) * (self.width / self.dim), # y1
               int(idx % self.dim) * (self.width / self.dim) + 
                   (self.width / self.dim), # x2
               int(idx / self.dim) * (self.width / self.dim) + 
                   (self.width / self.dim), # y2
               outline = ('blue' if self.baseline[idx] == 'B' else 'green'),
               fill = ('blue' if self.baseline[idx] == 'B' else 'green'))
            idx = idx + 1
        
        f.close()
        drawing.pack()
        window.update()


    # produce visualization of differences between two disk images
    def display_difference(self, filename1, filename2):

        idx=0
        window = Toplevel(self.root)                  
        window.title(filename1 + "-->" + filename2)
        drawing = Canvas(window)
        drawing.config(width=self.width, 
                       height=self.width, 
                       background="white")
        drawing.pack(fill=BOTH)

        # mark differences between clusters in the two disk images
        f1 = open(filename1, "rb")
        f2 = open(filename2, "rb")
        while True:
            data1 = f1.read(self.clustersize)
            data2 = f2.read(self.clustersize)
            if not data1:
                break

            if (data1 != self.zero[0:len(data1)] or 
                data2 != self.zero[0:len(data2)]):
                self.baseline[idx] = 'G'
            if data1 != data2:
                self.diffs[idx] = 'R'
                if (self.DEBUG):
                    print ("\"" + filename1 + "\" --> \"" + filename2 + 
                        "\": difference in non-zero cluster", idx)
            idx = idx + 1

        for idx in range(0, int(math.ceil(float(self.filesize) /
                                          float(self.clustersize)))):
            if self.diffs[idx] == 'R':
                drawing.create_rectangle(
                    int(idx % self.dim) * (self.width / self.dim), # x1
                    int(idx / self.dim) * (self.width / self.dim), # y1
                    int(idx % self.dim) * (self.width / self.dim) + 
                        (self.width / self.dim), # x2
                    int(idx / self.dim) * (self.width / self.dim) + 
                        (self.width / self.dim), # y2
                    outline = 'red', 
                    fill = 'red')
            else:
                drawing.create_rectangle(
                    int(idx % self.dim) * (self.width / self.dim)+1, # x1
                    int(idx / self.dim) * (self.width / self.dim)+1, # y1
                    int(idx % self.dim) * (self.width / self.dim) + 
                        (self.width / self.dim), # x2
                    int(idx / self.dim) * (self.width / self.dim) + 
                        (self.width / self.dim), # y2
                    outline = ('blue' if self.baseline[idx] == 'B' 
                               else 'green'),
                    fill = ('blue' if self.baseline[idx] == 'B' 
                              else 'green'))

        drawing.pack()
        window.update()


def main():

    root=Tk()
    numargs=len(sys.argv)
    fileidx=4
    if numargs < 4:
        sys.exit("Usage: vizdiff.py <clustersize> <width> " +
                 "<imgfile1> <imgfile2> [...<imgfileN>]\n")
    else:
        clustersize = int(sys.argv[1])
        width = int(sys.argv[2])
        (imagefilename1, imagefilename2) = sys.argv[3:5]
        if not os.path.isfile(imagefilename1):
            sys.exit("File \"" + imagefilename1 + "\" does not exist.\n")
        if not os.path.isfile(imagefilename2):
            sys.exit("File \""+ imagefilename2 + "\" does not exist.\n")

        (mode1, ino1, dev1, nlink1, uid1, gid1, size1, 
            atime1, mtime1, ctime1) = os.stat(imagefilename1)
        if not S_ISREG(mode1):
            sys.exit("Input must be regular files and file sizes " +
                     "must all be equal.\n")
        else:
            v = VizDiff(root, size1, clustersize, width)
            v.display_baseline(imagefilename1)
            while True:
                if not os.path.isfile(imagefilename2):
                    sys.exit("File \"" + imagefilename2 + "\" does not exist.")
                (mode2, ino2, dev2, nlink2, uid2, gid2, size2, 
                    atime2, mtime2, ctime2) = os.stat(imagefilename2)
                if not S_ISREG(mode2) or size1 != size2:
                    sys.exit("Input must be regular files and file sizes " +
                             "must all be equal.\n")
                else:
                    print("Computing differences between\"" + imagefilename1 + 
                        "\" and \"" + imagefilename2 + "\"...")
                    v.display_difference(imagefilename1, imagefilename2)
                    print("Done.")
                    fileidx = fileidx + 1
                    if fileidx >= numargs:
                        break
                    imagefilename1=imagefilename2
                    imagefilename2=sys.argv[fileidx]

        print("To exit, simply close the baseline window.")
        root.mainloop()

if __name__ == "__main__":
    main()
