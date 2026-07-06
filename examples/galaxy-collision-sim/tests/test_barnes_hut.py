"""
Tests for Barnes-Hut octree.
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from physics.particle import Particle
from physics.barnes_hut import BarnesHutTree
from physics.gravity import compute_gravity_direct


def test_barnes_hut_tree_construction():
    """Test that Barnes-Hut tree is constructed correctly."""
    particles = [
        Particle(
            position=np.array([1.0, 0.0, 0.0]),
            velocity=np.array([0.0, 0.0, 0.0]),
            mass=1.0,
            color=(1.0, 1.0, 1.0),
            radius=0.1
        ),
        Particle(
            position=np.array([-1.0, 0.0, 0.0]),
            velocity=np.array([0.0, 0.0, 0.0]),
            mass=1.0,
            color=(1.0, 1.0, 1.0),
            radius=0.1
        )
    ]
    
    tree = BarnesHutTree(theta=0.5, softening=0.1, G=1.0)
    tree.build(particles)
    
    assert tree.root is not None
    assert tree.root.total_mass == 2.0


def test_barnes_hut_accuracy():
    """Test that Barnes-Hut approximation is reasonably accurate."""
    # Create a simple system
    particles = []
    for i in range(10):
        particles.append(Particle(
            position=np.random.uniform(-5, 5, 3),
            velocity=np.zeros(3),
            mass=1.0,
            color=(1.0, 1.0, 1.0),
            radius=0.1
        ))
    
    # Compute forces using direct summation
    forces_direct = compute_gravity_direct(particles, softening=0.1, G=1.0)
    
    # Compute forces using Barnes-Hut
    tree = BarnesHutTree(theta=0.5, softening=0.1, G=1.0)
    tree.build(particles)
    forces_bh = tree.compute_all_forces(particles)
    
    # Compare forces (should be within 15% for Barnes-Hut approximation with theta=0.5)
    for i in range(len(particles)):
        if np.linalg.norm(forces_direct[i]) > 1e-10:
            relative_error = np.linalg.norm(forces_bh[i] - forces_direct[i]) / np.linalg.norm(forces_direct[i])
            assert relative_error < 0.15


def test_barnes_hut_empty():
    """Test Barnes-Hut with no particles."""
    tree = BarnesHutTree(theta=0.5, softening=0.1, G=1.0)
    tree.build([])
    
    assert tree.root is None
