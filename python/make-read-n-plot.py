import pylab as pl
import os
import sys
from matplotlib import rc
rc('font',**{'family':'serif'})

def make(address):
    """
    initializes the data
    """
    os.system(address+"/release/Solarsystem.exe") # fitted for my windows dir, hopefully going to get that fixed by today so that directory address applies to linux as well

def read(address):
    """
    reads data from file
    """
    body_names = pl.array(['Sun', 'Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto'])
    bodies_positions = dict.fromkeys(body_names, []) # creates a dict of all relevant objects

    
    with open(address+"/positions.xyz", 'r') as infile:
        data = infile.read()
    data_splat = line.split('\n')

    for line in np.arange(len(data_splat)-1):
        data_splat



if __name__ == '__main__':
    address = "../../build-SolarSystem-Desktop_Qt_5_7_0_MSVC2015_64bit-Release"

    make(address)
    read(address)
