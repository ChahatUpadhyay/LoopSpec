"""Gravity computation: direct N-body and Barnes-Hut. (C1, C2)"""
import numpy as np
from .octree import build_octree, compute_force_bh


def compute_forces_direct(positions: np.ndarray, masses: np.ndarray, 
                          softening: float = 0.01) -> np.ndarray:
    """Direct O(N^2) gravity computation. (C1)
    
    F_i = sum_j (m_i * m_j * (r_j - r_i)) / (|r_j - r_i|^2 + eps^2)^(3/2)
    
    Returns accelerations (force / mass) for each particle.
    """
    n = len(masses)
    accelerations = np.zeros_like(positions)
    
    for i in range(n):
        dx = positions - positions[i]  # (N, 3)
        r_sq = np.sum(dx**2, axis=1) + softening**2  # (N,)
        r_sq[i] = 1.0  # avoid self
        inv_r3 = 1.0 / (r_sq * np.sqrt(r_sq))
        inv_r3[i] = 0.0
        accelerations[i] = np.sum(masses[:, None] * dx * inv_r3[:, None], axis=0)
    
    return accelerations


def compute_forces_barnes_hut(positions: np.ndarray, masses: np.ndarray,
                              softening: float = 0.01, theta: float = 0.8) -> np.ndarray:
    """Barnes-Hut O(N log N) gravity computation. (C2, C57)
    
    Uses octree spatial partitioning with opening angle theta.
    
    Args:
        positions: (N, 3) particle positions
        masses: (N,) particle masses  
        softening: Softening parameter (C3)
        theta: Barnes-Hut opening angle (0.5=accurate, 1.0=fast)
    
    Returns:
        (N, 3) accelerations
    """
    n = len(masses)
    accelerations = np.zeros_like(positions)
    
    # Build octree
    tree = build_octree(positions, masses)
    if tree is None:
        return accelerations
    
    # Compute force on each particle
    for i in range(n):
        accelerations[i] = compute_force_bh(tree, positions[i], softening, theta)
    
    return accelerations


def compute_forces_gpu(positions: np.ndarray, masses: np.ndarray,
                       softening: float = 0.01) -> np.ndarray:
    """GPU-accelerated direct gravity via CuPy. (C59)
    
    Uses CuPy for vectorized GPU computation.
    Falls back to CPU Barnes-Hut if CuPy unavailable.
    """
    try:
        import cupy as cp
        
        pos_gpu = cp.asarray(positions)
        mass_gpu = cp.asarray(masses)
        n = len(masses)
        accelerations = cp.zeros_like(pos_gpu)
        
        # Vectorized pairwise computation on GPU
        for i in range(n):
            dx = pos_gpu - pos_gpu[i]
            r_sq = cp.sum(dx**2, axis=1) + softening**2
            r_sq[i] = 1.0
            inv_r3 = 1.0 / (r_sq * cp.sqrt(r_sq))
            inv_r3[i] = 0.0
            accelerations[i] = cp.sum(mass_gpu[:, None] * dx * inv_r3[:, None], axis=0)
        
        return cp.asnumpy(accelerations)
    except Exception:
        # Fallback to CPU Barnes-Hut
        return compute_forces_barnes_hut(positions, masses, softening)
