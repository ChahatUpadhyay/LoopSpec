"""Leapfrog integrator with adaptive timestep. (C4, C5)"""
import numpy as np
from .particles import ParticleSystem
from .gravity import compute_forces_barnes_hut, compute_forces_gpu


class LeapfrogIntegrator:
    """Kick-Drift-Kick Leapfrog integrator for N-body systems. (C4)
    
    The leapfrog method is symplectic, meaning it conserves energy
    over long timescales (no secular drift).
    
    KDK scheme:
        v(t + dt/2) = v(t) + a(t) * dt/2        [kick]
        x(t + dt)   = x(t) + v(t + dt/2) * dt   [drift]
        a(t + dt)   = compute_forces(x(t + dt))  [force eval]
        v(t + dt)   = v(t + dt/2) + a(t+dt)*dt/2 [kick]
    """
    
    def __init__(self, softening: float = 0.01, theta: float = 0.8, 
                 dt: float = 0.005, use_gpu: bool = False,
                 adaptive: bool = True):
        """Initialize integrator.
        
        Args:
            softening: Gravitational softening length (C3)
            theta: Barnes-Hut opening angle
            dt: Base timestep
            use_gpu: Whether to use GPU for gravity (C59)
            adaptive: Whether to use adaptive timestep (C5)
        """
        self.softening = softening
        self.theta = theta
        self.dt = dt
        self.base_dt = dt
        self.use_gpu = use_gpu
        self.adaptive = adaptive
        self._accelerations: np.ndarray | None = None
        self.physics_fps = 0.0
        self._last_time = 0.0
    
    def _compute_accelerations(self, particles: ParticleSystem) -> np.ndarray:
        """Compute gravitational accelerations."""
        if self.use_gpu and particles.n > 2000:
            return compute_forces_gpu(
                particles.positions, particles.masses, self.softening
            )
        else:
            return compute_forces_barnes_hut(
                particles.positions, particles.masses, 
                self.softening, self.theta
            )
    
    def _adapt_timestep(self, particles: ParticleSystem) -> float:
        """Compute adaptive timestep based on particle proximity. (C5)
        
        Uses the minimum free-fall time: dt ~ eta * sqrt(eps / |a_max|)
        """
        if not self.adaptive or self._accelerations is None:
            return self.base_dt
        
        a_mag = np.sqrt(np.sum(self._accelerations**2, axis=1))
        a_max = np.max(a_mag) if len(a_mag) > 0 else 1.0
        
        if a_max > 0:
            eta = 0.3
            dt_adaptive = eta * np.sqrt(self.softening / a_max)
            # Clamp between 0.1x and 2x base timestep
            return np.clip(dt_adaptive, self.base_dt * 0.1, self.base_dt * 2.0)
        return self.base_dt
    
    def step(self, particles: ParticleSystem) -> None:
        """Advance the simulation by one timestep using KDK leapfrog.
        
        Modifies particles in-place.
        """
        import time
        t0 = time.perf_counter()
        
        # Adapt timestep
        if self.adaptive:
            self.dt = self._adapt_timestep(particles)
        
        dt = self.dt
        
        # Initial force computation (or reuse from previous step)
        if self._accelerations is None:
            self._accelerations = self._compute_accelerations(particles)
        
        # Kick (half step)
        particles.velocities += 0.5 * dt * self._accelerations
        
        # Drift (full step)
        particles.positions += dt * particles.velocities
        
        # Force evaluation at new positions
        self._accelerations = self._compute_accelerations(particles)
        
        # Kick (half step)
        particles.velocities += 0.5 * dt * self._accelerations
        
        # Track physics FPS
        elapsed = time.perf_counter() - t0
        if elapsed > 0:
            self.physics_fps = 1.0 / elapsed
