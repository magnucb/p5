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
    pl.grid("on")
    pl.title(r"Energy over time, %dbody %gdt %g$\varepsilon$" % (bodycount, dt, eps) )

    pl.subplot(2, 1, 2)
    pl.plot(timelen, endat[1], label="Potential")
    pl.legend(loc='best')
    pl.xlabel(r"Time $\tau_c$")
    pl.ylabel("Potential energy")
    pl.xlim([0.0, tot_time])
    pl.grid("on")
    pl.savefig("../figs/ClusterEnergiesSys_"+str(bodycount)+"body_dt"+str(int(dt*1000))+"_eps"+str(int(eps*100))+"_dur"+str(int(tot_time))+".png")

def n(r, r0, n0):
    return n0/(1. + (r/float(r0))**4)

def rho(r, r0, rho0):
    return rho0/( (r/float(r0)) * ( ( 1. + r/float(r0) )**2 ) )

def plotVirial(posdat, endat, bodycount, dt, eps, tot_time):
    """
    makes the virial comparison plot and everything else
    """

    bodycount, pos_length, postype = posdat.shape
    pos_timelen = pl.linspace(0, tot_time, pos_length)

    # component wise energies
    kin_en_comp = posdat[:,:,4] # (100 bodies, kin energies at timestep).shape
    pot_en_comp = posdat[:,:,5] # pot energies
    kin_en_ejec_comp = pl.zeros((bodycount, pos_length))
    pot_en_ejec_comp = pl.zeros((bodycount, pos_length))
    masses = posdat[:,0,3]

    # now to exclude ejected bodies
    ejecta_body_array = pl.zeros(bodycount)  # identifies which bodies become ejected at which time
    ejecta_time_array = pl.zeros(pos_length) # measures no. of ejecta at time incr.

    # body summed energies, for use in en. consv. and virial test
    kin_en_sum = pl.zeros(pos_length)
    pot_en_sum = pl.zeros(pos_length)
    kin_en_ejec_sum = pl.zeros(pos_length)
    pot_en_ejec_sum = pl.zeros(pos_length)

    # task f) relevant
    eq_time  = pl.array([4.52])
    eq_pos   = []
    eq_arg   = int(pl.where(pos_timelen >= eq_time[0])[0][0])

    # running through the lists
    for step in pl.arange(0, pos_length):
        for body in pl.arange(0, bodycount):
            if kin_en_comp[body,step] + pot_en_comp[body,step] > 0:
                # move to ejected lists
                kin_en_ejec_comp[body, step] = kin_en_comp[body,step]
                pot_en_ejec_comp[body, step] = pot_en_comp[body,step]

                ejecta_body_array[body] = 1  # identification
                ejecta_time_array[step] = sum(ejecta_body_array)
                                             # stores no. of ejecta at time incr.
                kin_en_comp[body,step] = 0.  # necessary for elimination
                pot_en_comp[body,step] = 0.

        kin_en_sum[step] = sum(kin_en_comp[:,step])
        pot_en_sum[step] = sum(pot_en_comp[:,step])/2.
                                    # factor of 1/2 because system

        kin_en_ejec_sum[step] = sum(kin_en_ejec_comp[:,step])
        pot_en_ejec_sum[step] = sum(pot_en_ejec_comp[:,step])/.2

        """print type(pos_timelen[step]), pos_timelen[step]
        print type(eq_time[0]), eq_time[0]
        print """
        if step == eq_arg:
            for i in range(len(ejecta_body_array)):
                if int(ejecta_body_array[i]) == 0:
                    eq_pos.append(posdat[i, eq_arg, :3])
                            # equilibrium positions, (bodies, positions).shape
    eq_pos = pl.array(eq_pos)
    eq_radia = pl.zeros(len(eq_pos))
    for i in range(len(eq_pos)):
        eq_radia[i] = (eq_pos[i,0]**2 + eq_pos[i,1]**2 + eq_pos[i,2]**2)**.5

    consv_bound_ejec_sum = kin_en_sum + pot_en_sum \
                            + kin_en_ejec_sum + pot_en_ejec_sum


    # --- tasks b) through e) --- #

    pl.figure()
    pl.subplot(2, 1, 1)
    pl.plot(pos_timelen, kin_en_sum, label="Kinetic")
    pl.legend(loc='best')
    pl.ylabel("Kinetic energy")
    pl.xlim([0.0, tot_time])
    pl.title(r"Bound energy over time, %dbody %gdt %g$\varepsilon$" % (bodycount, dt, eps) )
    pl.grid("on")

    pl.subplot(2, 1, 2)
    pl.plot(pos_timelen, pot_en_sum, label="Potential")
    pl.legend(loc='best')
    pl.xlabel(r"Time $\tau_c$")
    pl.ylabel("Potential energy")
    pl.xlim([0.0, tot_time])
    pl.grid("on")
    pl.savefig("../figs/ClusterEnergiesComp_"+str(bodycount)+"body_dt"+str(int(dt*1000))+"_eps"+str(int(eps*100))+"_dur"+str(int(tot_time))+".png")
    
    ### --- ###

    pl.figure()
    pl.subplot(2,1,1)
    pl.title(r"No. of ejecta, %dbody %gdt %g$\varepsilon$" % (bodycount, dt, eps) )
    pl.ylabel(r"Ejection fraction")
    pl.xlim([0.0, tot_time])
    pl.plot(pos_timelen, ejecta_time_array/bodycount, label="Ejecta/Tot")
    pl.legend(loc='best')
    pl.grid("on")

    pl.subplot(2,1,2)

    pl.plot(pos_timelen, kin_en_ejec_sum - pot_en_ejec_sum, label=r"$K_e - V_e$")
    pl.legend(loc='best')
    pl.xlabel(r"Time $\tau_c$")
    pl.ylabel("Energy")
    pl.xlim([0., tot_time])
    pl.title(r"Ejected bodies' energy, %dbody %gdt %g$\varepsilon$" % (bodycount, dt, eps) )
    pl.grid("on")
    pl.savefig("../figs/ClusterEnergiesEjecEn_"+str(bodycount)+"body_dt"+str(int(dt*1000))+"_eps"+str(int(eps*100))+"_dur"+str(int(tot_time))+".png")

    ### --- ###

    pl.figure()
    pl.subplot(2,1,1)
    pl.plot(pos_timelen, consv_bound_ejec_sum, label=r"$K_b + V_b + K_e + V_e$")
    pl.plot(pos_timelen, pl.ones(pos_length)*pot_en_sum[0], linestyle="dashed", color="black", label="Conserved ideal")
    pl.legend(loc='best')
    pl.ylabel("Energy sum")
    pl.xlim([0., tot_time])
    # pl.ylim([pot_en_sum[0] - 0.1*max(consv_bound_ejec_sum), max(consv_bound_ejec_sum) + 0.1*max(consv_bound_ejec_sum)])
    pl.title(r"Energy conservation test, %dbody %gdt %g$\varepsilon$" % (bodycount, dt, eps) )
    pl.grid("on")

    pl.subplot(2,1,2)
    pl.plot(pos_timelen, 2*kin_en_sum/(bodycount-ejecta_time_array) + pot_en_sum/(bodycount-ejecta_time_array), label=r"$2K_b + V_b$")
    pl.plot(pos_timelen, pl.zeros(pos_length), linestyle="dashed", color="black", label="Virial ideal")
    pl.legend(loc='best')
    pl.xlabel(r"Time $\tau_c$")
    pl.ylabel("Virial energy comparison")
    pl.xlim([0.0, tot_time])
    pl.title(r"Virial comparison fit, %dbody %gdt %g$\varepsilon$" % (bodycount, dt, eps) )
    pl.grid("on")
    pl.savefig("../figs/ClusterEnConsvVirial_"+str(bodycount)+"body_dt"+str(int(dt*1000))+"_eps"+str(int(eps*100))+"_dur"+str(int(tot_time))+".png")

    ################################
    # --- beginning of task f) --- #
    ################################

    # 

    colorlist = []
    for i in range(bodycount):
        colorlist.append(random.rand(3,1))

    fig3D = pl.figure()
    ax3D = fig3D.add_subplot(111,projection='3d')

    for body in range(len(eq_pos)):
        ax3D.plot([eq_pos[body,0]], [eq_pos[body,1]], [eq_pos[body,2]], marker="o", color=colorlist[body])

    ax3D.set_title(r"Star cluster 3D %dbody %gdt %g$\varepsilon$, t=%g$\tau_c$" % (bodycount, dt, eps, (tot_time*i/float(pos_length)) ) )
    ax3D.set_xlabel("X-axis [ly]")
    ax3D.set_ylabel("Y-axis [ly]")
    ax3D.set_zlabel("Z-axis [ly]")
    ax3D.set_xlim([-25,25])
    ax3D.set_ylim([-25,25])
    ax3D.set_zlim([-25,25])
    fig3D.savefig("../moviefigs/eps"+str(int(eps*100))+"/ClusterPos_"+str(bodycount)+"body_dt"+str(int(dt*1000))+"_eps"+str(int(eps*100))+"_dur"+str(int(tot_time))+"_movie"+str(i)+".png")

    print "mean eq. radius:", pl.mean(eq_radia)
    print "std dev. radius:", pl.std(eq_radia)

    bincount = 60
    weights, edges = pl.histogram(eq_radia, bins = bincount, range=None, normed=False, weights=None, density=None)
    radia = edges + 0.5*(edges[1]-edges[0])
    
    # lsm finds correct r0
    lengthnumber = 1000
    alphalower  = 0.01
    alphaupper  = 2.
    alpha       = pl.linspace(alphalower, alphaupper, lengthnumber)
    r0lower     = 0.001
    r0upper     = 10.
    r0          = pl.linspace(r0lower, r0upper, lengthnumber)
    
    n0      = max(weights)
    print n0
    n0arg   = pl.argmax(weights)
    r0final = bodycount**(1./3) # assuming it depends somehow on total body number in volume
    nsums   = pl.zeros(lengthnumber)
    
    for alphacount in range(lengthnumber):
        nset = n(edges[:-1]-edges[n0arg], alpha[alphacount]*r0final, n0)
        nsums[alphacount] = sum((nset - weights)**2)

    minarg = pl.argmin(nsums)
    r0final *= alpha[minarg]
    
    pl.figure()
    pl.hist(eq_radia, bins=bincount, label="hist")
    # pl.bar(edges[:-1], weights, label="histogram")
    pl.plot(radia, n(edges, r0final, n0), label="n(r)", color='black', linestyle='dashed', linewidth=5)

    pl.title(r"Radial density of bound bodies, %dbody %gdt %g$\varepsilon$" % (bodycount, dt, eps) )
    pl.xlabel(r"Radius $R_0$")
    pl.ylabel(r"Bodies")
    pl.legend(loc='best')
    pl.grid('on')
    pl.savefig("../figs/ClusterRadDens_"+str(bodycount)+"body_dt"+str(int(dt*1000))+"_eps"+str(int(eps*100))+"_dur"+str(int(tot_time))+".png")


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
    
    try:
        movarg = str(sys.argv[5])
        if movarg != "-m":
            movarg = False
    except IndexError:
        movarg = False
    
    posdat, endat = ColDat(bodycount, dt, eps, tot_time)

    if movarg:
        PlotDat3DMov(posdat, bodycount, dt, eps, tot_time)

    plotEnergySys(endat, bodycount, dt, eps, tot_time)
    plotVirial(posdat, endat, bodycount, dt, eps, tot_time)