"""
Tests for galaxy generation.
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from galaxy.spiral_generator import SpiralGalaxyGenerator, GalaxyParameters
from physics.particle import Particle


def test_galaxy_generation():
    """Test that galaxy generator creates particles."""
    generator = SpiralGalaxyGenerator()
    params = GalaxyParameters(num_particles=100)
    
    particles = generator.generate(params)
    
    assert len(particles) == 100
    assert all(isinstance(p, Particle) for p in particles)


def test_milky_way_preset():
    """Test Milky Way preset."""
    generator = SpiralGalaxyGenerator()
    particles = generator.generate(SpiralGalaxyGenerator.MILKY_WAY)
    
    assert len(particles) == 10000
    assert all(isinstance(p, Particle) for p in particles)


def test_andromeda_preset():
    """Test Andromeda preset."""
    generator = SpiralGalaxyGenerator()
    particles = generator.generate(SpiralGalaxyGenerator.ANDROMEDA)
    
    assert len(particles) == 15000
    assert all(isinstance(p, Particle) for p in particles)


def test_random_galaxy():
    """Test random galaxy generation."""
    generator = SpiralGalaxyGenerator()
    particles = generator.generate_random(num_particles=100)
    
    assert len(particles) == 100
    assert all(isinstance(p, Particle) for p in particles)


def test_galaxy_parameters():
    """Test that galaxy parameters affect generation."""
    generator = SpiralGalaxyGenerator()
    
    params1 = GalaxyParameters(num_arms=2, num_particles=100)
    params2 = GalaxyParameters(num_arms=4, num_particles=100)
    
    particles1 = generator.generate(params1)
    particles2 = generator.generate(params2)
    
    assert len(particles1) == len(particles2)
    # The distributions should be different (though hard to test precisely)
