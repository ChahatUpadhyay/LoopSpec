"""
Particle class for N-body simulation.

Represents a single particle in the simulation with position, velocity, mass, color, and radius.
"""

import numpy as np
from dataclasses import dataclass
from typing import Tuple


@dataclass
class Particle:
    """
    A particle in the N-body simulation.
    
    Attributes:
        position: 3D position vector (x, y, z) in simulation units
        velocity: 3D velocity vector (vx, vy, vz) in simulation units per time
        mass: Particle mass in simulation units
        color: RGB color tuple (r, g, b) in range [0, 1]
        radius: Particle radius for rendering
    """
    position: np.ndarray
    velocity: np.ndarray
    mass: float
    color: Tuple[float, float, float]
    radius: float
    
    def __post_init__(self):
        """Ensure position and velocity are numpy arrays."""
        self.position = np.asarray(self.position, dtype=np.float64)
        self.velocity = np.asarray(self.velocity, dtype=np.float64)
        
    @property
    def kinetic_energy(self) -> float:
        """Calculate kinetic energy: 0.5 * m * v^2."""
        v_squared = np.sum(self.velocity ** 2)
        return 0.5 * self.mass * v_squared
    
    @property
    def momentum(self) -> np.ndarray:
        """Calculate momentum: m * v."""
        return self.mass * self.velocity
    
    def angular_momentum(self, center: np.ndarray) -> np.ndarray:
        """
        Calculate angular momentum about a center point: r x (m * v).
        
        Args:
            center: Center point about which to calculate angular momentum
            
        Returns:
            Angular momentum vector
        """
        r = self.position - center
        p = self.momentum
        return np.cross(r, p)
