"""
Procedural spiral galaxy generator.

Generates spiral galaxies with configurable parameters including number of arms,
bulge radius, disk radius, rotation velocity, mass distribution, and dark matter halo.
"""

import numpy as np
from typing import List, Tuple
from dataclasses import dataclass
from physics.particle import Particle


@dataclass
class GalaxyParameters:
    """
    Parameters for spiral galaxy generation.
    
    Attributes:
        num_arms: Number of spiral arms (typically 2-6)
        bulge_radius: Radius of the central bulge
        disk_radius: Radius of the disk
        arm_tightness: How tightly wound the arms are (higher = tighter)
        rotation_velocity: Initial rotation velocity
        num_particles: Total number of particles
        bulge_mass_fraction: Fraction of mass in the bulge
        dark_matter_strength: Strength of dark matter halo
        inclination: Inclination angle in radians
        position_offset: 3D position offset
        velocity_offset: 3D velocity offset
    """
    num_arms: int = 2
    bulge_radius: float = 1.0
    disk_radius: float = 10.0
    arm_tightness: float = 2.0
    rotation_velocity: float = 1.0
    num_particles: int = 10000
    bulge_mass_fraction: float = 0.3
    dark_matter_strength: float = 1.0
    inclination: float = 0.0
    position_offset: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    velocity_offset: Tuple[float, float, float] = (0.0, 0.0, 0.0)


class SpiralGalaxyGenerator:
    """
    Procedural spiral galaxy generator.
    
    Creates realistic spiral galaxies using logarithmic spiral equations
    and mass distribution models.
    """
    
    # Preset configurations
    MILKY_WAY = GalaxyParameters(
        num_arms=4,
        bulge_radius=1.5,
        disk_radius=15.0,
        arm_tightness=2.5,
        rotation_velocity=1.2,
        num_particles=10000,
        bulge_mass_fraction=0.25,
        dark_matter_strength=1.2,
        inclination=0.0
    )
    
    ANDROMEDA = GalaxyParameters(
        num_arms=2,
        bulge_radius=2.0,
        disk_radius=20.0,
        arm_tightness=3.0,
        rotation_velocity=1.5,
        num_particles=15000,
        bulge_mass_fraction=0.35,
        dark_matter_strength=1.5,
        inclination=0.5
    )
    
    def __init__(self):
        """Initialize galaxy generator."""
        pass
    
    def generate(self, params: GalaxyParameters) -> List[Particle]:
        """
        Generate a spiral galaxy with the given parameters.
        
        Args:
            params: Galaxy parameters
            
        Returns:
            List of particles representing the galaxy
        """
        particles = []
        
        # Calculate particle distribution
        num_bulge = int(params.num_particles * params.bulge_mass_fraction)
        num_disk = params.num_particles - num_bulge
        
        # Generate bulge particles
        bulge_particles = self._generate_bulge(params, num_bulge)
        particles.extend(bulge_particles)
        
        # Generate disk particles
        disk_particles = self._generate_disk(params, num_disk)
        particles.extend(disk_particles)
        
        # Apply inclination
        self._apply_inclination(particles, params.inclination)
        
        # Apply offsets
        self._apply_offsets(particles, params.position_offset, params.velocity_offset)
        
        return particles
    
    def _generate_bulge(self, params: GalaxyParameters, num_particles: int) -> List[Particle]:
        """Generate bulge particles using spherical distribution."""
        particles = []
        
        for _ in range(num_particles):
            # Random position in sphere using rejection sampling
            while True:
                x = np.random.uniform(-params.bulge_radius, params.bulge_radius)
                y = np.random.uniform(-params.bulge_radius, params.bulge_radius)
                z = np.random.uniform(-params.bulge_radius * 0.5, params.bulge_radius * 0.5)
                r = np.sqrt(x**2 + y**2 + z**2)
                if r <= params.bulge_radius:
                    break
            
            position = np.array([x, y, z])
            
            # Mass decreases with radius
            mass = 1.0 / (1.0 + r)
            
            # Velocity for circular orbit (simplified)
            v_circular = params.rotation_velocity * np.sqrt(params.bulge_radius / (r + 0.1))
            velocity = np.array([-y, x, 0]) / (r + 0.1) * v_circular
            
            # Color: yellowish for bulge
            color = (1.0, 0.9, 0.7)
            radius = 0.05
            
            particles.append(Particle(position, velocity, mass, color, radius))
        
        return particles
    
    def _generate_disk(self, params: GalaxyParameters, num_particles: int) -> List[Particle]:
        """Generate disk particles with spiral arms."""
        particles = []
        
        for i in range(num_particles):
            # Distribute particles along spiral arms
            arm_index = i % params.num_arms
            progress = i / num_particles
            
            # Radius distribution (more particles near center)
            r = params.bulge_radius + (params.disk_radius - params.bulge_radius) * (progress ** 0.5)
            
            # Logarithmic spiral equation
            theta = params.arm_tightness * np.log(r / params.bulge_radius) + (2 * np.pi * arm_index / params.num_arms)
            
            # Add some scatter around the arm
            scatter = 0.3 * (r / params.disk_radius)
            theta += np.random.normal(0, scatter)
            
            # Position in disk plane
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            z = np.random.normal(0, 0.1 * (r / params.disk_radius))
            
            position = np.array([x, y, z])
            
            # Mass distribution
            mass = 0.5 / (1.0 + r / params.disk_radius)
            
            # Velocity for circular orbit with dark matter
            v_circular = self._compute_rotation_velocity(r, params)
            velocity = np.array([-y, x, 0]) / (r + 0.1) * v_circular
            
            # Color: bluish for young stars in arms
            color = (0.7, 0.8, 1.0)
            radius = 0.03
            
            particles.append(Particle(position, velocity, mass, color, radius))
        
        return particles
    
    def _compute_rotation_velocity(self, r: float, params: GalaxyParameters) -> float:
        """
        Compute rotation velocity including dark matter halo.
        
        Uses a simplified model combining disk mass and dark matter halo.
        """
        # Disk contribution (Keplerian)
        v_disk = params.rotation_velocity * np.sqrt(params.disk_radius / (r + params.bulge_radius))
        
        # Dark matter halo contribution (flat rotation curve)
        v_halo = params.rotation_velocity * params.dark_matter_strength
        
        # Combine
        return np.sqrt(v_disk**2 + v_halo**2)
    
    def _apply_inclination(self, particles: List[Particle], inclination: float) -> None:
        """Apply inclination to galaxy."""
        if inclination == 0:
            return
        
        cos_i = np.cos(inclination)
        sin_i = np.sin(inclination)
        
        for particle in particles:
            # Rotate around x-axis
            y = particle.position[1]
            z = particle.position[2]
            particle.position[1] = y * cos_i - z * sin_i
            particle.position[2] = y * sin_i + z * cos_i
            
            # Also rotate velocity
            vy = particle.velocity[1]
            vz = particle.velocity[2]
            particle.velocity[1] = vy * cos_i - vz * sin_i
            particle.velocity[2] = vy * sin_i + vz * cos_i
    
    def _apply_offsets(
        self,
        particles: List[Particle],
        position_offset: Tuple[float, float, float],
        velocity_offset: Tuple[float, float, float]
    ) -> None:
        """Apply position and velocity offsets."""
        pos_offset = np.array(position_offset)
        vel_offset = np.array(velocity_offset)
        
        for particle in particles:
            particle.position += pos_offset
            particle.velocity += vel_offset
    
    def generate_random(self, num_particles: int = 10000) -> List[Particle]:
        """
        Generate a random galaxy.
        
        Args:
            num_particles: Number of particles
            
        Returns:
            List of particles
        """
        params = GalaxyParameters(
            num_arms=np.random.randint(2, 6),
            bulge_radius=np.random.uniform(0.5, 2.0),
            disk_radius=np.random.uniform(8.0, 20.0),
            arm_tightness=np.random.uniform(1.5, 3.5),
            rotation_velocity=np.random.uniform(0.8, 1.5),
            num_particles=num_particles,
            bulge_mass_fraction=np.random.uniform(0.2, 0.4),
            dark_matter_strength=np.random.uniform(0.8, 1.5),
            inclination=np.random.uniform(0.0, 1.0)
        )
        
        return self.generate(params)
