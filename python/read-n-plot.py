import pylab as pl
from mpl_toolkits.mplot3d import Axes3D
import os
import sys
from matplotlib import rc
rc('font',**{'family':'serif'})

def read(address):
    """
    reads data from file
    """
    body_names = pl.array(['Sun', 'Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto'])
    bodies_positions = {}

    ###### REMEMBER TO EDIT THIS WHEN PLOTTING DIFFERENT STUFF
    with open(address+"/positions_verlet_SunEarthJupiterMercuryVenusMarsSaturnUranusNeptunePluto.xyz", 'r') as infile:
        ###### REMEMBER TO EDIT THIS WHEN PLOTTING DIFFERENT STUFF
        data = infile.read()
    
    data_splat = data.split('\n')
    file_len = len(data_splat)

    for l in pl.arange(file_len-1):
        line = pl.array(data_splat[l].split(' '))
        try:
            bodies_positions[line[0]].append(line[1:].astype(pl.float64))
        except KeyError:
            bodies_positions[line[0]] = [line[1:].astype(pl.float64)]
        except:
            sys.exit('Error in dictionary making')
        
    for key in bodies_positions:
        bodies_positions[key] = pl.array(bodies_positions[key])

    return body_names, bodies_positions


def plot(keys, bodies_with_positions):
    """
    plots all present celestial bodies_positions
    """
    colors = {'Sun':'y', 'Mercury':'k', 'Venus':'0.75', 'Earth':'b', 'Mars':'r', 'Jupiter':'#FF5733', 'Saturn':'#C88617', 'Uranus':'c', 'Neptune':'#6A82FF', 'Pluto':'g'}
    linestyles = {'Sun': '-', 'Mercury':'-', 'Venus':'-', 'Earth':'-', 'Mars':'-', 'Jupiter':'-', 'Saturn':'-', 'Uranus':'-', 'Neptune':'-', 'Pluto':'-'}
    pointstyles = {'Sun': '*', 'Mercury':'o', 'Venus':'o', 'Earth':'o', 'Mars':'o', 'Jupiter':'o', 'Saturn':'o', 'Uranus':'o', 'Neptune':'o', 'Pluto':'o'}
    pl.rcParams['legend.fontsize'] = 11
    
    #pl.xkcd()
    fig = pl.figure()
    ax = fig.gca(projection='3d')
    for i in bodies_positions:
        xyz = bodies_positions[i]
        ax.plot(xyz[:,0], xyz[:,1], xyz[:,2], linestyles[i], label=i, color=colors[i])
        #ax.plot([xyz[0,0]], [xyz[0,1]], [xyz[0,2]], pointstyles[i], color=colors[i])
        ax.plot([xyz[-1,0]], [xyz[-1,1]], [xyz[-1,2]], pointstyles[i], color=colors[i])
    ax.set_aspect('equal')
    # system = "inner"
    system = "jupiter"
    # system = 'merc'
    # system = 0
    if system == "inner":
        ax.set_xlim([-1.2,1.2])
        ax.set_ylim([-1.2,1.2])
        ax.set_zlim([-1.2,1.2])
    elif system == "jupiter":
        ax.set_xlim([-3.5,3.5])
        ax.set_ylim([-3.5,3.5])
        ax.set_zlim([-3.5,3.5])
    elif system == "merc":
        ax.set_xlim([-0.3,0.3])
        ax.set_ylim([-0.3,0.3])
        ax.set_zlim([-0.3,0.3])
    else:                           # plot comprehension
        ax.set_xlim([-30.2,30.2])
        ax.set_ylim([-30.2,30.2])
        ax.set_zlim([-30.2,30.2])
    ax.grid('on')
    ax.set_xlabel('X-axis [AU]')
    ax.set_ylabel('Y-axis [AU]')
    ax.set_zlabel('Z-axis [AU]')
    ax.set_title(r'Solar system, inner system view, Verlet, $1\cdot10^2$ yrs') ###### REMEMBER TO EDIT THIS WHEN PLOTTING DIFFERENT STUFF
    ax.legend(loc='lower left')
    pl.show()

    # pl.figure()
    # for i in bodies_positions:
    #     xyz = bodies_positions[i]
    #     pl.plot(xyz[:,0], xyz[:,1], linestyles[i], label=i, color=colors[i])
    #     pl.plot([xyz[0,0]], [xyz[0,1]], pointstyles[i], color=colors[i])
    #     pl.plot([xyz[-1,0]], [xyz[-1,1]], pointstyles[i], color=colors[i])
    # pl.xlabel('X-axis [AU]')
    # pl.ylabel('Y-axis [AU]')
    # pl.title(r'Sun+Earth, Verlet, $10^3$ yrs') ###### REMEMBER TO EDIT THIS WHEN PLOTTING DIFFERENT STUFF
    # pl.legend(loc='lower left')
    # pl.grid('on')
    # pl.axes().set_aspect('equal', 'datalim')
    # pl.savefig('sun+earth_verlet_n1e6_v414.png')
    

    body_string = ""
    for key in bodies_positions:
        body_string += key

    # pl.savefig('solar_system_with_%s.png' % body_string, dpi=300) # doesn't work


if __name__ == '__main__':
    
    address = os.getcwd()+"/../build-SolarSystem-Desktop_Qt_5_7_0_MSVC2015_64bit-Release"

    keys, bodies_positions = read(address)
    plot(keys, bodies_positions)