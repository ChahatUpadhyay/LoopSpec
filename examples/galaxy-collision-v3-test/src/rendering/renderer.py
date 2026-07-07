"""Vispy GPU-accelerated particle renderer. (C22, C23-C25, C28, C31, C61)"""
import numpy as np
from vispy import scene
from vispy.scene import visuals


class GalaxyRenderer:
    """GPU-accelerated particle renderer using Vispy SceneCanvas.
    
    Renders particles as point sprites with mass-based coloring,
    supports zoom/pan/orbit camera controls.
    
    Criteria: C22 (30+ FPS), C23 (zoom), C24 (pan), C25 (orbit),
              C28 (coloring), C31 (particle view), C61 (dynamic sizing)
    """
    
    def __init__(self, parent=None):
        """Initialize renderer.
        
        Args:
            parent: PyQt6 widget parent for embedding
        """
        self.canvas = scene.SceneCanvas(
            keys='interactive', 
            show=False,
            parent=parent,
            bgcolor='#0a0a1a',
        )
        
        self.view = self.canvas.central_widget.add_view()
        
        # Turntable camera for zoom/pan/orbit (C23, C24, C25)
        self.view.camera = scene.TurntableCamera(
            distance=8.0,
            elevation=30,
            azimuth=45,
            fov=60,
        )
        
        # Scatter plot for particles (C31)
        self.scatter = visuals.Markers(parent=self.view.scene)
        self.scatter.set_gl_state('translucent', depth_test=False)
        
        # FPS tracking (C55)
        self._frame_count = 0
        self._fps = 0.0
        self._last_fps_time = 0.0
        
    def update_particles(self, positions: np.ndarray, colors: np.ndarray,
                         radii: np.ndarray, zoom: float = 1.0) -> None:
        """Update rendered particle data.
        
        Args:
            positions: (N, 3) particle positions
            colors: (N, 4) RGBA colors (C28)
            radii: (N,) particle radii
            zoom: Current zoom level for dynamic sizing (C61)
        """
        if len(positions) == 0:
            return
        
        # Dynamic particle sizing based on zoom (C61)
        base_size = 3.0
        size = base_size / max(0.1, zoom * 0.1)
        sizes = np.clip(radii * size * 100, 1.0, 20.0)
        
        self.scatter.set_data(
            pos=positions.astype(np.float32),
            face_color=colors,
            size=sizes,
            edge_width=0,
            edge_color=None,
        )
    
    def get_fps(self) -> float:
        """Get current rendering FPS. (C55)"""
        import time
        now = time.perf_counter()
        self._frame_count += 1
        
        elapsed = now - self._last_fps_time
        if elapsed >= 1.0:
            self._fps = self._frame_count / elapsed
            self._frame_count = 0
            self._last_fps_time = now
        
        return self._fps
    
    def get_widget(self):
        """Get the native Qt widget for embedding in PyQt6."""
        return self.canvas.native
    
    def save_screenshot(self, filepath: str) -> None:
        """Save current frame as image. (C40)"""
        img = self.canvas.render()
        from PIL import Image
        Image.fromarray(img).save(filepath)
