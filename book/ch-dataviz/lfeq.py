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
    x = [1,2,3,4,5,7,8,9,10]
    y = [4,3,1,3,4,5,2,3,4]
    #ax.plot(x,y)
    #ax.plot(x,[5]*9)
    ax.bar(['red','blue','green'],[1,2,3])
    #ax.bar(x,y)
    ax.set_title('Some title!')
    #ax.set_yticklabels([])      # remove Y ticks
    #ax.set_xticklabels([])      # remove X ticks
    plt.savefig(ofn)
        

if __name__=="__main__":
    rgb = matplotlib.colors.colorConverter.to_rgb # RGB color generator
    white = rgb("white")
    M = [white]*48
    print(M)
    render(M,width=8,ofn="try.pdf")
