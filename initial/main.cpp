#define _USE_MATH_DEFINES
#include <iostream>
#include <iomanip>
#include <string>
#include <cmath>
#include <fstream>
#include <time.h>
#include <random>

#include "cluster.h"
#include "verlet.h"

using namespace std;

int main(int numArguments, char **arguments){

    //int numTimesteps = 1000;
    double dt = 0.001;
    int NumOfBodies = 10;
    double R0 = 20.0;
    double avg_Msun = 10.0;
    double std_Msun = 1.0;
    double eps = 0.0;
    clock_t t_start, t_stop;
    double time;
    int tot_time = 4;

//    if (numArguments >= 2) {
//        numTimesteps = atoi(arguments[1]);
//    }
    if (numArguments >= 2) {
        NumOfBodies = atoi(arguments[1]);
    }
    if (numArguments >= 3) {
        dt = atof(arguments[2]);
    }
    if (numArguments >= 4) {
        eps = atof(arguments[3]);
    }
    if (numArguments >= 5) {
        tot_time = atoi(arguments[4]);
    }
    int numTimesteps = 1/dt;
    cout << "Using Verlet method w/ " << numTimesteps
         << " time steps per tau_c." << endl;

    // Initializing random device and random number generators
    std::random_device rd;
    std::mt19937_64 gen(rd());
    std::uniform_real_distribution<double> uniform_RNG(0.0,1.0);
        // Uniform probability distribution - position, scales with R0 later
    std::normal_distribution<double> gaussian_RNG(avg_Msun, std_Msun);
        // Gaussian probability distribution - masses

    // Use with: cluster.createCelestialBody( position, velocity, mass );
    // creating the base cluster
    Cluster cluster(eps);
    for (int i=0; i<NumOfBodies; i++){

        double r = uniform_RNG(gen);
        double theta = M_PI*uniform_RNG(gen);
        double phi = 2*M_PI*uniform_RNG(gen);

        double x = R0*r*sin(theta)*cos(phi);
        double y = R0*r*sin(theta)*sin(phi);
        double z = R0*r*cos(theta); // maybe put this as func in class struct

        cluster.createCelestialBody( vec3(x,y,z), vec3(0,0,0),
                                     gaussian_RNG(gen));
    }
    cluster.Gengage(R0);//just to initialize the value of G, dep on tot_mass
    string filename = "..\\data\\cluster_"
            +to_string(NumOfBodies)+"body_dt"+to_string(int(dt*1000))+
            "_eps"+to_string(int(eps*100))+
            "_dur"+to_string(tot_time)+".dat";

    Verlet integrator(dt);
    t_start = clock();
    cluster.writeToFile(filename);
    for(int timestep=0; timestep<tot_time*numTimesteps; timestep++) {
        integrator.integrateOneStep(cluster);
        if (timestep%60 == 0) cluster.writeToFile(filename); // less size
    }

    t_stop = clock();

    cout << "I just created my first galactic cluster that has " << cluster.bodies().size() << " objects." << endl;

    time = abs(t_start - t_stop)/( (double) CLOCKS_PER_SEC);
    cout << "time of integration method: t=" << time << " s" << endl;

    return 0;
}

