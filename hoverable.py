import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.figure import Figure
import numpy as np

class Hoverable(Figure):
    """A figure with Hoverable points"""

    def __init__(self,x,y,images,boxsize=15,marker="o"):
        self.x=x
        self.y=y
        self.images=images
    
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.line, = self.ax.plot(x,y, ls="", marker=marker)
        self.im = OffsetImage(images[0,:,:], zoom=boxsize)
        self.xybox=(95., 95.)
        self.ab = AnnotationBbox(self.im, (0,0), xybox=self.xybox, xycoords='data',
        boxcoords="offset points",  pad=0.3,  arrowprops=dict(arrowstyle="->"))
        self.ax.add_artist(self.ab)
        self.ab.set_visible(False)
        self.fig.canvas.mpl_connect('motion_notify_event', self.hover)


    def hover(self,event):
    # if the mouse is over the scatter points
        if self.line.contains(event)[0]:
            # find out the index within the array from the event
            ind, = self.line.contains(event)[1]["ind"]
            # get the figure size
            w,h = self.fig.get_size_inches()*self.fig.dpi
            ws = (event.x > w/2.)*-1 + (event.x <= w/2.) 
            hs = (event.y > h/2.)*-1 + (event.y <= h/2.)
            # if event occurs in the top or right quadrant of the figure,
            # change the annotation box position relative to mouse.
            self.ab.xybox = (self.xybox[0]*ws, self.xybox[1]*hs)
            # make annotation box visible
            self.ab.set_visible(True)
            # place it at the position of the hovered scatter point
            self.ab.xy =(self.x[ind], self.y[ind])
            # set the image corresponding to that point
            self.im.set_data(self.images[ind,:,:])
        else:
            #if the mouse is not over a scatter point
            self.ab.set_visible(False)
        self.fig.canvas.draw_idle()


