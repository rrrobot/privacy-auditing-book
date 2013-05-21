import numpy as np
import matplotlib

matplotlib.use('Agg')           # must be called before pyplot is imported

import matplotlib.pyplot as plt
#from matplotlib.colors import Colormap, normalize
from matplotlib.colors import colorConverter

if __name__=="__main__":
    import pylab
    import matplotlib.colors

    black = colorConverter.to_rgb("black")
    red = colorConverter.to_rgb("red")
    blue = colorConverter.to_rgb("blue")

    n=100

    # create a random array
    X= np.array([[red,red,red],[blue,blue,blue],[black,black,black]])


    #X[1][0] = red
    #cmBase = pylab.cm.jet

    # plot it array as an image
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(X, interpolation='nearest')

    # plot with the modified colormap and norm
    ax.imshow(X,interpolation='nearest')
    plt.savefig("output.pdf")
