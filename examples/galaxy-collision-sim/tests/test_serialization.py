"""
Tests for serialization.
"""

import pytest
import numpy as np
import sys
import json
import tempfile
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from physics.particle import Particle
from galaxy.spiral_generator import GalaxyParameters
from serialization import SimulationState, save_simulation, load_simulation, save_galaxy_params, load_galaxy_params


def test_simulation_state_to_dict():
    """Test converting simulation state to dictionary."""
    particles = [
        Particle(
            position=np.array([1.0, 2.0, 3.0]),
            velocity=np.array([0.1, 0.2, 0.3]),
            mass=1.0,
            color=(1.0, 0.5, 0.0),
            radius=0.1
        )
    ]
    
    state = SimulationState(particles=particles)
    data = state.to_dict()
    
    assert 'particles' in data
    assert len(data['particles']) == 1
    assert data['particles'][0]['position'] == [1.0, 2.0, 3.0]


def test_simulation_state_from_dict():
    """Test creating simulation state from dictionary."""
    data = {
        'particles': [
            {
                'position': [1.0, 2.0, 3.0],
                'velocity': [0.1, 0.2, 0.3],
                'mass': 1.0,
                'color': [1.0, 0.5, 0.0],
                'radius': 0.1
            }
        ],
        'galaxy_params': None,
        'simulation_settings': {},
        'metadata': {}
    }
    
    state = SimulationState.from_dict(data)
    
    assert len(state.particles) == 1
    assert np.allclose(state.particles[0].position, np.array([1.0, 2.0, 3.0]))


def test_save_load_simulation():
    """Test saving and loading simulation state."""
    particles = [
        Particle(
            position=np.array([1.0, 2.0, 3.0]),
            velocity=np.array([0.1, 0.2, 0.3]),
            mass=1.0,
            color=(1.0, 0.5, 0.0),
            radius=0.1
        )
    ]
    
    state = SimulationState(particles=particles)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        filepath = f.name
    
    try:
        save_simulation(state, filepath)
        loaded_state = load_simulation(filepath)
        
        assert len(loaded_state.particles) == len(state.particles)
        assert np.allclose(loaded_state.particles[0].position, state.particles[0].position)
    finally:
        Path(filepath).unlink()


def test_save_load_galaxy_params():
    """Test saving and loading galaxy parameters."""
    params = GalaxyParameters(num_arms=3, num_particles=5000)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        filepath = f.name
    
    try:
        save_galaxy_params(params, filepath)
        loaded_params = load_galaxy_params(filepath)
        
        assert loaded_params.num_arms == params.num_arms
        assert loaded_params.num_particles == params.num_particles
    finally:
        Path(filepath).unlink()
