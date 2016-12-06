import os
import sys

def make(address):
    """
    initializes the data
    """
    os.system(str(address)+"/release/Solarsystem.exe %s %s" % (sys.argv[1], sys.argv[2])) # fitted for my windows dir, hopefully going to get that fixed by today so that directory address applies to linux as well

if __name__ == '__main__':
    address = os.getcwd()+"/../build-SolarSystem-Desktop_Qt_5_7_0_MSVC2015_64bit-Release"

    make(address)