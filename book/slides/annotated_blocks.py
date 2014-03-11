from pylab import *
from matplotlib import colors
# A = [[1,2,3,4,5]]
A = [[0],[1]]
Amap = colors.ListedColormap(['blue','green'])

fig = figure(1)
ax = fig.add_subplot(111, autoscale_on=False)
imshow(A, cmap=Amap, interpolation='nearest')
ax.annotate('AA BB', fontsize=20, xy=(.25, .75),
            xycoords='data', xytext=(150, -6),
            textcoords='offset points',
            arrowprops=dict(arrowstyle="->",
                            linewidth = 5.,
                            color = 'red')
            )
ax.annotate('CC DD', fontsize=20, xy=(.25, .25),
            xycoords='data', xytext=(150, -6),
            textcoords='offset points',
            arrowprops=dict(width = 5.,
                            headwidth = 15.,
                            frac = 0.2,
                            shrink = 0.05,
                            linewidth = 2,
                            color = 'red')
            )
axis('off')
savefig('graph-py.pdf')
show()
close()
