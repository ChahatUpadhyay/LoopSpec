"""Visual effects: bloom, trails, heatmap, density. (C26, C27, C29, C32-C34)"""
import numpy as np
from vispy import scene
from vispy.scene import visuals


class TrailEffect:
    """Particle trail visualization. (C26)
    
    Stores last N positions and renders as fading lines.
    """
    
    def __init__(self, view: scene.ViewBox, max_history: int = 20):
        self.view = view
        self.max_history = max_history
        self.history: list[np.ndarray] = []
        self.trail_visual = None
        self.enabled = False
    
    def update(self, positions: np.ndarray):
        """Add current positions to history."""
        if not self.enabled:
            return
        self.history.append(positions.copy())
        if len(self.history) > self.max_history:
            self.history.pop(0)
    
    def render(self):
        """Render trails as fading lines."""
        if not self.enabled or len(self.history) < 2:
            return
        
        # Sample every 10th particle for performance
        n = self.history[0].shape[0]
        sample_idx = np.arange(0, n, max(1, n // 200))
        
        # Build line segments
        segments = []
        colors = []
        for i in range(len(self.history) - 1):
            alpha = (i + 1) / len(self.history) * 0.3
            for idx in sample_idx:
                segments.append(self.history[i][idx])
                segments.append(self.history[i + 1][idx])
                colors.append([0.3, 0.5, 1.0, alpha])
                colors.append([0.3, 0.5, 1.0, alpha])
        
        if segments:
            if self.trail_visual is not None:
                self.trail_visual.parent = None
            pos = np.array(segments, dtype=np.float32)
            col = np.array(colors, dtype=np.float32)
            self.trail_visual = visuals.Line(
                pos=pos, color=col, connect='segments',
                parent=self.view.scene
            )
    
    def clear(self):
        self.history.clear()
        if self.trail_visual is not None:
            self.trail_visual.parent = None
            self.trail_visual = None


class DensityHeatmap:
    """2D density heatmap projection. (C29, C32)"""
    
    def __init__(self, resolution: int = 64):
        self.resolution = resolution
    
    def compute(self, positions: np.ndarray, extent: float = 10.0) -> np.ndarray:
        """Compute 2D density field (XY projection).
        
        Returns (resolution, resolution) density array.
        """
        res = self.resolution
        density = np.zeros((res, res), dtype=np.float32)
        
        # Project to XY plane, bin into grid
        x = positions[:, 0]
        y = positions[:, 1]
        
        # Map to grid indices
        xi = ((x + extent) / (2 * extent) * res).astype(int)
        yi = ((y + extent) / (2 * extent) * res).astype(int)
        
        # Clip to bounds
        mask = (xi >= 0) & (xi < res) & (yi >= 0) & (yi < res)
        xi, yi = xi[mask], yi[mask]
        
        np.add.at(density, (xi, yi), 1)
        
        # Smooth with simple box filter
        from scipy.ndimage import gaussian_filter
        try:
            density = gaussian_filter(density, sigma=1.5)
        except ImportError:
            pass
        
        return density


class VelocityField:
    """Velocity field visualization (arrow glyphs). (C33)"""
    
    def __init__(self, grid_size: int = 8):
        self.grid_size = grid_size
    
    def compute(self, positions: np.ndarray, velocities: np.ndarray, 
                extent: float = 10.0) -> tuple[np.ndarray, np.ndarray]:
        """Compute velocity field on grid.
        
        Returns (grid_positions, velocity_vectors) for arrow rendering.
        """
        gs = self.grid_size
        grid_pos = []
        grid_vel = []
        
        step = 2 * extent / gs
        for i in range(gs):
            for j in range(gs):
                cx = -extent + (i + 0.5) * step
                cy = -extent + (j + 0.5) * step
                
                # Average velocity of particles in this cell
                mask = (
                    (positions[:, 0] > cx - step/2) & (positions[:, 0] < cx + step/2) &
                    (positions[:, 1] > cy - step/2) & (positions[:, 1] < cy + step/2)
                )
                if np.any(mask):
                    avg_vel = velocities[mask].mean(axis=0)
                    grid_pos.append([cx, cy, 0])
                    grid_vel.append(avg_vel)
        
        if grid_pos:
            return np.array(grid_pos), np.array(grid_vel)
        return np.zeros((0, 3)), np.zeros((0, 3))


class PotentialField:
    """Gravitational potential field visualization. (C34)"""
    
    def __init__(self, resolution: int = 32):
        self.resolution = resolution
    
    def compute(self, positions: np.ndarray, masses: np.ndarray,
                extent: float = 10.0, softening: float = 0.1) -> np.ndarray:
        """Compute gravitational potential on 2D grid.
        
        Returns (resolution, resolution) potential array.
        """
        res = self.resolution
        potential = np.zeros((res, res), dtype=np.float32)
        
        # Grid coordinates
        x = np.linspace(-extent, extent, res)
        y = np.linspace(-extent, extent, res)
        
        # Sample particles for speed
        n = len(masses)
        if n > 500:
            idx = np.random.choice(n, 500, replace=False)
            pos_sample = positions[idx]
            mass_sample = masses[idx] * (n / 500)
        else:
            pos_sample = positions
            mass_sample = masses
        
        for i in range(res):
            for j in range(res):
                dx = pos_sample[:, 0] - x[i]
                dy = pos_sample[:, 1] - y[j]
                r = np.sqrt(dx**2 + dy**2 + softening**2)
                potential[i, j] = -np.sum(mass_sample / r)
        
        return potential
