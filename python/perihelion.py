import pylab as pl
from mpl_toolkits.mplot3d import Axes3D
import os
import sys
from matplotlib import rc
rc('font',**{'family':'serif'})

def do_peri():
    """
    reads data from file
    """
    body_names = pl.array(['Sun', 'Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto'])
    bodies_positions = {}

    address = os.getcwd()+"/../build-SolarSystem-Desktop_Qt_5_7_0_MSVC2015_64bit-Release"

    with open(address+"/perihelion_positions.xyz", 'r') as infile:
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

    Mercury_pos = bodies_positions['Mercury']
    thetas_p = pl.arctan(Mercury_pos[:,1]/Mercury_pos[:,0])#assuming these come out in radians

    subtraction = abs(thetas_p[-1] - thetas_p[0])#total precession angle difference over 100yrs
    subtraction *= 360.*60/(2*pl.pi)# this should be the correct conversion
    print subtraction

if __name__ == '__main__':
    do_peri()