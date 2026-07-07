"""Particle data structure for N-body simulation. (C9)"""
import numpy as np
from dataclasses import dataclass
from typing import Optional


@dataclass
class ParticleSystem:
    """Stores particle state as structured NumPy arrays.
    
    Each particle has: position (3D), velocity (3D), mass, color (RGBA), radius.
    Criteria: C9
    """
    positions: np.ndarray      # (N, 3) float64
    velocities: np.ndarray     # (N, 3) float64
    masses: np.ndarray         # (N,) float64
    colors: np.ndarray         # (N, 4) float32 RGBA
    radii: np.ndarray          # (N,) float32
    
    @property
    def n(self) -> int:
        """Number of particles."""
        return len(self.masses)
    
    @classmethod
    def create(cls, n: int) -> 'ParticleSystem':
        """Create an empty particle system with N particles."""
        return cls(
            positions=np.zeros((n, 3), dtype=np.float64),
            velocities=np.zeros((n, 3), dtype=np.float64),
            masses=np.ones(n, dtype=np.float64),
            colors=np.ones((n, 4), dtype=np.float32),
            radii=np.ones(n, dtype=np.float32) * 0.01,
        )
    
    def kinetic_energy(self) -> float:
        """Compute total kinetic energy: sum(0.5 * m * v^2). (C51)"""
        v_sq = np.sum(self.velocities ** 2, axis=1)
        return 0.5 * np.sum(self.masses * v_sq)
    
    def momentum(self) -> np.ndarray:
        """Compute total momentum vector: sum(m * v). (C52)"""
        return np.sum(self.masses[:, None] * self.velocities, axis=0)
    
    def angular_momentum(self) -> np.ndarray:
        """Compute total angular momentum: sum(m * r x v). (C53)"""
        cross = np.cross(self.positions, self.velocities)
        return np.sum(self.masses[:, None] * cross, axis=0)
    
    def center_of_mass(self) -> np.ndarray:
        """Compute center of mass position. (C54)"""
        total_mass = np.sum(self.masses)
        if total_mass == 0:
            return np.zeros(3)
        return np.sum(self.masses[:, None] * self.positions, axis=0) / total_mass
    
    def potential_energy(self, softening: float = 0.01) -> float:
        """Compute gravitational potential energy (approximate for large N). (C50)
        
        Uses sampling for N > 1000 to avoid O(N^2) cost.
        """
        n = self.n
        if n < 2:
            return 0.0
        
        if n <= 1000:
            pe = 0.0
            for i in range(n):
                dx = self.positions[i+1:] - self.positions[i]
                r = np.sqrt(np.sum(dx**2, axis=1) + softening**2)
                pe -= np.sum(self.masses[i] * self.masses[i+1:] / r)
            return pe
        else:
            # Sample 500 random pairs for approximation
            rng = np.random.default_rng(42)
            idx_i = rng.integers(0, n, size=500)
            idx_j = rng.integers(0, n, size=500)
            mask = idx_i != idx_j
            idx_i, idx_j = idx_i[mask], idx_j[mask]
            dx = self.positions[idx_j] - self.positions[idx_i]
            r = np.sqrt(np.sum(dx**2, axis=1) + softening**2)
            sample_pe = -np.sum(self.masses[idx_i] * self.masses[idx_j] / r)
            # Scale by ratio of total pairs to sampled pairs
            total_pairs = n * (n - 1) / 2
            return sample_pe * total_pairs / len(idx_i)
