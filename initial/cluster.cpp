#define _USE_MATH_DEFINES
#include "Cluster.h"
#include <cmath>
#include <iostream>
using namespace std;

Cluster::Cluster(double RadLim, double epsilon) :
    m_kineticEnergy(0),
    m_potentialEnergy(0),
    m_totM(0)
{
    R0 = RadLim;
    eps = epsilon;
}

CelestialBody& Cluster::createCelestialBody(vec3 position, vec3 velocity, double mass) {
    m_bodies.push_back( CelestialBody(position, velocity, mass) );
    m_totM += mass;
    return m_bodies.back(); // Return reference to the newest added celstial body
}

void Cluster::calculateForcesAndEnergy()
{
    m_kineticEnergy = 0;
    m_potentialEnergy = 0;
    m_angularMomentum.zeros();
    m_momentum.zeros();

    double m_G = M_PI*M_PI*R0*R0*R0/(8.0*m_totM);
    // double angconst = 3.0/pow(63197.8,2); // 3 / c**2, [c] = AU/yr

    for(CelestialBody &body : m_bodies) {
        // Reset forces on all bodies
        body.force.zeros();
    }

    for(int i=0; i<numberOfBodies(); i++) {
        CelestialBody &body1 = m_bodies[i];
        for(int j=i+1; j<numberOfBodies(); j++) {
            CelestialBody &body2 = m_bodies[j];
            vec3 deltaRVector = body1.position - body2.position;
            double dr = deltaRVector.length();

//            vec3 deltaVVector = body1.velocity - body2.velocity;
//            double l2 = angularMomentum(deltaRVector, deltaVVector).lengthSquared();


            // Calculate the force and potential energy here
            // vec3 Force = (-m_G*body1.mass*body2.mass*deltaRVector)*(1 + angconst*l2/(dr*dr))/(dr*dr*dr);9
            vec3 Force = -m_G*body1.mass*body2.mass * deltaRVector
                         /(dr*dr + eps*eps);
            body1.force += Force;
            body2.force -= Force;
        }
        m_momentum += body1.mass*body1.velocity;
        m_angularMomentum += body1.position.cross(m_momentum);
        m_kineticEnergy += 0.5*body1.mass*body1.velocity.lengthSquared();
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

void Cluster::writeToFile(string filename)
{
    if(!m_file.good()) {
        m_file.open(filename.c_str(), ofstream::out);
        if(!m_file.good()) {
            cout << "Error opening file " << filename << ". Aborting!" << endl;
            terminate();
        }
    }

    for(CelestialBody &body : m_bodies) {
        m_file << " " << body.position.x() << " " << body.position.y() << " " << body.position.z() << "\n";
    }
}

vec3 Cluster::angularMomentum(vec3 position, vec3 velocity) const
{
    return position.cross(velocity);//m_angularMomentum;
}

std::vector<CelestialBody> &Cluster::bodies()
{
    return m_bodies;
}
