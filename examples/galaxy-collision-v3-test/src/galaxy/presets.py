"""Collision presets for galaxy pairs. (C16-C21)"""
import numpy as np
from ..physics.particles import ParticleSystem
from .generator import milky_way_preset, andromeda_preset, random_galaxy


def merge_galaxies(g1: ParticleSystem, g2: ParticleSystem) -> ParticleSystem:
    """Merge two galaxy particle systems into one."""
    n = g1.n + g2.n
    merged = ParticleSystem.create(n)
    merged.positions[:g1.n] = g1.positions
    merged.positions[g1.n:] = g2.positions
    merged.velocities[:g1.n] = g1.velocities
    merged.velocities[g1.n:] = g2.velocities
    merged.masses[:g1.n] = g1.masses
    merged.masses[g1.n:] = g2.masses
    merged.colors[:g1.n] = g1.colors
    merged.colors[g1.n:] = g2.colors
    merged.radii[:g1.n] = g1.radii
    merged.radii[g1.n:] = g2.radii
    return merged


def head_on_collision(n_per_galaxy: int = 5000) -> ParticleSystem:
    """Head-on collision: two galaxies on direct collision course. (C16)"""
    g1 = milky_way_preset(n_per_galaxy, 
                          center=np.array([-3.0, 0.0, 0.0]),
                          velocity=np.array([0.4, 0.0, 0.0]))
    g2 = andromeda_preset(n_per_galaxy,
                          center=np.array([3.0, 0.0, 0.0]),
                          velocity=np.array([-0.4, 0.0, 0.0]))
    return merge_galaxies(g1, g2)


def flyby_collision(n_per_galaxy: int = 5000) -> ParticleSystem:
    """Fly-by: galaxies pass close but don't directly collide. (C17)"""
    g1 = milky_way_preset(n_per_galaxy,
                          center=np.array([-4.0, -1.0, 0.0]),
                          velocity=np.array([0.3, 0.15, 0.0]))
    g2 = andromeda_preset(n_per_galaxy,
                          center=np.array([4.0, 1.0, 0.0]),
                          velocity=np.array([-0.3, -0.15, 0.0]))
    return merge_galaxies(g1, g2)


def retrograde_collision(n_per_galaxy: int = 5000) -> ParticleSystem:
    """Retrograde: galaxies with opposing rotation directions. (C18)"""
    g1 = milky_way_preset(n_per_galaxy,
                          center=np.array([-3.5, 0.0, 0.0]),
                          velocity=np.array([0.35, 0.0, 0.0]))
    # Flip velocities for retrograde rotation
    g2 = andromeda_preset(n_per_galaxy,
                          center=np.array([3.5, 0.0, 0.0]),
                          velocity=np.array([-0.35, 0.0, 0.0]))
    g2.velocities[:, :2] *= -1  # Reverse disk rotation
    return merge_galaxies(g1, g2)


def prograde_collision(n_per_galaxy: int = 5000) -> ParticleSystem:
    """Prograde: galaxies with same rotation direction. (C19)"""
    g1 = milky_way_preset(n_per_galaxy,
                          center=np.array([-3.5, 0.5, 0.0]),
                          velocity=np.array([0.3, -0.05, 0.0]))
    g2 = andromeda_preset(n_per_galaxy,
                          center=np.array([3.5, -0.5, 0.0]),
                          velocity=np.array([-0.3, 0.05, 0.0]))
    return merge_galaxies(g1, g2)


def elliptical_merger(n_per_galaxy: int = 5000) -> ParticleSystem:
    """Elliptical orbit merger: slow inspiral. (C20)"""
    g1 = milky_way_preset(n_per_galaxy,
                          center=np.array([-4.0, 0.0, 0.0]),
                          velocity=np.array([0.1, 0.25, 0.0]))
    g2 = andromeda_preset(n_per_galaxy,
                          center=np.array([4.0, 0.0, 0.0]),
                          velocity=np.array([-0.1, -0.25, 0.0]))
    return merge_galaxies(g1, g2)


def random_collision(n_per_galaxy: int = 5000, seed=None) -> ParticleSystem:
    """Random collision configuration. (C21)"""
    rng = np.random.default_rng(seed)
    sep = rng.uniform(3.0, 6.0)
    angle = rng.uniform(0, 2 * np.pi)
    speed = rng.uniform(0.1, 0.5)
    
    c1 = np.array([-sep/2 * np.cos(angle), -sep/2 * np.sin(angle), 0.0])
    c2 = np.array([sep/2 * np.cos(angle), sep/2 * np.sin(angle), 0.0])
    v1 = np.array([speed * np.cos(angle), speed * np.sin(angle), rng.uniform(-0.1, 0.1)])
    v2 = -v1
    
    g1 = random_galaxy(n_per_galaxy, center=c1, velocity=v1, seed=rng.integers(10000))
    g2 = random_galaxy(n_per_galaxy, center=c2, velocity=v2, seed=rng.integers(10000))
    return merge_galaxies(g1, g2)


PRESET_MAP = {
    'Head-On': head_on_collision,
    'Fly-By': flyby_collision,
    'Retrograde': retrograde_collision,
    'Prograde': prograde_collision,
    'Elliptical Merger': elliptical_merger,
    'Random': random_collision,
}
