"""
Tests for gravity calculations.
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from physics.particle import Particle
from physics.gravity import (
    compute_gravity_direct,
    compute_potential_energy,
    compute_kinetic_energy,
    compute_total_energy,
    compute_momentum,
    compute_angular_momentum,
    compute_center_of_mass
)


def test_gravity_two_body():
    """Test gravity calculation for two-body system."""
    p1 = Particle(
        position=np.array([0.0, 0.0, 0.0]),
        velocity=np.array([0.0, 0.0, 0.0]),
        mass=1.0,
        color=(1.0, 1.0, 1.0),
        radius=0.1
    )
    p2 = Particle(
        position=np.array([1.0, 0.0, 0.0]),
        velocity=np.array([0.0, 0.0, 0.0]),
        mass=1.0,
        color=(1.0, 1.0, 1.0),
        radius=0.1
    )
    
    forces = compute_gravity_direct([p1, p2], softening=0.1, G=1.0)
    
    # Force on p1 should be toward p2 (positive x direction)
    assert forces[0][0] > 0
    # Force on p2 should be toward p1 (negative x direction)
    assert forces[1][0] < 0
    # Forces should be equal and opposite
    assert np.allclose(forces[0], -forces[1])


def test_potential_energy():
    """Test potential energy calculation."""
    p1 = Particle(
        position=np.array([0.0, 0.0, 0.0]),
        velocity=np.array([0.0, 0.0, 0.0]),
        mass=1.0,
        color=(1.0, 1.0, 1.0),
        radius=0.1
    )
    p2 = Particle(
        position=np.array([1.0, 0.0, 0.0]),
        velocity=np.array([0.0, 0.0, 0.0]),
        mass=1.0,
        color=(1.0, 1.0, 1.0),
        radius=0.1
    )
    
    PE = compute_potential_energy([p1, p2], softening=0.1, G=1.0)
    
    # PE should be negative (attractive)
    assert PE < 0


def test_kinetic_energy():
    """Test kinetic energy calculation."""
    p1 = Particle(
        position=np.array([0.0, 0.0, 0.0]),
        velocity=np.array([1.0, 0.0, 0.0]),
        mass=1.0,
        color=(1.0, 1.0, 1.0),
        radius=0.1
    )
    p2 = Particle(
        position=np.array([0.0, 0.0, 0.0]),
        velocity=np.array([0.0, 1.0, 0.0]),
        mass=1.0,
        color=(1.0, 1.0, 1.0),
        radius=0.1
    )
    
    KE = compute_kinetic_energy([p1, p2])
    
    # KE = 0.5 * 1.0 * 1.0^2 + 0.5 * 1.0 * 1.0^2 = 1.0
    assert abs(KE - 1.0) < 1e-10


def test_total_energy():
    """Test total energy calculation."""
    p1 = Particle(
        position=np.array([0.0, 0.0, 0.0]),
        velocity=np.array([0.0, 0.0, 0.0]),
        mass=1.0,
        color=(1.0, 1.0, 1.0),
        radius=0.1
    )
    p2 = Particle(
        position=np.array([1.0, 0.0, 0.0]),
        velocity=np.array([0.0, 0.0, 0.0]),
        mass=1.0,
        color=(1.0, 1.0, 1.0),
        radius=0.1
    )
    
    E = compute_total_energy([p1, p2], softening=0.1, G=1.0)
    
    # Should be sum of KE (0) and PE (negative)
    assert E < 0


def test_momentum():
    """Test momentum calculation."""
    p1 = Particle(
        position=np.array([0.0, 0.0, 0.0]),
        velocity=np.array([1.0, 0.0, 0.0]),
        mass=1.0,
        color=(1.0, 1.0, 1.0),
        radius=0.1
    )
    p2 = Particle(
        position=np.array([0.0, 0.0, 0.0]),
        velocity=np.array([-1.0, 0.0, 0.0]),
        mass=1.0,
        color=(1.0, 1.0, 1.0),
        radius=0.1
    )
    
    P = compute_momentum([p1, p2])
    
    # Total momentum should be zero
    assert np.allclose(P, np.zeros(3))


def test_angular_momentum():
    """Test angular momentum calculation."""
    p1 = Particle(
        position=np.array([1.0, 0.0, 0.0]),
        velocity=np.array([0.0, 1.0, 0.0]),
        mass=1.0,
        color=(1.0, 1.0, 1.0),
        radius=0.1
    )
    
    L = compute_angular_momentum([p1], center=np.array([0.0, 0.0, 0.0]))
    
    # L should be in z direction
    assert abs(L[0]) < 1e-10
    assert abs(L[1]) < 1e-10
    assert abs(L[2] - 1.0) < 1e-10


def test_center_of_mass():
    """Test center of mass calculation."""
    p1 = Particle(
        position=np.array([0.0, 0.0, 0.0]),
        velocity=np.array([0.0, 0.0, 0.0]),
        mass=1.0,
        color=(1.0, 1.0, 1.0),
        radius=0.1
    )
    p2 = Particle(
        position=np.array([2.0, 0.0, 0.0]),
        velocity=np.array([0.0, 0.0, 0.0]),
        mass=1.0,
        color=(1.0, 1.0, 1.0),
        radius=0.1
    )
    
    com = compute_center_of_mass([p1, p2])
    
    # Center of mass should be at (1, 0, 0)
    expected = np.array([1.0, 0.0, 0.0])
    assert np.allclose(com, expected)
