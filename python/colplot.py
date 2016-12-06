import pylab as pl
from numpy import random
from mpl_toolkits.mplot3d import Axes3D
import os
import sys
from matplotlib import rc
rc('font',**{'family':'serif'})

def ColDat(bodycount):
    """
    takes a data file according to the no. of bodies, and plots appropriate 
    """

    filename = "../data/cluster_"+str(bodycount)+"body.dat"
    x, y, z = pl.loadtxt( filename, usecols=(0,1,2), unpack=True )
    posdat = pl.zeros((bodycount, int(len(x)/bodycount), 3))
            # body, step no., vector
    ibc = 0 # iterative body count
    isc = 0 # iterative step count
    for i in range(len(x)):
        if ibc == (bodycount):
            ibc = 0 # reset to cycle between bodies
            isc += 1
        print "line", i, " - body", ibc, " - step", isc
        print 
        posdat[ibc, isc] = pl.array([ x[i], y[i], z[i] ]) # store data
        
        ibc += 1 # next body
        
    return posdat

def PlotDat2D(posdat, bodycount):
    """
    takes the data created and plots it 
    """
    pl.figure()
    for body in range(bodycount):
        paint = random.rand(3,1)
        pl.plot(posdat[body,:,0], posdat[body,:,1], linestyle="-", color=paint)
        pl.plot([posdat[body,-1,0]], [posdat[body,-1,1]], marker="o", color=paint)

    pl.title("Star cluster orbits, 2D")
    pl.xlabel("X-axis")
    pl.ylabel("Y-axis")
    pl.grid('on')
    pl.savefig("../figs/cluster_"+str(bodycount)+"body.png")
    pl.show()



if __name__ == '__main__':
    try:
        bodycount = sys.argv[1]
    except IndexError:
        bodycount = int(raw_input("Number of bodies in the cluster: "))

    posdat = ColDat(bodycount)

    PlotDat2D(posdat, bodycount)