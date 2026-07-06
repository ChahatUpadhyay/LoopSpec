"""
GPU-accelerated renderer using vispy for OpenGL rendering.

Implements particle rendering using vispy for GPU-accelerated visualization.
"""

import numpy as np
from typing import List, Optional
try:
    from vispy import scene, app
    from vispy.visuals.transforms import STTransform
    VISPY_AVAILABLE = True
except ImportError:
    VISPY_AVAILABLE = False
    print("vispy not available")

from physics.particle import Particle


class OpenGLRenderer:
    """
    GPU-accelerated renderer using vispy.
    
    Provides particle rendering with GPU acceleration for high performance.
    
    Attributes:
        canvas: Vispy SceneCanvas
        view: Vispy ViewBox
        scatter: MarkersVisual for particles
        fps: Current frames per second
    """
    
    def __init__(self, size: tuple = (1024, 768)):
        """
        Initialize vispy renderer.
        
        Args:
            size: Window size (width, height)
        """
        if not VISPY_AVAILABLE:
            raise ImportError("vispy is required for GPU rendering")
        
        self.canvas = scene.SceneCanvas(keys='interactive', size=size, show=False, vsync=True)
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = 'turntable'
        self.view.camera.set_range()
        
        self.scatter = None
        self.fps = 0.0
        self.frame_count = 0
        self.last_time = 0
        
    def set_particles(self, particles: List[Particle]) -> None:
        """
        Set particles for rendering.
        
        Args:
            particles: List of particles to render
        """
        if not particles:
            if self.scatter:
                self.scatter.parent = None
                self.scatter = None
            return
        
        # Extract positions and colors
        positions = np.array([p.position for p in particles], dtype=np.float32)
        colors = np.array([p.color for p in particles], dtype=np.float32)
        sizes = np.array([p.radius * 10 for p in particles], dtype=np.float32)
        
        # Create or update scatter plot
        if self.scatter is None:
            self.scatter = scene.visuals.Markers(parent=self.view.scene)
        
        self.scatter.set_data(
            pos=positions,
            face_color=colors,
            size=sizes,
            edge_width=0,
            edge_color=None
        )
        
        # Update camera range
        self.view.camera.set_range(
            x=(positions[:, 0].min(), positions[:, 0].max()),
            y=(positions[:, 1].min(), positions[:, 1].max()),
            z=(positions[:, 2].min(), positions[:, 2].max())
        )
    
    def update(self) -> None:
        """Update the renderer (called each frame)."""
        import time
        current_time = time.time()
        self.frame_count += 1
        
        if current_time - self.last_time >= 1.0:
            self.fps = self.frame_count / (current_time - self.last_time)
            self.frame_count = 0
            self.last_time = current_time
        
        self.canvas.update()
    
    def get_fps(self) -> float:
        """Get current FPS."""
        return self.fps
    
    def reset_camera(self) -> None:
        """Reset camera to default position."""
        self.view.camera.set_range()
    
    def close(self) -> None:
        """Close the renderer."""
        self.canvas.close()
