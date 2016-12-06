import pylab as pl

class SolarSystem(CelestialBody):
    def __init__(self):
        CelestialBody.__init__(self):




class CelestialBody:
    def __init__(self, pos_, vel_, mass_):
        self.pos = pos_
        self.vec = vel_
        self.mass = mass_




solarSystem = SolarSystem

solarSystem.Sun = 