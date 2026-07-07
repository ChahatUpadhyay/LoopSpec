"""Simulation state serialization. (C15, C68, C69)"""
import json
import numpy as np
from ..physics.particles import ParticleSystem


def save_state(particles: ParticleSystem, filepath: str, metadata: dict = None) -> None:
    """Save simulation state to JSON. (C68)
    
    Args:
        particles: Current particle system state
        filepath: Output file path
        metadata: Optional metadata (timestep, iteration, etc.)
    """
    state = {
        'version': 1,
        'n_particles': particles.n,
        'positions': particles.positions.tolist(),
        'velocities': particles.velocities.tolist(),
        'masses': particles.masses.tolist(),
        'colors': particles.colors.tolist(),
        'radii': particles.radii.tolist(),
    }
    if metadata:
        state['metadata'] = metadata
    
    with open(filepath, 'w') as f:
        json.dump(state, f)


def load_state(filepath: str) -> tuple[ParticleSystem, dict]:
    """Load simulation state from JSON. (C69)
    
    Args:
        filepath: Input file path
    
    Returns:
        (ParticleSystem, metadata_dict)
    """
    with open(filepath, 'r') as f:
        state = json.load(f)
    
    n = state['n_particles']
    particles = ParticleSystem(
        positions=np.array(state['positions'], dtype=np.float64),
        velocities=np.array(state['velocities'], dtype=np.float64),
        masses=np.array(state['masses'], dtype=np.float64),
        colors=np.array(state['colors'], dtype=np.float32),
        radii=np.array(state['radii'], dtype=np.float32),
    )
    metadata = state.get('metadata', {})
    return particles, metadata


def save_galaxy_params(params: dict, filepath: str) -> None:
    """Save galaxy generation parameters. (C15)"""
    with open(filepath, 'w') as f:
        json.dump(params, f, indent=2)


def load_galaxy_params(filepath: str) -> dict:
    """Load galaxy generation parameters. (C15)"""
    with open(filepath, 'r') as f:
        return json.load(f)
