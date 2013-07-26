import sys,os,os.path
import numpy as np
import matplotlib

matplotlib.use('Agg')           # generate a PDF without a GUI

import matplotlib.pyplot as plt # plotter

# Render an array as a PDF file
def render(data,width=10,ofn="output.pdf"):
    ratio = len(data) / (width*width)
    fig = plt.figure(figsize=(8,8*ratio))
    ax = fig.add_subplot(111)
    y = 0
    for i in range(len(data)):
        x = i % width
        xs = [x,x,x+1,x+1]        # Create the points of a polygon to be filled
        ys = [y,y+1,y+1,y]
        ax.fill(xs,ys, color=M[i])
        if(x==width-1): y+=1

    ax.invert_yaxis()
    ax.set_title('Some title!')
    ax.set_yticklabels([])      # remove Y ticks
    ax.set_xticklabels([])      # remove X ticks
    plt.savefig(ofn)
        

if __name__=="__main__":
    rgb = matplotlib.colors.colorConverter.to_rgb # RGB color generator
    white = rgb("white")
    M = [white]*48
    print(M)
    render(M,width=8,ofn="try.pdf")
