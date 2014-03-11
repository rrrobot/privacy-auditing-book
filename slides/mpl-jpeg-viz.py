#!/usr/bin/env python3.2

# http://stackoverflow.com/questions/9295026/matplotlib-plots-removing-axis-legends-and-white-spaces
# http://matplotlib.org/examples/pylab_examples/image_interp.html
# http://stackoverflow.com/questions/9707676/defining-a-discrete-colormap-for-imshow-in-matplotlib

from pylab import *
from matplotlib import colors
# A = [[1,2,3,4,5]]
A = [[0],[1]]
Amap = colors.ListedColormap(['blue','green'])

figure(1)
imshow(A, cmap=Amap, interpolation='nearest')
annotate('AA BB',xy=(0,0), xytext=(.8,0), fontsize=20)
axis('off')
savefig('graph-py.pdf')
show()
