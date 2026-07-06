"""
Serialization module for saving and loading simulation state.

Provides JSON-based serialization of simulation state including particles,
galaxy parameters, and simulation settings.
"""

import json
import numpy as np
from typing import List, Dict, Any
from pathlib import Path
from physics.particle import Particle
from galaxy.spiral_generator import GalaxyParameters


class SimulationState:
    """
    Container for complete simulation state.
    
    Attributes:
        particles: List of particles
        galaxy_params: Galaxy parameters
        simulation_settings: Simulation settings (dt, softening, etc.)
        metadata: Additional metadata (timestamp, version, etc.)
    """
    
    def __init__(
        self,
        particles: List[Particle],
        galaxy_params: GalaxyParameters = None,
        simulation_settings: Dict[str, Any] = None,
        metadata: Dict[str, Any] = None
    ):
        self.particles = particles
        self.galaxy_params = galaxy_params
        self.simulation_settings = simulation_settings or {}
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert simulation state to dictionary for JSON serialization."""
        # Serialize particles
        particles_data = []
        for p in self.particles:
            particles_data.append({
                'position': p.position.tolist(),
                'velocity': p.velocity.tolist(),
                'mass': float(p.mass),
                'color': p.color,
                'radius': float(p.radius)
            })
        
        # Serialize galaxy parameters
        galaxy_data = None
        if self.galaxy_params:
            galaxy_data = {
                'num_arms': self.galaxy_params.num_arms,
                'bulge_radius': self.galaxy_params.bulge_radius,
                'disk_radius': self.galaxy_params.disk_radius,
                'arm_tightness': self.galaxy_params.arm_tightness,
                'rotation_velocity': self.galaxy_params.rotation_velocity,
                'num_particles': self.galaxy_params.num_particles,
                'bulge_mass_fraction': self.galaxy_params.bulge_mass_fraction,
                'dark_matter_strength': self.galaxy_params.dark_matter_strength,
                'inclination': self.galaxy_params.inclination,
                'position_offset': self.galaxy_params.position_offset,
                'velocity_offset': self.galaxy_params.velocity_offset
            }
        
        return {
            'particles': particles_data,
            'galaxy_params': galaxy_data,
            'simulation_settings': self.simulation_settings,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SimulationState':
        """Create simulation state from dictionary."""
        # Deserialize particles
        particles = []
        for p_data in data['particles']:
            particle = Particle(
                position=np.array(p_data['position']),
                velocity=np.array(p_data['velocity']),
                mass=p_data['mass'],
                color=tuple(p_data['color']),
                radius=p_data['radius']
            )
            particles.append(particle)
        
        # Deserialize galaxy parameters
        galaxy_params = None
        if data.get('galaxy_params'):
            gp_data = data['galaxy_params']
            galaxy_params = GalaxyParameters(
                num_arms=gp_data['num_arms'],
                bulge_radius=gp_data['bulge_radius'],
                disk_radius=gp_data['disk_radius'],
                arm_tightness=gp_data['arm_tightness'],
                rotation_velocity=gp_data['rotation_velocity'],
                num_particles=gp_data['num_particles'],
                bulge_mass_fraction=gp_data['bulge_mass_fraction'],
                dark_matter_strength=gp_data['dark_matter_strength'],
                inclination=gp_data['inclination'],
                position_offset=tuple(gp_data['position_offset']),
                velocity_offset=tuple(gp_data['velocity_offset'])
            )
        
        return cls(
            particles=particles,
            galaxy_params=galaxy_params,
            simulation_settings=data.get('simulation_settings', {}),
            metadata=data.get('metadata', {})
        )


def save_simulation(state: SimulationState, filepath: str) -> None:
    """
    Save simulation state to JSON file.
    
    Args:
        state: Simulation state to save
        filepath: Path to save file
    """
    data = state.to_dict()
    
    # Add timestamp to metadata
    if 'metadata' not in data:
        data['metadata'] = {}
    data['metadata']['timestamp'] = str(np.datetime64('now'))
    data['metadata']['version'] = '0.1.0'
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)


def load_simulation(filepath: str) -> SimulationState:
    """
    Load simulation state from JSON file.
    
    Args:
        filepath: Path to load file from
        
    Returns:
        Simulation state
    """
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    return SimulationState.from_dict(data)


def save_galaxy_params(params: GalaxyParameters, filepath: str) -> None:
    """
    Save galaxy parameters to JSON file.
    
    Args:
        params: Galaxy parameters to save
        filepath: Path to save file
    """
    state = SimulationState(particles=[], galaxy_params=params)
    save_simulation(state, filepath)


def load_galaxy_params(filepath: str) -> GalaxyParameters:
    """
    Load galaxy parameters from JSON file.
    
    Args:
        filepath: Path to load file from
        
    Returns:
        Galaxy parameters
    """
    state = load_simulation(filepath)
    return state.galaxy_params
