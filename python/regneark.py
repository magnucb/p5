from pylab import *

posearth = array([8.841554736579088E-01, 4.675846666013374E-01, -1.788208627053143E-04])
mearth = 0.000003003
velearth = array([-3.03047582e+00, 5.53804088e+00, -2.61593386e-04])

posmerc = array([-3.915735125896518E-01, -8.031632966591709E-02, 2.924535350247253E-02])
mmerc = 1.652e-7
velmerc = array([-4.12705352e-03,  -9.60776278e+00, -7.84947463e-01])

posvenus = array([3.136264982750417E-01, -6.546683031177923E-01, -2.707665055849010E-02])
mvenus = 0.000002447
velvenus = array([6.63254485, 3.12614069, -0.33993686])

posmars = array([1.208658599158087E+00, -6.711650212869039E-01, -4.387238661867205E-02])
mmars = 3.213e-7
velmars = array([2.69039887, 4.90008363, 0.03660091])

posjup = array([-5.425134275608231E+00, -4.965390581079263E-01, 1.233903897528774E-01])
mjup = 0.0009543
veljup = array([0.21935934, -2.61433515, 0.00596296])

possat = array([-2.236264385979587E+00, -9.782434228347928E+00, 2.590917399206301E-01])
msat = 0.0002857
velsat = array([1.87495851, -0.46042927, -0.06665673])

posur = array([1.845409667002747E+01, 7.582158156514705E+00, -2.109158924849341E-01])
mur = 0.00004365
velur = array([-0.55636872, 1.26177202, 0.011894])

posnept = array([2.826704082725938E+01, -9.904409112730836E+00, -4.474799704373976E-01])
mnept = 0.0009543
velnept = array([0.37149543, 1.0889944, -0.03084886])

posplut = array([9.442295163349636E+00, -3.181678067153034E+01, 6.733338703492342E-01])
mplut = 6.58086572e-9
velplut = array([1.1266729, 0.09182691, -0.33562222])

possun = zeros(3)
msun = 1.
velsun = -(mmerc*velmerc + mvenus*velvenus + mearth*velearth + mmars*velmars + mjup*veljup + msat*velsat + mur*velur + mnept*velnept + mplut*velplut)/msun

print velsun

masses = array([msun, mmerc, mvenus, mearth, mmars, mjup, msat, mur, mnept, mplut])
positions = array([possun, posmerc, posvenus, posearth, posmars, posjup, possat, posur, posnept, posplut])

totm = sum(masses)

possun =  -(mmerc*posmerc + mvenus*posvenus + mearth*posearth + mmars*posmars + mjup*posjup + msat*possat + mur*posur + mnept*posnept + mplut*posplut)/msun
print possun

"""
//    CelestialBody &earth = solarSystem.createCelestialBody( vec3(1, 0, 0), vec3(0, 2*M_PI*sqrt(2), 0), 0.000003003, string("Earth") );

//    CelestialBody &mercury = solarSystem.createCelestialBody( vec3(0.39, 0, 0),  vec3(0, 2*M_PI*0.39/0.240846, 0), 0.000002447, string("Mercury"));
//    CelestialBody &venus = solarSystem.createCelestialBody(   vec3(0.728, 0, 0), vec3(0, 2*M_PI*0.728/0.61521, 0), 0.000002447, string("Venus"));
//    CelestialBody &mars = solarSystem.createCelestialBody(    vec3(1.524, 0, 0), vec3(0, 2*M_PI*1.524/1.88089, 0), 3.213e-7, string("Mars"));
//    CelestialBody &jupiter = solarSystem.createCelestialBody( vec3(5.203, 0, 0), vec3(0, 2*M_PI*5.203/11.8653, 0), 0.0009543, string("Jupiter"));
//    CelestialBody &saturn = solarSystem.createCelestialBody(  vec3(9.582, 0, 0), vec3(0, 2*M_PI*9.582/29.46, 0),   0.0002857, string("Saturn"));
//    CelestialBody &uranus = solarSystem.createCelestialBody(  vec3(19.2, 0, 0),  vec3(0, 2*M_PI*19.20/84.04, 0),   0.00004365, string("Uranus"));
//    CelestialBody &neptune = solarSystem.createCelestialBody( vec3(30.05, 0, 0), vec3(0, 2*M_PI*30.05/164.8, 0),   0.0009543, string("Neptune"));
//    CelestialBody &pluto = solarSystem.createCelestialBody(   vec3(39.48, 0, 0), vec3(0, 2*M_PI*39.48/248.1, 0),   0.0009543, string("Pluto"));
"""