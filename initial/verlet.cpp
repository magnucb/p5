#define _USE_MATH_DEFINES
#include "verlet.h"
#include "cluster.h"
#include <math.h>


Verlet::Verlet(double dt) :
    m_dt(dt)
{

}

void Verlet::integrateOneStep(Cluster &system)
{
    system.calculateForcesAndEnergy();
    // Velocity Verlet
    for (CelestialBody &body :system.bodies()) {
        // half-step computation
        body.velocity += (m_dt/2.0)*(body.force / body.mass);
        body.position += body.velocity*m_dt;
    }
    system.calculateForcesAndEnergy();
    for (CelestialBody &body :system.bodies()) {
        // the new velocity
        body.velocity += (m_dt/2.0)*(body.force / body.mass);
    }
}
