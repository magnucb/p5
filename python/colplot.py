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

    filename = "../data/ClusterPos_"+str(bodycount)+"body_dt"+str(int(dt*1000))+"_eps"+str(int(eps*100))+"_dur"+str(int(tot_time))+".dat"
    x, y, z, mass, kin, pot = pl.loadtxt( filename, usecols=(0,1,2, 3, 4,5), unpack=True )
    posdat = pl.zeros((bodycount, int(len(x)/bodycount), 6))
            # (body, step no., vector etc).shape
    ibc = 0 # iterative body count
    isc = 0 # iterative step count
    for i in range(len(x)):
        if ibc == (bodycount):
            ibc = 0 # reset to cycle between bodies
            isc += 1

        posdat[ibc, isc] = pl.array([ x[i], y[i], z[i], mass[i], kin[i], pot[i] ]) # store data
        
        ibc += 1 # next body
    
    enName = "../data/ClusterEn_"+str(bodycount)+"body_dt"+str(int(dt*1000))+"_eps"+str(int(eps*100))+"_dur"+str(int(tot_time))+".dat"

    kin, pot = pl.loadtxt( enName, usecols=(0,1), unpack=True )
    endat = pl.array([kin, pot]) # pl.zeros((2, len(kin)))

    return posdat, endat

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
        fig3D.savefig("../moviefigs/ClusterPos_"+str(bodycount)+"body_dt"+str(int(dt*1000))+"_eps"+str(int(eps*100))+"_dur"+str(int(tot_time))+"_movie"+str(i)+".png")

def plotEnergySys(endat, bodycount, dt, eps, tot_time):
    """
    plots energy over time
    """
    entype, length = endat.shape
    timelen = pl.linspace(0, tot_time, length)

    pl.figure()
    pl.subplot(2, 1, 1)
    pl.plot(timelen, endat[0], label="Kinetic")
    pl.legend(loc='best')
    pl.ylabel("Kinetic energy")
    pl.xlim([0.0, tot_time])
    pl.title(r"Energy over time, %dbody %gdt %g$\varepsilon$" % (bodycount, dt, eps) )

    pl.subplot(2, 1, 2)
    pl.plot(timelen, endat[1], label="Potential")
    pl.legend(loc='best')
    pl.xlabel(r"Time $\tau_c$")
    pl.ylabel("Potential energy")
    pl.xlim([0.0, tot_time])
    pl.savefig("../figs/ClusterEnergiesSys_"+str(bodycount)+"body_dt"+str(int(dt*1000))+"_eps"+str(int(eps*100))+"_dur"+str(int(tot_time))+".png")

def plotVirial(posdat, endat, bodycount, dt, eps, tot_time):
    """
    makes the virial comparison plot
    """
    # entype, en_length = endat.shape
    # en_timelen = pl.linspace(0, tot_time, en_length)

    bodycount, pos_length, postype = posdat.shape
    pos_timelen = pl.linspace(0, tot_time, pos_length)

    # component wise energies
    kin_en_comp = posdat[:,:,4] # (100 bodies, kin energies at timestep).shape
    pot_en_comp = posdat[:,:,5] # pot energies
    total_comp = kin_en_comp + pot_en_comp
    masses = posdat[:,0,3]

    # now to exclude ejected particles
    ejecta_body_array = pl.zeros(bodycount)  # identifies which bodies become ejected
    ejecta_time_array = pl.zeros(pos_length) # measures no. of ejecta at time incr.
    for step in pl.arange(0, pos_length):
        for body in pl.arange(0, bodycount):
            if kin_en_comp[body,step] > abs(pot_en_comp[body,step]):
                kin_en_comp[body,step] = 0.  # necessary for elimination
                ejecta_body_array[body] = 1  # identification
                ejecta_time_array[step] = sum(ejecta_body_array)
                                             # stores no. of ejecta at time incr.

    # body summed energies
    kin_en_sum = pl.zeros(pos_length)
    pot_en_sum = pl.zeros(pos_length)
    for timestep in pl.arange(0, pos_length):
        kin_en_sum[timestep] = sum(kin_en_comp[:,timestep])
        pot_en_sum[timestep] = sum(pot_en_comp[:,timestep])

    
    pl.figure()
    pl.subplot(2, 1, 1)
    pl.plot(pos_timelen, kin_en_sum, label="Kinetic")
    pl.legend(loc='best')
    pl.ylabel("Kinetic energy")
    pl.xlim([0.0, tot_time])
    pl.title(r"Energy over time, %dbody %gdt %g$\varepsilon$" % (bodycount, dt, eps) )

    pl.subplot(2, 1, 2)
    pl.plot(pos_timelen, pot_en_sum/2., label="Potential")
    pl.legend(loc='best')
    pl.xlabel(r"Time $\tau_c$")
    pl.ylabel("Potential energy")
    pl.xlim([0.0, tot_time])
    pl.savefig("../figs/ClusterEnergiesComp_"+str(bodycount)+"body_dt"+str(int(dt*1000))+"_eps"+str(int(eps*100))+"_dur"+str(int(tot_time))+".png")
    
    ### --- ###

    pl.figure()
    pl.subplot(2,1,1)
    pl.title(r"No. of ejecta, %dbody %gdt %g$\varepsilon$" % (bodycount, dt, eps) )
    pl.ylabel(r"Ejection fraction")
    pl.xlim([0.0, tot_time])
    pl.plot(pos_timelen, ejecta_time_array/bodycount, label="Ejecta/Tot")
    pl.legend(loc='best')


    pl.subplot(2,1,2)
    pl.plot(pos_timelen, 2*kin_en_sum + pot_en_sum/2, label="2<K> + <U>, Virial")
    pl.plot(pos_timelen, pl.zeros(pos_length), linestyle="dashed", color="black", label="Virial ideal")
    pl.legend(loc='best')
    pl.xlabel(r"Time $\tau_c$")
    pl.ylabel("Potential energy")
    pl.xlim([0.0, tot_time])
    pl.title(r"Virial comparison fit, %dbody %gdt %g$\varepsilon$" % (bodycount, dt, eps) )
    pl.savefig("../figs/ClusterEnergiesVirial_"+str(bodycount)+"body_dt"+str(int(dt*1000))+"_eps"+str(int(eps*100))+"_dur"+str(int(tot_time))+".png")




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
    
    posdat, endat = ColDat(bodycount, dt, eps, tot_time)

    PlotDat3DMov(posdat, bodycount, dt, eps, tot_time)
    plotEnergySys(endat, bodycount, dt, eps, tot_time)
    plotVirial(posdat, endat, bodycount, dt, eps, tot_time)