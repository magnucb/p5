#ifndef CLUSTER_H
#define CLUSTER_H

#include "celestialbody.h"
#include <vector>
#include <string>
#include <fstream>


class Cluster
{
public:
    Cluster(double epsilon);
    CelestialBody &createCelestialBody(vec3 position, vec3 velocity, double mass);
    void Gengage(double R0);
    void calculateForcesAndEnergy();
    int numberOfBodies() const;


    double totalEnergy() const;
    double potentialEnergy() const;
    double kineticEnergy() const;
    void writeToFile(std::string filename);

    vec3 angularMomentum(vec3 position, vec3 velocity) const;
    vec3 momentum() const;
    std::vector<CelestialBody> &bodies();
    double eps;
    double m_G;

private:
    std::vector<CelestialBody> m_bodies;
    vec3 m_momentum;
    vec3 m_angularMomentum;
    std::ofstream m_file;
    double m_kineticEnergy;
    double m_potentialEnergy;
    double m_totM;
};

#endif // CLUSTER_H
