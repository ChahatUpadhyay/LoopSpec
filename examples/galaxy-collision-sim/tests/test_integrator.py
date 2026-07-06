"""
Tests for leapfrog integrator.
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from physics.particle import Particle
from physics.integrator import LeapfrogIntegrator
from physics.gravity import compute_total_energy


def test_integrator_energy_conservation():
    """Test that leapfrog integrator conserves energy."""
    # Create a simple two-body system
    p1 = Particle(
        position=np.array([0.0, 0.0, 0.0]),
        velocity=np.array([0.0, 0.5, 0.0]),
        mass=1.0,
        color=(1.0, 1.0, 1.0),
        radius=0.1
    )
    p2 = Particle(
        position=np.array([1.0, 0.0, 0.0]),
        velocity=np.array([0.0, -0.5, 0.0]),
        mass=1.0,
        color=(1.0, 1.0, 1.0),
        radius=0.1
    )
    
    integrator = LeapfrogIntegrator(dt=0.01, adaptive=False, G=1.0, softening=0.1)
    
    # Compute initial energy
    initial_energy = compute_total_energy([p1, p2], softening=0.1, G=1.0)
    
    # Integrate for 1000 steps
    particles = [p1, p2]
    for _ in range(1000):
        integrator.step(particles)
    
    # Compute final energy
    final_energy = compute_total_energy(particles, softening=0.1, G=1.0)
    
    # Energy drift should be less than 1%
    energy_drift = abs(final_energy - initial_energy) / abs(initial_energy)
    assert energy_drift < 0.01


def test_integrator_adaptive_timestep():
    """Test that adaptive timestep adjusts based on particle proximity."""
    # Create particles that will get close
    p1 = Particle(
        position=np.array([0.0, 0.0, 0.0]),
        velocity=np.array([0.1, 0.0, 0.0]),
        mass=1.0,
        color=(1.0, 1.0, 1.0),
        radius=0.1
    )
    p2 = Particle(
        position=np.array([1.0, 0.0, 0.0]),
        velocity=np.array([-0.1, 0.0, 0.0]),
        mass=1.0,
        color=(1.0, 1.0, 1.0),
        radius=0.1
    )
    
    integrator = LeapfrogIntegrator(dt=0.01, adaptive=True, min_dt=1e-6, max_dt=0.1, G=1.0, softening=0.1)
    
    particles = [p1, p2]
    
    # Get timestep when particles are far apart
    dt_far = integrator.get_adaptive_timestep(particles)
    
    # Move particles closer
    p2.position = np.array([0.1, 0.0, 0.0])
    
    # Get timestep when particles are close
    dt_close = integrator.get_adaptive_timestep(particles)
    
    # Timestep should be smaller when particles are closer
    assert dt_close < dt_far


def test_integrator_reset():
    """Test that integrator reset clears state."""
    p1 = Particle(
        position=np.array([0.0, 0.0, 0.0]),
        velocity=np.array([0.0, 0.0, 0.0]),
        mass=1.0,
        color=(1.0, 1.0, 1.0),
        radius=0.1
    )
    
    integrator = LeapfrogIntegrator(dt=0.01, G=1.0, softening=0.1)
    
    # Take a step
    integrator.step([p1])
    
    # Reset
    integrator.reset()
    
    # Accelerations should be cleared
    assert len(integrator.accelerations) == 0
