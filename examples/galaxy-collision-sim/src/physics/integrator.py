"""
Leapfrog integrator for N-body simulation.

Implements the leapfrog (kick-drift-kick) integration scheme with adaptive timestep.
"""

import numpy as np
from typing import List, Callable
from physics.particle import Particle
from physics.gravity import compute_gravity_direct, compute_total_energy


class LeapfrogIntegrator:
    """
    Leapfrog integrator with adaptive timestep.
    
    Uses the kick-drift-kick scheme which is symplectic and conserves energy well.
    Supports adaptive timestep based on particle proximity.
    
    Attributes:
        dt: Base timestep
        adaptive: Whether to use adaptive timestep
        min_dt: Minimum timestep for adaptive integration
        max_dt: Maximum timestep for adaptive integration
        G: Gravitational constant
        softening: Softening parameter
    """
    
    def __init__(
        self,
        dt: float = 0.01,
        adaptive: bool = True,
        min_dt: float = 1e-6,
        max_dt: float = 0.1,
        G: float = 1.0,
        softening: float = 0.1
    ):
        """
        Initialize leapfrog integrator.
        
        Args:
            dt: Base timestep
            adaptive: Enable adaptive timestep
            min_dt: Minimum timestep
            max_dt: Maximum timestep
            G: Gravitational constant
            softening: Softening parameter
        """
        self.dt = dt
        self.adaptive = adaptive
        self.min_dt = min_dt
        self.max_dt = max_dt
        self.G = G
        self.softening = softening
        
        # Store accelerations for leapfrog
        self.accelerations: List[np.ndarray] = []
        
    def compute_forces(
        self,
        particles: List[Particle],
        use_barnes_hut: bool = False,
        barnes_hut_tree=None
    ) -> List[np.ndarray]:
        """
        Compute forces on all particles.
        
        Args:
            particles: List of particles
            use_barnes_hut: Whether to use Barnes-Hut approximation
            barnes_hut_tree: Pre-built Barnes-Hut tree
            
        Returns:
            List of force vectors
        """
        if use_barnes_hut and barnes_hut_tree is not None:
            forces = barnes_hut_tree.compute_all_forces(particles)
            return [forces[i] for i in range(len(particles))]
        else:
            forces = compute_gravity_direct(particles, self.softening, self.G)
            return [forces[i] for i in range(len(particles))]
    
    def get_adaptive_timestep(self, particles: List[Particle]) -> float:
        """
        Compute adaptive timestep based on particle proximity.
        
        Smaller timestep when particles are close to prevent ejection.
        
        Args:
            particles: List of particles
            
        Returns:
            Adaptive timestep
        """
        if not self.adaptive:
            return self.dt
        
        # Find minimum distance between any two particles
        min_dist = float('inf')
        positions = np.array([p.position for p in particles])
        
        n = len(positions)
        for i in range(n):
            for j in range(i + 1, n):
                dist = np.linalg.norm(positions[i] - positions[j])
                if dist < min_dist:
                    min_dist = dist
        
        if min_dist == float('inf') or min_dist == 0:
            return self.dt
        
        # Adaptive timestep: scale with minimum distance
        # Smaller distance -> smaller timestep
        adaptive_dt = self.dt * min_dist / (self.softening + min_dist)
        
        # Clamp to bounds
        return np.clip(adaptive_dt, self.min_dt, self.max_dt)
    
    def step(
        self,
        particles: List[Particle],
        use_barnes_hut: bool = False,
        barnes_hut_tree=None
    ) -> float:
        """
        Perform one integration step using kick-drift-kick leapfrog.
        
        Args:
            particles: List of particles (modified in place)
            use_barnes_hut: Whether to use Barnes-Hut approximation
            barnes_hut_tree: Pre-built Barnes-Hut tree
            
        Returns:
            Actual timestep used
        """
        if not particles:
            return 0.0
        
        # Get adaptive timestep
        dt = self.get_adaptive_timestep(particles)
        
        # Initialize accelerations on first step
        if not self.accelerations:
            forces = self.compute_forces(particles, use_barnes_hut, barnes_hut_tree)
            self.accelerations = [f / p.mass for f, p in zip(forces, particles)]
        
        # Kick: v(t + dt/2) = v(t) + a(t) * dt/2
        for i, particle in enumerate(particles):
            particle.velocity += self.accelerations[i] * (dt / 2.0)
        
        # Drift: r(t + dt) = r(t) + v(t + dt/2) * dt
        for particle in particles:
            particle.position += particle.velocity * dt
        
        # Compute new forces/accelerations
        forces = self.compute_forces(particles, use_barnes_hut, barnes_hut_tree)
        new_accelerations = [f / p.mass for f, p in zip(forces, particles)]
        
        # Kick: v(t + dt) = v(t + dt/2) + a(t + dt) * dt/2
        for i, particle in enumerate(particles):
            particle.velocity += new_accelerations[i] * (dt / 2.0)
        
        # Update accelerations for next step
        self.accelerations = new_accelerations
        
        return dt
    
    def reset(self) -> None:
        """Reset the integrator state."""
        self.accelerations = []
    
    def integrate(
        self,
        particles: List[Particle],
        steps: int,
        use_barnes_hut: bool = False,
        barnes_hut_tree=None
    ) -> List[float]:
        """
        Integrate for multiple steps.
        
        Args:
            particles: List of particles (modified in place)
            steps: Number of steps to integrate
            use_barnes_hut: Whether to use Barnes-Hut approximation
            barnes_hut_tree: Pre-built Barnes-Hut tree (will be rebuilt each step if needed)
            
        Returns:
            List of timesteps used
        """
        timesteps = []
        for _ in range(steps):
            # Rebuild Barnes-Hut tree each step if using it
            if use_barnes_hut and barnes_hut_tree is not None:
                barnes_hut_tree.build(particles)
            
            dt = self.step(particles, use_barnes_hut, barnes_hut_tree)
            timesteps.append(dt)
        
        return timesteps
