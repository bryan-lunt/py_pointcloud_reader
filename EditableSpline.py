import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D

from spline_tools import ParametricSpline

class EditableSpline:
    def __init__(self, an_ax,initial_data=None,color='#00FF00'):
        self.ax = an_ax
        self.press = None
        self.data = initial_data if initial_data is not None else np.zeros((1,2))
        self.markers = list()
        for x,y in initial_data:
            tmp = patches.Rectangle((x, y), 5,5)
            self.markers.append(tmp)
            self.ax.add_patch(tmp)

        self.color = color
        self.line = None
        self.spline = None
        self.spline_line = None

    def update_line(self):

        self.spline = ParametricSpline(self.data[:,0],self.data[:,1])

        if self.spline_line is not None:
            self.spline_line.remove()
        spline_data = self.spline(np.linspace(0.0,1.0,20*self.data.shape[0]))
        self.spline_line = Line2D(spline_data[:,0], spline_data[:,1],c="#0000FF")
        self.ax.add_line(self.spline_line)

        #Seems out of order, but we want this to render over the spline
        if self.line is not None:
            self.line.remove()
        self.line = Line2D(self.data[:,0], self.data[:,1], ls='--', c=self.color,
                  marker='x', mew=2, mec='#204a87')
        self.ax.add_line(self.line)


    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.ax.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.ax.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.ax.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def on_press(self, event):
        'on button press we will see if the mouse is over us and store some data'
        #print "press"
        #self.press = None
        if event.inaxes != self.ax: return

        contains = None
        for i in range(len(self.markers)):
            contains,_ =  self.markers[i].contains(event)
            if contains:
                break
        if not contains: return

        x0, y0 = self.markers[i].xy
        self.press = i, x0, y0, event.xdata, event.ydata

    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        if self.press is None: return
        if event.inaxes != self.ax: return

        i, x0, y0, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        #print('x0=%f, xpress=%f, event.xdata=%f, dx=%f, x0+dx=%f' %
        #      (x0, xpress, event.xdata, dx, x0+dx))

        self.data[i,0] = x0+dx
        self.data[i,1] = y0+dy

        self.markers[i].set_x(x0+dx)
        self.markers[i].set_y(y0+dy)
        self.update_line()
        self.ax.figure.canvas.draw()


    def on_release(self, event):
        'on release we reset the press data'
        if self.press is not None:
            pass
            #update the spline
            #self.update_line()

        self.press = None
        self.ax.figure.canvas.draw()

    def disconnect(self):
        'disconnect all the stored connection ids'
        self.ax.canvas.mpl_disconnect(self.cidpress)
        self.ax.canvas.mpl_disconnect(self.cidrelease)
        self.ax.canvas.mpl_disconnect(self.cidmotion)

class MultiSpline(object):
    def __init__(self,ax,multiple_data):
        self.ax = ax
        self.datas = multiple_data
        self.splines = list()
        for i in range(len(multiple_data)):
            self.splines.append(EditableSpline(ax,self.datas[i]))

    def on_press(self, event):
        for i in self.splines:
            i.on_press(event)

    def on_motion(self, event):
        for i in self.splines:
            i.on_motion(event)

    def on_release(self, event):
        for i in self.splines:
            i.on_release(event)

    def update_line(self):
        for i in self.splines:
            i.update_line()

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.ax.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.ax.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.ax.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def disconnect(self):
        'disconnect all the stored connection ids'
        self.ax.canvas.mpl_disconnect(self.cidpress)
        self.ax.canvas.mpl_disconnect(self.cidrelease)
        self.ax.canvas.mpl_disconnect(self.cidmotion)

if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot(111)

    thedata = np.array(([[0.1,0.1],
                        [0.5, 0.5],
                        [0.75, 0.75]]))

    myspline = EditableSpline(ax,thedata)
    myspline.connect()
    myspline.update_line()

    plt.show()
