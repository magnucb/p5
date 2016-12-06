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

int main(int numArguments, char **arguments)
{
    int numTimesteps = 1000;
    double dt = 0.001;
    int NumOfBodies = 10;
    double R0 = 20.0;
    double eps = 0.0;
    clock_t t_start, t_stop;
    double time;

    if (numArguments >= 2) {
        numTimesteps = atoi(arguments[1]);
    }
    if (numArguments >= 3) {
        NumOfBodies = atoi(arguments[2]);
    }
    cout << "Using Verlet method w/ " << numTimesteps
         << " time steps." << endl;

    // Initializing random device and random number generators
    std::random_device rd;
    std::mt19937_64 gen(rd());
    std::uniform_real_distribution<double> uniform_RNG(0.0,R0);
        // Uniform probability distribution
    std::normal_distribution<double> gaussian_RNG(10,1);
        // Gaussian probability distribution

    // Use with: cluster.createCelestialBody( position, velocity, mass );
    // creating the base cluster
    Cluster cluster(eps);
    for (int i=0; i<NumOfBodies; i++){
        vec3 pos(uniform_RNG(gen), uniform_RNG(gen), uniform_RNG(gen));
        cluster.createCelestialBody( pos, vec3(0,0,0), gaussian_RNG(gen));
    }

    string filename = "..\\data\\cluster_"+to_string(NumOfBodies)+"body.dat";
    Verlet integrator(dt);
    t_start = clock();
    cluster.writeToFile(filename);
    for(int timestep=0; timestep<numTimesteps; timestep++) {
        integrator.integrateOneStep(cluster);
        if (timestep%100 == 0) cluster.writeToFile(filename); // less size
    }

    t_stop = clock();

    cout << "I just created my first galactic cluster that has " << cluster.bodies().size() << " objects." << endl;

    time = abs(t_start - t_stop)/( (double) CLOCKS_PER_SEC);
    cout << "time of integration method: t=" << time << " s" << endl;

    return 0;
}

