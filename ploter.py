import matplotlib.pyplot as plt
from matplotlib import animation, rc
import math
import numpy as np


frame_interval = 1

def show():
    plt.show()

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def movie(xs,earth,xpos,ypos):
    fig = plt.figure()
    ax = plt.axes(xlim=(2*(-max(ypos)), 2*max(ypos)), ylim=(2*(-max(ypos)), 2*max(ypos)))
    line, = ax.plot([], [], 'o-y', lw=2)
    line2, = ax.plot([], [], '_-b', lw=2)
    line3, = ax.plot([], [], '_-b', lw=2)
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
    altitude_text = ax.text(0.02, 0.90, '', transform=ax.transAxes)
    x_text = ax.text(0.02, 0.85, '', transform=ax.transAxes)
    y_text = ax.text(0.02, 0.80, '', transform=ax.transAxes)
    circle3 = plt.Circle((0,0), earth.equator_radius, color='g', clip_on=False)
    ax.add_artist(circle3)

    ax.scatter(xpos,ypos, lw=0.1)
    #for x,y in  zip(xpos,ypos):
    #    ax.plot([x,y],[],'0-g',lw=1)
    #    ax.scatter(x,y)




    # initialization function: plot the background of each frame
    def init():
        line.set_data([], [])
        line2.set_data([], [])
        line3.set_data([], [])
        time_text.set_text('')
        altitude_text.set_text('')
        x_text.set_text('')
        y_text.set_text('')
        return line, line2, line3,time_text,altitude_text,x_text,y_text,

    # animation function.  This is called sequentially
    def animate(i):
        indexOfFrame=find_nearest(xs,i)
        x = xpos[indexOfFrame]
        y = ypos[indexOfFrame]
        altitude=earth.distance_from_center(x,y)-earth.equator_radius
        line.set_data(x, y)
        line2.set_data(0, earth.troposphere[1])
        line3.set_data(0, earth.lower_stratosphere[1])
        time_text.set_text('frame = %.1d out of %1d frames' % (i,math.floor(max(xs))))
        altitude_text.set_text('altitude = %.1f m' % altitude)
        x_text.set_text('x = %.1f m' % x)
        y_text.set_text('y = %.1f m' % y)
        return line, line2, line3,time_text,altitude_text,x_text,y_text,



    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=math.floor(max(xs)), interval=frame_interval, blit=True)

    #anim.save('rocketboi.mp4', fps=166, extra_args=['-vcodec', 'libx264'])


def showGuides(col,data,rocket,points=False,lines=False):
    stage_1_end = rocket.stage_1_firing_time
    stage_2_end = rocket.stage_1_firing_time + rocket.stage_2_firing_time
    stage_3_end = rocket.stage_1_firing_time + rocket.stage_2_firing_time + rocket.stage_3_firing_time

    xs=data[0]
    ys=data[1]

    if points:
        col.plot(stage_1_end, ys[find_nearest(xs,stage_1_end)], color='r', marker='o', linestyle='dashed', linewidth=2, markersize=4)
        col.plot(stage_2_end, ys[find_nearest(xs,stage_2_end)], color='m', marker='o', linestyle='dashed', linewidth=2, markersize=4)
        col.plot(stage_3_end, ys[find_nearest(xs,stage_3_end)], color='y', marker='o', linestyle='dashed', linewidth=2, markersize=4)

    if lines:
        col.axvline(x=stage_1_end,color='r',marker='o',linestyle='dashed',linewidth=2,markersize=4)
        col.axvline(x=stage_2_end,color='m',marker='o',linestyle='dashed',linewidth=2,markersize=4)
        col.axvline(x=stage_3_end,color='y',marker='o',linestyle='dashed',linewidth=2,markersize=4)


#send in a list of tupples to plot. each tupple holds (x's and y's) to be plotted
def plots(plots, rocket):

    numPlots=len(plots)
    subplotDim=math.ceil(math.sqrt(numPlots))

    fig, ax = plt.subplots(nrows=subplotDim, ncols=subplotDim)

    index=0

    for row in ax:
        for col in row:
            if index<len(plots):
                col.plot(plots[index][0], plots[index][1])
                col.set_title(plots[index][2])
                showGuides(col,plots[index],rocket,points=True,lines=False)
                index=index+1

def plotVector(xs,listsOfAnges):

    fig = plt.figure()
    sp = plt.subplot(1, 1, 1, projection='polar')

    def update(i):
        indexOfFrame=find_nearest(xs,i)
        sp.clear()
        for j,l in zip(range(len(listsOfAnges)), listsOfAnges):
            sp.text(0.02, 0.90-j*0.05, l[2],color=l[1], transform=sp.transAxes)
            arrow=sp.arrow(0,0,l[0][indexOfFrame],0.8, linewidth=2,color=l[1])
    anim = animation.FuncAnimation(fig, update,frames=len(listsOfAnges[0][0]),interval=frame_interval, blit=False)

    fig.add_subplot(sp)
    plt.show()

