"""
Newtonian gravity calculations for N-body simulation.

Implements direct N-body force calculation and softening parameter.
"""

import numpy as np
from typing import List
from physics.particle import Particle


def compute_gravity_direct(
    particles: List[Particle],
    softening: float = 0.1,
    G: float = 1.0
) -> np.ndarray:
    """
    Compute gravitational forces using direct N-body summation.
    
    Uses semi-vectorized approach for better performance.
    
    Args:
        particles: List of Particle objects
        softening: Softening parameter to prevent singularities
        G: Gravitational constant (default 1.0 in simulation units)
        
    Returns:
        Array of force vectors for each particle, shape (N, 3)
    """
    n = len(particles)
    if n == 0:
        return np.zeros((0, 3))
    
    # Extract positions and masses
    positions = np.array([p.position for p in particles])
    masses = np.array([p.mass for p in particles])
    
    # Compute forces using vectorized operations per particle
    forces = np.zeros((n, 3))
    
    for i in range(n):
        # Vector from all particles to particle i
        r_vec = positions - positions[i]  # shape (N, 3)
        
        # Distance squared
        r_sq = np.sum(r_vec**2, axis=1)  # shape (N,)
        
        # Softened distance cubed
        softened_dist_cubed = (r_sq + softening**2)**1.5
        
        # Force magnitude (G * m_i * m_j / r^3)
        force_mag = G * masses[i] * masses / softened_dist_cubed  # shape (N,)
        
        # Force vectors
        force_vec = force_mag[:, np.newaxis] * r_vec  # shape (N, 3)
        
        # Sum forces (exclude self-interaction)
        force_vec[i] = 0
        forces[i] = np.sum(force_vec, axis=0)
    
    return forces


def compute_potential_energy(
    particles: List[Particle],
    softening: float = 0.1,
    G: float = 1.0
) -> float:
    """
    Compute total gravitational potential energy of the system.
    
    Args:
        particles: List of Particle objects
        softening: Softening parameter
        G: Gravitational constant
        
    Returns:
        Total potential energy
    """
    n = len(particles)
    if n == 0:
        return 0.0
    
    positions = np.array([p.position for p in particles])
    masses = np.array([p.mass for p in particles])
    
    potential = 0.0
    
    for i in range(n):
        for j in range(i + 1, n):
            r_vec = positions[j] - positions[i]
            r_mag = np.linalg.norm(r_vec)
            softened_dist = np.sqrt(r_mag**2 + softening**2)
            potential -= G * masses[i] * masses[j] / softened_dist
    
    return potential


def compute_kinetic_energy(particles: List[Particle]) -> float:
    """
    Compute total kinetic energy of the system.
    
    Args:
        particles: List of Particle objects
        
    Returns:
        Total kinetic energy
    """
    return sum(p.kinetic_energy for p in particles)


def compute_total_energy(
    particles: List[Particle],
    softening: float = 0.1,
    G: float = 1.0
) -> float:
    """
    Compute total energy (kinetic + potential) of the system.
    
    Args:
        particles: List of Particle objects
        softening: Softening parameter
        G: Gravitational constant
        
    Returns:
        Total energy
    """
    return compute_kinetic_energy(particles) + compute_potential_energy(
        particles, softening, G
    )


def compute_momentum(particles: List[Particle]) -> np.ndarray:
    """
    Compute total momentum of the system.
    
    Args:
        particles: List of Particle objects
        
    Returns:
        Total momentum vector
    """
    total_momentum = np.zeros(3)
    for p in particles:
        total_momentum += p.momentum
    return total_momentum


def compute_angular_momentum(
    particles: List[Particle],
    center: np.ndarray = None
) -> np.ndarray:
    """
    Compute total angular momentum of the system about a center point.
    
    Args:
        particles: List of Particle objects
        center: Center point (default: origin)
        
    Returns:
        Total angular momentum vector
    """
    if center is None:
        center = np.zeros(3)
    
    total_L = np.zeros(3)
    for p in particles:
        total_L += p.angular_momentum(center)
    return total_L


def compute_center_of_mass(particles: List[Particle]) -> np.ndarray:
    """
    Compute center of mass of the system.
    
    Args:
        particles: List of Particle objects
        
    Returns:
        Center of mass position
    """
    if not particles:
        return np.zeros(3)
    
    total_mass = sum(p.mass for p in particles)
    if total_mass == 0:
        return np.zeros(3)
    
    weighted_pos = np.zeros(3)
    for p in particles:
        weighted_pos += p.mass * p.position
    
    return weighted_pos / total_mass
