"""
Barnes-Hut octree for O(N log N) N-body force calculation.

Implements spatial partitioning using an octree data structure to accelerate
gravitational force calculations from O(N^2) to O(N log N).
"""

import numpy as np
from typing import List, Optional
from physics.particle import Particle


class OctreeNode:
    """
    A node in the Barnes-Hut octree.
    
    Attributes:
        center: Center position of this node's region
        size: Size of this node's region (half-width)
        particles: List of particles in this node (leaf nodes only)
        children: Eight child nodes (internal nodes only)
        total_mass: Total mass of particles in this node
        center_of_mass: Center of mass of particles in this node
    """
    
    def __init__(self, center: np.ndarray, size: float):
        self.center = np.asarray(center, dtype=np.float64)
        self.size = size
        self.particles: List[Particle] = []
        self.children: List[Optional['OctreeNode']] = [None] * 8
        self.total_mass = 0.0
        self.center_of_mass = np.zeros(3)
        
    def is_leaf(self) -> bool:
        """Check if this node is a leaf (no children)."""
        return all(child is None for child in self.children)
    
    def contains(self, position: np.ndarray) -> bool:
        """Check if a position is within this node's region."""
        return np.all(np.abs(position - self.center) <= self.size)
    
    def get_child_index(self, position: np.ndarray) -> int:
        """
        Get the index of the child node that contains a position.
        
        Returns 0-7 based on octant:
        0: +x, +y, +z
        1: -x, +y, +z
        2: +x, -y, +z
        3: -x, -y, +z
        4: +x, +y, -z
        5: -x, +y, -z
        6: +x, -y, -z
        7: -x, -y, -z
        """
        index = 0
        if position[0] < self.center[0]:
            index |= 1
        if position[1] < self.center[1]:
            index |= 2
        if position[2] < self.center[2]:
            index |= 4
        return index
    
    def create_child(self, index: int) -> 'OctreeNode':
        """Create a child node for the given octant."""
        child_size = self.size / 2.0
        child_center = self.center.copy()
        
        if index & 1:
            child_center[0] -= child_size
        else:
            child_center[0] += child_size
            
        if index & 2:
            child_center[1] -= child_size
        else:
            child_center[1] += child_size
            
        if index & 4:
            child_center[2] -= child_size
        else:
            child_center[2] += child_size
            
        return OctreeNode(child_center, child_size)


class BarnesHutTree:
    """
    Barnes-Hut octree for accelerated N-body force calculation.
    
    Uses the Barnes-Hut algorithm to approximate gravitational forces
    in O(N log N) time instead of O(N^2) for direct summation.
    
    Attributes:
        root: Root node of the octree
        theta: Opening angle parameter (smaller = more accurate, slower)
        softening: Softening parameter for force calculation
        G: Gravitational constant
    """
    
    def __init__(self, theta: float = 0.5, softening: float = 0.1, G: float = 1.0):
        """
        Initialize Barnes-Hut tree.
        
        Args:
            theta: Opening angle (typically 0.5-1.0)
            softening: Softening parameter
            G: Gravitational constant
        """
        self.theta = theta
        self.softening = softening
        self.G = G
        self.root: Optional[OctreeNode] = None
        
    def build(self, particles: List[Particle]) -> None:
        """
        Build the octree from a list of particles.
        
        Args:
            particles: List of particles to insert into the tree
        """
        if not particles:
            self.root = None
            return
        
        # Find bounding box
        positions = np.array([p.position for p in particles])
        min_pos = np.min(positions, axis=0)
        max_pos = np.max(positions, axis=0)
        
        # Create root node encompassing all particles
        center = (min_pos + max_pos) / 2.0
        size = np.max(max_pos - min_pos) / 2.0 + 1e-10
        self.root = OctreeNode(center, size)
        
        # Insert all particles
        for particle in particles:
            self._insert(self.root, particle)
            
        # Compute mass distribution
        self._compute_mass_distribution(self.root)
    
    def _insert(self, node: OctreeNode, particle: Particle) -> None:
        """Insert a particle into the tree."""
        if node.is_leaf():
            node.particles.append(particle)
            
            # If node has too many particles, subdivide
            if len(node.particles) > 1:
                self._subdivide(node)
        else:
            # Find appropriate child and insert
            index = node.get_child_index(particle.position)
            if node.children[index] is None:
                node.children[index] = node.create_child(index)
            self._insert(node.children[index], particle)
    
    def _subdivide(self, node: OctreeNode) -> None:
        """Subdivide a leaf node into 8 children."""
        particles = node.particles
        node.particles = []
        
        for particle in particles:
            index = node.get_child_index(particle.position)
            if node.children[index] is None:
                node.children[index] = node.create_child(index)
            self._insert(node.children[index], particle)
    
    def _compute_mass_distribution(self, node: OctreeNode) -> None:
        """Compute total mass and center of mass for each node."""
        if node.is_leaf():
            if node.particles:
                total_mass = sum(p.mass for p in node.particles)
                weighted_pos = sum(p.mass * p.position for p in node.particles)
                node.total_mass = total_mass
                node.center_of_mass = weighted_pos / total_mass if total_mass > 0 else node.center
            else:
                node.total_mass = 0.0
                node.center_of_mass = node.center
        else:
            total_mass = 0.0
            weighted_pos = np.zeros(3)
            
            for child in node.children:
                if child is not None:
                    self._compute_mass_distribution(child)
                    total_mass += child.total_mass
                    weighted_pos += child.total_mass * child.center_of_mass
            
            node.total_mass = total_mass
            node.center_of_mass = weighted_pos / total_mass if total_mass > 0 else node.center
    
    def compute_force(self, particle: Particle) -> np.ndarray:
        """
        Compute gravitational force on a particle using the Barnes-Hut approximation.
        
        Args:
            particle: Particle to compute force for
            
        Returns:
            Force vector
        """
        if self.root is None:
            return np.zeros(3)
        
        return self._compute_force_recursive(self.root, particle)
    
    def _compute_force_recursive(self, node: OctreeNode, particle: Particle) -> np.ndarray:
        """Recursively compute force using Barnes-Hut approximation."""
        if node.total_mass == 0:
            return np.zeros(3)
        
        # Vector from particle to node's center of mass
        r_vec = node.center_of_mass - particle.position
        r_mag = np.linalg.norm(r_vec)
        
        # Check if node is far enough to use approximation
        if r_mag == 0:
            return np.zeros(3)
        
        ratio = node.size / r_mag
        
        if ratio < self.theta or node.is_leaf():
            # Use node as a single mass
            softened_dist = np.sqrt(r_mag**2 + self.softening**2)
            force_mag = self.G * particle.mass * node.total_mass / (softened_dist**3)
            return force_mag * r_vec
        else:
            # Recurse into children
            force = np.zeros(3)
            for child in node.children:
                if child is not None:
                    force += self._compute_force_recursive(child, particle)
            return force
    
    def compute_all_forces(self, particles: List[Particle]) -> np.ndarray:
        """
        Compute forces on all particles using the Barnes-Hut tree.
        
        Args:
            particles: List of particles
            
        Returns:
            Array of force vectors, shape (N, 3)
        """
        forces = np.zeros((len(particles), 3))
        for i, particle in enumerate(particles):
            forces[i] = self.compute_force(particle)
        return forces
