"""
Tests for Particle class.
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from physics.particle import Particle


def test_particle_creation():
    """Test that Particle can be created with all required attributes."""
    position = np.array([1.0, 2.0, 3.0])
    velocity = np.array([0.1, 0.2, 0.3])
    mass = 1.0
    color = (1.0, 0.5, 0.0)
    radius = 0.1
    
    particle = Particle(position, velocity, mass, color, radius)
    
    assert np.allclose(particle.position, position)
    assert np.allclose(particle.velocity, velocity)
    assert particle.mass == mass
    assert particle.color == color
    assert particle.radius == radius


def test_particle_kinetic_energy():
    """Test kinetic energy calculation."""
    particle = Particle(
        position=np.array([0.0, 0.0, 0.0]),
        velocity=np.array([1.0, 0.0, 0.0]),
        mass=2.0,
        color=(1.0, 1.0, 1.0),
        radius=0.1
    )
    
    # KE = 0.5 * m * v^2 = 0.5 * 2.0 * 1.0^2 = 1.0
    assert abs(particle.kinetic_energy - 1.0) < 1e-10


def test_particle_momentum():
    """Test momentum calculation."""
    particle = Particle(
        position=np.array([0.0, 0.0, 0.0]),
        velocity=np.array([1.0, 2.0, 3.0]),
        mass=2.0,
        color=(1.0, 1.0, 1.0),
        radius=0.1
    )
    
    momentum = particle.momentum
    expected = np.array([2.0, 4.0, 6.0])
    assert np.allclose(momentum, expected)


def test_particle_angular_momentum():
    """Test angular momentum calculation."""
    particle = Particle(
        position=np.array([1.0, 0.0, 0.0]),
        velocity=np.array([0.0, 1.0, 0.0]),
        mass=1.0,
        color=(1.0, 1.0, 1.0),
        radius=0.1
    )
    
    center = np.array([0.0, 0.0, 0.0])
    L = particle.angular_momentum(center)
    
    # L = r x (m * v) = (1,0,0) x (0,1,0) = (0,0,1)
    expected = np.array([0.0, 0.0, 1.0])
    assert np.allclose(L, expected)
