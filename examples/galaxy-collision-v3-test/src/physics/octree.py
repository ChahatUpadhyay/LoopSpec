"""Barnes-Hut Octree for O(N log N) gravity. (C2, C57)"""
import numpy as np
from typing import Optional


class OctreeNode:
    """A node in the Barnes-Hut octree.
    
    Each node represents a cubic region of space and stores:
    - Total mass of contained particles
    - Center of mass position
    - Child nodes (up to 8 octants)
    """
    __slots__ = ['center', 'half_size', 'mass', 'com', 'children', 'is_leaf', 'particle_idx']
    
    def __init__(self, center: np.ndarray, half_size: float):
        self.center = center
        self.half_size = half_size
        self.mass = 0.0
        self.com = np.zeros(3)
        self.children: list[Optional['OctreeNode']] = [None] * 8
        self.is_leaf = True
        self.particle_idx = -1


def _get_octant(pos: np.ndarray, center: np.ndarray) -> int:
    """Determine which octant a position falls into."""
    octant = 0
    if pos[0] >= center[0]: octant |= 1
    if pos[1] >= center[1]: octant |= 2
    if pos[2] >= center[2]: octant |= 4
    return octant


def _octant_center(parent_center: np.ndarray, half_size: float, octant: int) -> np.ndarray:
    """Get the center of a child octant."""
    offset = half_size * 0.5
    return np.array([
        parent_center[0] + (offset if octant & 1 else -offset),
        parent_center[1] + (offset if octant & 2 else -offset),
        parent_center[2] + (offset if octant & 4 else -offset),
    ])


def build_octree(positions: np.ndarray, masses: np.ndarray) -> Optional[OctreeNode]:
    """Build a Barnes-Hut octree from particle positions and masses.
    
    Args:
        positions: (N, 3) array of particle positions
        masses: (N,) array of particle masses
    
    Returns:
        Root OctreeNode, or None if no particles
    """
    n = len(masses)
    if n == 0:
        return None
    
    # Determine bounding box
    min_pos = positions.min(axis=0)
    max_pos = positions.max(axis=0)
    center = (min_pos + max_pos) / 2.0
    half_size = np.max(max_pos - min_pos) / 2.0 * 1.01  # slight padding
    
    if half_size == 0:
        half_size = 1.0
    
    root = OctreeNode(center, half_size)
    
    for i in range(n):
        _insert(root, positions[i], masses[i], i)
    
    return root


def _insert(node: OctreeNode, pos: np.ndarray, mass: float, idx: int):
    """Insert a particle into the octree."""
    if node.mass == 0 and node.is_leaf:
        # Empty leaf — place particle here
        node.mass = mass
        node.com = pos.copy()
        node.particle_idx = idx
        return
    
    if node.is_leaf:
        # Leaf with existing particle — subdivide
        old_pos = node.com.copy()
        old_mass = node.mass
        old_idx = node.particle_idx
        node.is_leaf = False
        node.particle_idx = -1
        
        # Re-insert existing particle
        octant = _get_octant(old_pos, node.center)
        child_center = _octant_center(node.center, node.half_size, octant)
        node.children[octant] = OctreeNode(child_center, node.half_size * 0.5)
        _insert(node.children[octant], old_pos, old_mass, old_idx)
    
    # Insert new particle into appropriate child
    octant = _get_octant(pos, node.center)
    if node.children[octant] is None:
        child_center = _octant_center(node.center, node.half_size, octant)
        node.children[octant] = OctreeNode(child_center, node.half_size * 0.5)
    _insert(node.children[octant], pos, mass, idx)
    
    # Update mass and center of mass
    total_mass = node.mass + mass
    node.com = (node.com * node.mass + pos * mass) / total_mass
    node.mass = total_mass


def compute_force_bh(node: Optional[OctreeNode], pos: np.ndarray, 
                     softening: float, theta: float) -> np.ndarray:
    """Compute gravitational force on a particle using Barnes-Hut approximation.
    
    Args:
        node: Root of octree
        pos: Position of target particle
        softening: Softening length to avoid singularities (C3)
        theta: Opening angle parameter (larger = faster but less accurate)
    
    Returns:
        Force vector (3,)
    """
    if node is None or node.mass == 0:
        return np.zeros(3)
    
    dx = node.com - pos
    r_sq = np.sum(dx**2) + softening**2
    r = np.sqrt(r_sq)
    
    if node.is_leaf:
        if r < softening * 0.01:  # Skip self-interaction
            return np.zeros(3)
        return node.mass * dx / (r_sq * r)
    
    # Barnes-Hut criterion: s/d < theta
    s = node.half_size * 2  # node size
    if s / r < theta:
        # Treat as single body
        return node.mass * dx / (r_sq * r)
    
    # Recurse into children
    force = np.zeros(3)
    for child in node.children:
        if child is not None:
            force += compute_force_bh(child, pos, softening, theta)
    return force
