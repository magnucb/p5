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
    void calculateBodyEnergy();
    int numberOfBodies() const;


    double totalEnergy() const;
    double potentialEnergy() const;
    double kineticEnergy() const;
    void writeToFile(std::string filename);
    void EnergyToFile(std::string filename);

    vec3 angularMomentum(vec3 position, vec3 velocity) const;
    vec3 momentum() const;
    std::vector<CelestialBody> &bodies();
    std::vector<CelestialBody> m_bodies;
    double eps;
    double m_G;

private:
    vec3 m_momentum;
    vec3 m_angularMomentum;
    std::vector<double> PotEnVec;
    std::vector<double> KinEnVec;
    std::ofstream m_file;
    std::ofstream en_file;
    double m_kineticEnergy;
    double m_potentialEnergy;
    double m_totM;
};

#endif // CLUSTER_H
