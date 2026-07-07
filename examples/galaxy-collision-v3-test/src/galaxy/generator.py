"""Procedural spiral galaxy generation. (C10-C14)"""
import numpy as np
from ..physics.particles import ParticleSystem


def generate_spiral_galaxy(
    n_particles: int = 5000,
    n_arms: int = 2,
    bulge_radius: float = 0.3,
    disk_radius: float = 2.0,
    disk_height: float = 0.05,
    rotation_velocity: float = 1.0,
    mass_range: tuple = (0.5, 2.0),
    bulge_fraction: float = 0.2,
    center: np.ndarray = None,
    velocity: np.ndarray = None,
    seed: int = None,
) -> ParticleSystem:
    """Generate a spiral galaxy with configurable parameters. (C10, C11)
    
    Args:
        n_particles: Total number of particles
        n_arms: Number of spiral arms
        bulge_radius: Radius of central bulge
        disk_radius: Radius of galactic disk
        disk_height: Thickness of disk (z-direction)
        rotation_velocity: Base orbital velocity
        mass_range: (min, max) mass for particles
        bulge_fraction: Fraction of particles in bulge
        center: Galaxy center position [x, y, z]
        velocity: Bulk velocity of galaxy [vx, vy, vz]
        seed: Random seed for reproducibility
    
    Returns:
        ParticleSystem with generated galaxy
    """
    rng = np.random.default_rng(seed)
    
    if center is None:
        center = np.zeros(3)
    if velocity is None:
        velocity = np.zeros(3)
    
    particles = ParticleSystem.create(n_particles)
    n_bulge = int(n_particles * bulge_fraction)
    n_disk = n_particles - n_bulge
    
    # === Bulge particles (spherical distribution) ===
    r_bulge = rng.exponential(bulge_radius * 0.5, n_bulge)
    theta = rng.uniform(0, 2 * np.pi, n_bulge)
    phi = np.arccos(rng.uniform(-1, 1, n_bulge))
    
    particles.positions[:n_bulge, 0] = r_bulge * np.sin(phi) * np.cos(theta)
    particles.positions[:n_bulge, 1] = r_bulge * np.sin(phi) * np.sin(theta)
    particles.positions[:n_bulge, 2] = r_bulge * np.cos(phi)
    
    # Bulge velocities (mild random motion)
    particles.velocities[:n_bulge] = rng.normal(0, 0.1 * rotation_velocity, (n_bulge, 3))
    
    # === Disk particles (spiral arm distribution) ===
    r_disk = rng.exponential(disk_radius * 0.4, n_disk)
    r_disk = np.clip(r_disk, 0, disk_radius)
    
    # Spiral arm angle: base angle + log spiral offset
    arm_idx = rng.integers(0, n_arms, n_disk)
    base_angle = arm_idx * (2 * np.pi / n_arms)
    spiral_angle = base_angle + np.log1p(r_disk) * 2.5  # log spiral
    # Add scatter
    spiral_angle += rng.normal(0, 0.3, n_disk)
    
    particles.positions[n_bulge:, 0] = r_disk * np.cos(spiral_angle)
    particles.positions[n_bulge:, 1] = r_disk * np.sin(spiral_angle)
    particles.positions[n_bulge:, 2] = rng.normal(0, disk_height, n_disk)
    
    # Disk velocities (circular orbit + perturbation)
    # v_circular = sqrt(GM/r) approximated by rotation_velocity * sqrt(r/disk_radius)
    v_circ = rotation_velocity * np.sqrt(r_disk / (disk_radius * 0.5 + r_disk))
    particles.velocities[n_bulge:, 0] = -v_circ * np.sin(spiral_angle)
    particles.velocities[n_bulge:, 1] = v_circ * np.cos(spiral_angle)
    particles.velocities[n_bulge:, 2] = rng.normal(0, 0.02, n_disk)
    
    # === Apply center offset and bulk velocity ===
    particles.positions += center
    particles.velocities += velocity
    
    # === Masses ===
    particles.masses = rng.uniform(mass_range[0], mass_range[1], n_particles)
    
    # === Colors based on mass (C28) ===
    mass_norm = (particles.masses - mass_range[0]) / (mass_range[1] - mass_range[0])
    particles.colors[:, 0] = 0.5 + 0.5 * mass_norm  # R: heavier = redder
    particles.colors[:, 1] = 0.7 - 0.3 * mass_norm  # G
    particles.colors[:, 2] = 1.0 - 0.5 * mass_norm  # B: lighter = bluer
    particles.colors[:, 3] = 1.0  # Alpha
    
    # === Radii based on mass ===
    particles.radii = 0.005 + 0.01 * mass_norm.astype(np.float32)
    
    return particles


def milky_way_preset(n: int = 5000, center=None, velocity=None) -> ParticleSystem:
    """Milky Way-like galaxy preset. (C12)"""
    return generate_spiral_galaxy(
        n_particles=n, n_arms=4, bulge_radius=0.4, disk_radius=2.5,
        disk_height=0.04, rotation_velocity=1.2, bulge_fraction=0.15,
        center=center if center is not None else np.zeros(3),
        velocity=velocity if velocity is not None else np.zeros(3),
        seed=42,
    )


def andromeda_preset(n: int = 5000, center=None, velocity=None) -> ParticleSystem:
    """Andromeda-like galaxy preset. (C13)"""
    return generate_spiral_galaxy(
        n_particles=n, n_arms=2, bulge_radius=0.5, disk_radius=3.0,
        disk_height=0.03, rotation_velocity=1.0, bulge_fraction=0.25,
        center=center if center is not None else np.array([5.0, 0.0, 0.0]),
        velocity=velocity if velocity is not None else np.array([-0.3, 0.1, 0.0]),
        seed=123,
    )


def random_galaxy(n: int = 5000, center=None, velocity=None, seed=None) -> ParticleSystem:
    """Random galaxy generation. (C14)"""
    rng = np.random.default_rng(seed)
    return generate_spiral_galaxy(
        n_particles=n,
        n_arms=rng.integers(2, 6),
        bulge_radius=rng.uniform(0.2, 0.6),
        disk_radius=rng.uniform(1.5, 3.5),
        disk_height=rng.uniform(0.02, 0.08),
        rotation_velocity=rng.uniform(0.8, 1.5),
        bulge_fraction=rng.uniform(0.1, 0.3),
        center=center if center is not None else np.zeros(3),
        velocity=velocity if velocity is not None else np.zeros(3),
        seed=seed,
    )
