#define _USE_MATH_DEFINES
#include "Cluster.h"
#include <cmath>
#include <iostream>
using namespace std;

Cluster::Cluster(double epsilon) :
    m_kineticEnergy(0),
    m_potentialEnergy(0),
    m_totM(0),
    m_G(0)
{
    eps = epsilon;
}

CelestialBody& Cluster::createCelestialBody(vec3 position, vec3 velocity, double mass) {
    m_bodies.push_back( CelestialBody(position, velocity, mass) );
    m_totM += mass;
    return m_bodies.back(); // Return reference to the newest added celstial body
}

void Cluster::Gengage(double R0){
    m_G = M_PI*M_PI*R0*R0*R0/(8.0*m_totM);
    PotEnVec.resize(numberOfBodies(), 0);
    KinEnVec.resize(numberOfBodies(), 0);
}

void Cluster::calculateForcesAndEnergy(){
    // Calculates forces between objects and total energies
    m_kineticEnergy = 0;
    m_potentialEnergy = 0;

    for(CelestialBody &body : m_bodies) {
        // Reset forces on all bodies
        body.force.zeros();
    }

    for(int i=0; i<numberOfBodies(); i++) {
        CelestialBody &body1 = m_bodies[i];
        for(int j=i+1; j<numberOfBodies(); j++) {
            // setting up variables
            CelestialBody &body2 = m_bodies[j];
            vec3 deltaRVector = body1.position - body2.position;
            double dr = deltaRVector.length();

            // Force
            vec3 Force = -m_G*body1.mass*body2.mass * deltaRVector/dr
                         /(dr*dr + eps*eps);
            body1.force += Force;
            body2.force -= Force;

            // Pot en rel. to 2 masses, added to tot
            m_potentialEnergy -= m_G*body1.mass*body2.mass / dr;
        }
        // Kin en rel to one mass added to tot
        m_kineticEnergy += 0.5*body1.mass*body1.velocity.lengthSquared();
    }
}

void Cluster::calculateBodyEnergy(){
    // Making a function to calculate individual bodies' energies
    // so to find which are ejected and store their energies

    for(int i=0; i<numberOfBodies(); i++) {
        CelestialBody &body1 = m_bodies[i];
        // resetting variables
        double body_pot = 0;
        double body_kin = 0;

        for(int j=0; j<numberOfBodies(); j++) {
            if (j != i){
                // setting up variables
                CelestialBody &body2 = m_bodies[j];
                vec3 deltaRVector = body1.position - body2.position;
                double dr = deltaRVector.length();

                // Pot. en .of body added up
                body_pot -= m_G*body1.mass*body2.mass / dr;
            }
        }
        // Defining the bodies' energies
        PotEnVec[i] = body_pot;

        body_kin = 0.5*body1.mass*body1.velocity.lengthSquared();
        KinEnVec[i] = body_kin;
    }
}

int Cluster::numberOfBodies() const
{
    return m_bodies.size();
}

double Cluster::totalEnergy() const
{
    return m_kineticEnergy + m_potentialEnergy;
}

double Cluster::potentialEnergy() const
{
    return m_potentialEnergy;
}

double Cluster::kineticEnergy() const
{
    return m_kineticEnergy;
}

void Cluster::writeToFile(string filename){
    if(!m_file.good()) {
        m_file.open(filename.c_str(), ofstream::out);
        if(!m_file.good()) {
            cout << "Error opening file " << filename << ". Aborting!" << endl;
            terminate();
        }
    }

    int drac = 0;
    for(CelestialBody &body : m_bodies) {
        m_file << " " << body.position.x() <<
                  " " << body.position.y() <<
                  " " << body.position.z() <<
                  " " << body.mass <<
                  " " << KinEnVec[drac]    <<
                  " " << PotEnVec[drac]    << "\n";
        drac += 1;
    }
}

void Cluster::EnergyToFile(string filename){
    if(!en_file.good()) {
        en_file.open(filename.c_str(), ofstream::out);
        if(!en_file.good()) {
            cout << "Error opening file " << filename << ". Aborting!" << endl;
            terminate();
        }
    }
    // because the integrator's energies are half a step behind
    calculateForcesAndEnergy();
    en_file << " " << m_kineticEnergy <<
               " " << m_potentialEnergy << "\n";
}


vec3 Cluster::angularMomentum(vec3 position, vec3 velocity) const
{
    return position.cross(velocity);//m_angularMomentum;
}

std::vector<CelestialBody> &Cluster::bodies()
{
    return m_bodies;
}
