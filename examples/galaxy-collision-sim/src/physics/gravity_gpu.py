"""
GPU-accelerated gravity calculation using CuPy.

Implements fully vectorized N-body gravity on GPU for massive performance improvement.
"""

import numpy as np
try:
    import cupy as cp
    CUPY_AVAILABLE = True
except ImportError:
    CUPY_AVAILABLE = False
    print("CuPy not available, falling back to CPU")

from typing import List
from physics.particle import Particle


def compute_gravity_gpu(
    particles: List[Particle],
    softening: float = 0.1,
    G: float = 1.0
) -> np.ndarray:
    """
    Compute gravitational forces using GPU-accelerated fully vectorized approach.
    
    Uses CuPy for GPU acceleration with O(N^2) but massively parallelized.
    
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
    
    if not CUPY_AVAILABLE:
        # Fallback to CPU
        from physics.gravity import compute_gravity_direct
        return compute_gravity_direct(particles, softening, G)
    
    # Extract positions and masses
    positions = np.array([p.position for p in particles], dtype=np.float32)
    masses = np.array([p.mass for p in particles], dtype=np.float32)
    
    # Transfer to GPU
    pos_gpu = cp.array(positions)
    mass_gpu = cp.array(masses)
    
    # Compute forces using fully vectorized approach on GPU
    # r_vec[i, j] = pos[j] - pos[i]
    r_vec = pos_gpu[cp.newaxis, :, :] - pos_gpu[:, cp.newaxis, :]  # shape (N, N, 3)
    
    # Distance squared
    r_sq = cp.sum(r_vec**2, axis=2)  # shape (N, N)
    
    # Softened distance cubed
    softened_dist_cubed = (r_sq + softening**2)**1.5
    
    # Force magnitude (G * m_i * m_j / r^3)
    # mass_matrix[i, j] = mass[i] * mass[j]
    mass_matrix = mass_gpu[:, cp.newaxis] * mass_gpu[cp.newaxis, :]
    force_mag = G * mass_matrix / softened_dist_cubed  # shape (N, N)
    
    # Force vectors
    force_vec = force_mag[:, :, cp.newaxis] * r_vec  # shape (N, N, 3)
    
    # Sum forces (exclude self-interaction by setting diagonal to 0)
    cp.fill_diagonal(force_mag, 0)
    forces = cp.sum(force_vec, axis=1)  # shape (N, 3)
    
    # Transfer back to CPU
    return cp.asnumpy(forces)
