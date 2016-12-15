import pylab as pl
from numpy import random
from mpl_toolkits.mplot3d import Axes3D
import os
import sys
import subprocess
from matplotlib import rc
rc('font',**{'family':'serif'})

def ColDat(bodycount, dt, eps, tot_time):
    """
    takes a data file according to the no. of bodies, and plots appropriate 
    """

    filename = "../data/cluster_"+str(bodycount)+"body_dt"+str(int(dt*1000))+"_eps"+str(int(eps*100))+"_dur"+str(int(tot_time))+".dat"
    x, y, z = pl.loadtxt( filename, usecols=(0,1,2), unpack=True )
    posdat = pl.zeros((bodycount, int(len(x)/bodycount), 3))
            # body, step no., vector
    ibc = 0 # iterative body count
    isc = 0 # iterative step count
    for i in range(len(x)):
        if ibc == (bodycount):
            ibc = 0 # reset to cycle between bodies
            isc += 1

        posdat[ibc, isc] = pl.array([ x[i], y[i], z[i] ]) # store data
        
        ibc += 1 # next body
        
    return posdat

def PlotDat2D(posdat, bodycount, dt, eps, tot_time):
    """
    takes the data created and plots it 
    """
    pl.figure()
    #pl.xkcd()
    for body in range(bodycount):
        paint = random.rand(3,1)
        pl.plot(posdat[body,:,0], posdat[body,:,1], linestyle="-", color=paint)
        pl.plot([posdat[body,-1,0]], [posdat[body,-1,1]], marker="o", color=paint)

    pl.title(r"Star cluster 2D %dbody %gdt %g$\varepsilon$" % (bodycount, dt, eps))
    pl.xlabel("X-axis [AU]")
    pl.ylabel("Y-axis [AU]")
    pl.grid('on')
    pl.axis("equal")
    pl.xlim([-25,25])
    pl.ylim([-25,25])
    pl.savefig("../figs/cluster_"+str(bodycount)+"body_dt"+str(int(dt*1000))+"_eps"+str(int(eps*100))+"_dur"+str(int(tot_time))+".png")
    pl.show()

def PlotDat2DMov(posdat, bodycount, dt, eps, tot_time):
    """
    takes the data created and plots it 
    """
    bodycount, frames, dim = posdat.shape

    colorlist = []
    for i in range(bodycount):
        colorlist.append(random.rand(3,1))
    pl.figure()
    for i in range(frames):
        pl.clf()
        for body in range(bodycount):
            # pl.plot(posdat[body,:i+1,0], posdat[body,:i+1,1], linestyle="-", color=colorlist[body])
            pl.plot([posdat[body,i,0]], [posdat[body,i,1]], marker="o", color=colorlist[body])

        pl.title(r"Star cluster 2D %dbody %gdt %g$\varepsilon$, t=%g$\tau_c$" % (bodycount, dt, eps, (tot_time*i/float(frames)) ) )
        pl.xlabel("X-axis [ly]")
        pl.ylabel("Y-axis [ly]")
        pl.grid('on')
        pl.axis('equal')
        pl.xlim([-25,25])
        pl.ylim([-25,25])
        pl.savefig("../moviefigs/cluster_"+str(bodycount)+"body_dt"+str(int(dt*1000))+"_eps"+str(int(eps*100))+"_dur"+str(int(tot_time))+"_movie"+str(i)+".png")

def PlotDat3DMov(posdat, bodycount, dt, eps, tot_time):
    """
    takes the data created and plots it 
    """
    bodycount, frames, dim = posdat.shape

    colorlist = []
    for i in range(bodycount):
        colorlist.append(random.rand(3,1))

    fig3D = pl.figure()
    ax3D = fig3D.add_subplot(111,projection='3d')
    # pl.xkcd()
    for i in range(frames):
        ax3D.cla()
        for body in range(bodycount):
            # ax3D.plot(posdat[body,:i+1,0], posdat[body,:i+1,1], posdat[body,:i+1,2], linestyle="-", color=colorlist[body])
            ax3D.plot([posdat[body,i,0]], [posdat[body,i,1]], [posdat[body,i,2]], marker="o", color=colorlist[body])

        ax3D.set_title(r"Star cluster 3D %dbody %gdt %g$\varepsilon$, t=%g$\tau_c$" % (bodycount, dt, eps, (tot_time*i/float(frames)) ) )
        ax3D.set_xlabel("X-axis [ly]")
        ax3D.set_ylabel("Y-axis [ly]")
        ax3D.set_zlabel("Z-axis [ly]")
        ax3D.set_xlim([-25,25])
        ax3D.set_ylim([-25,25])
        ax3D.set_zlim([-25,25])
        fig3D.savefig("../moviefigs/cluster_"+str(bodycount)+"body_dt"+str(int(dt*1000))+"_eps"+str(int(eps*100))+"_dur"+str(int(tot_time))+"_movie"+str(i)+".png")

def MakeMov(bodycount):
    """
    creates a movie - does not work
    """
    subprocess.call('convert -delay 8/100 -loop 0 ../moviefigs/cluster_%dbody_movie*.png ../movies/cluster_%dbody.gif' % (bodycount, bodycount), shell=True)


if __name__ == '__main__':
    try:
        bodycount = int(sys.argv[1])
    except IndexError:
        bodycount = int(raw_input("Number of bodies in the cluster: "))
    try:
        dt = float(sys.argv[2])
    except IndexError:
        dt = float(raw_input("Delta time, dt: "))
    try:
        eps = float(sys.argv[3])
    except IndexError:
        eps = float(raw_input("Epsilon: "))
    try:
        tot_time = float(sys.argv[4])
    except IndexError:
        tot_time = float(raw_input("Duration: "))
    
    posdat = ColDat(bodycount, dt, eps, tot_time)

    PlotDat3DMov(posdat, bodycount, dt, eps, tot_time)