"""Physics engine for N-body simulation."""

from physics.particle import Particle
from physics.gravity import compute_gravity_direct
from physics.barnes_hut import BarnesHutTree
from physics.integrator import LeapfrogIntegrator

__all__ = ['Particle', 'compute_gravity_direct', 'BarnesHutTree', 'LeapfrogIntegrator']
