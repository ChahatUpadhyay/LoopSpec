"""
Collision presets for galaxy interactions.

Provides predefined configurations for different types of galaxy collisions.
"""

import numpy as np
from typing import List, Tuple
from galaxy.spiral_generator import SpiralGalaxyGenerator, GalaxyParameters
from physics.particle import Particle


class CollisionPresets:
    """
    Predefined collision configurations for galaxy interactions.
    
    Provides head-on and fly-by collision presets with scientifically
    plausible initial conditions.
    """
    
    @staticmethod
    def head_on_collision(
        num_particles: int = 10000,
        separation: float = 30.0,
        velocity: float = 1.0
    ) -> List[Particle]:
        """
        Create a head-on collision between two galaxies.
        
        Two galaxies approach each other directly along the x-axis.
        
        Args:
            num_particles: Total particles (split between galaxies)
            separation: Initial separation distance
            velocity: Approach velocity
            
        Returns:
            List of particles from both galaxies
        """
        generator = SpiralGalaxyGenerator()
        
        # Create two galaxies
        particles_per_galaxy = num_particles // 2
        
        # Galaxy 1: positioned at -separation/2, moving right
        params1 = GalaxyParameters(
            num_arms=4,
            bulge_radius=1.5,
            disk_radius=15.0,
            num_particles=particles_per_galaxy,
            position_offset=(-separation/2, 0, 0),
            velocity_offset=(velocity, 0, 0)
        )
        galaxy1 = generator.generate(params1)
        
        # Galaxy 2: positioned at +separation/2, moving left
        params2 = GalaxyParameters(
            num_arms=3,
            bulge_radius=1.5,
            disk_radius=15.0,
            num_particles=particles_per_galaxy,
            position_offset=(separation/2, 0, 0),
            velocity_offset=(-velocity, 0, 0)
        )
        galaxy2 = generator.generate(params2)
        
        return galaxy1 + galaxy2
    
    @staticmethod
    def fly_by_collision(
        num_particles: int = 10000,
        separation: float = 30.0,
        velocity: float = 1.0,
        impact_parameter: float = 10.0
    ) -> List[Particle]:
        """
        Create a fly-by collision between two galaxies.
        
        Two galaxies pass near each other with an offset (impact parameter).
        
        Args:
            num_particles: Total particles (split between galaxies)
            separation: Initial separation distance
            velocity: Approach velocity
            impact_parameter: Perpendicular offset for fly-by
            
        Returns:
            List of particles from both galaxies
        """
        generator = SpiralGalaxyGenerator()
        
        # Create two galaxies
        particles_per_galaxy = num_particles // 2
        
        # Galaxy 1: positioned at (-separation/2, -impact_parameter/2, 0), moving right
        params1 = GalaxyParameters(
            num_arms=4,
            bulge_radius=1.5,
            disk_radius=15.0,
            num_particles=particles_per_galaxy,
            position_offset=(-separation/2, -impact_parameter/2, 0),
            velocity_offset=(velocity, 0, 0)
        )
        galaxy1 = generator.generate(params1)
        
        # Galaxy 2: positioned at (+separation/2, +impact_parameter/2, 0), moving left
        params2 = GalaxyParameters(
            num_arms=3,
            bulge_radius=1.5,
            disk_radius=15.0,
            num_particles=particles_per_galaxy,
            position_offset=(separation/2, impact_parameter/2, 0),
            velocity_offset=(-velocity, 0, 0)
        )
        galaxy2 = generator.generate(params2)
        
        return galaxy1 + galaxy2
    
    @staticmethod
    def retrograde_collision(
        num_particles: int = 10000,
        separation: float = 30.0,
        velocity: float = 1.0
    ) -> List[Particle]:
        """
        Create a retrograde collision (galaxies rotating in opposite directions).
        
        Args:
            num_particles: Total particles (split between galaxies)
            separation: Initial separation distance
            velocity: Approach velocity
            
        Returns:
            List of particles from both galaxies
        """
        generator = SpiralGalaxyGenerator()
        
        particles_per_galaxy = num_particles // 2
        
        # Galaxy 1: normal rotation
        params1 = GalaxyParameters(
            num_arms=4,
            bulge_radius=1.5,
            disk_radius=15.0,
            num_particles=particles_per_galaxy,
            position_offset=(-separation/2, 0, 0),
            velocity_offset=(velocity, 0, 0)
        )
        galaxy1 = generator.generate(params1)
        
        # Galaxy 2: reverse rotation (negative rotation velocity)
        params2 = GalaxyParameters(
            num_arms=3,
            bulge_radius=1.5,
            disk_radius=15.0,
            rotation_velocity=-1.2,  # Negative for retrograde
            num_particles=particles_per_galaxy,
            position_offset=(separation/2, 0, 0),
            velocity_offset=(-velocity, 0, 0)
        )
        galaxy2 = generator.generate(params2)
        
        return galaxy1 + galaxy2
    
    @staticmethod
    def prograde_collision(
        num_particles: int = 10000,
        separation: float = 30.0,
        velocity: float = 1.0
    ) -> List[Particle]:
        """
        Create a prograde collision (galaxies rotating in same direction).
        
        Args:
            num_particles: Total particles (split between galaxies)
            separation: Initial separation distance
            velocity: Approach velocity
            
        Returns:
            List of particles from both galaxies
        """
        generator = SpiralGalaxyGenerator()
        
        particles_per_galaxy = num_particles // 2
        
        # Both galaxies with same rotation direction
        params1 = GalaxyParameters(
            num_arms=4,
            bulge_radius=1.5,
            disk_radius=15.0,
            rotation_velocity=1.2,
            num_particles=particles_per_galaxy,
            position_offset=(-separation/2, 0, 0),
            velocity_offset=(velocity, 0, 0)
        )
        galaxy1 = generator.generate(params1)
        
        params2 = GalaxyParameters(
            num_arms=3,
            bulge_radius=1.5,
            disk_radius=15.0,
            rotation_velocity=1.2,  # Same direction
            num_particles=particles_per_galaxy,
            position_offset=(separation/2, 0, 0),
            velocity_offset=(-velocity, 0, 0)
        )
        galaxy2 = generator.generate(params2)
        
        return galaxy1 + galaxy2
