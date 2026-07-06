"""
Main window for galaxy collision simulation.

PyQt6 main window integrating vispy canvas, control panel, and analysis panel.
"""

import sys
import numpy as np
from typing import List, Optional
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QSlider, QComboBox, QGroupBox,
    QDockWidget, QSpinBox, QDoubleSpinBox
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QAction
from renderer.opengl_renderer import OpenGLRenderer
from physics.particle import Particle
from physics.integrator import LeapfrogIntegrator
from physics.barnes_hut import BarnesHutTree
from physics.gravity import (
    compute_total_energy, compute_kinetic_energy,
    compute_potential_energy, compute_momentum,
    compute_angular_momentum, compute_center_of_mass
)
from galaxy.spiral_generator import SpiralGalaxyGenerator
from galaxy.collision_presets import CollisionPresets


class MainWindow(QMainWindow):
    """
    Main window for galaxy collision simulation.
    
    Integrates OpenGL renderer, control panel, and analysis panel.
    
    Attributes:
        renderer: OpenGL renderer
        particles: Current particle list
        integrator: Leapfrog integrator
        barnes_hut: Barnes-Hut tree
        timer: Simulation timer
        running: Simulation running state
        initial_particles: Initial state for reset
    """
    
    def __init__(self):
        """Initialize main window."""
        super().__init__()
        self.setWindowTitle("Galaxy Collision Simulation")
        self.resize(1400, 900)
        
        # Simulation state
        self.particles: List[Particle] = []
        self.initial_particles: List[Particle] = []
        self.running = False
        self.speed_multiplier = 1.0
        self.frame_count = 0
        
        # Physics components
        self.integrator = LeapfrogIntegrator(dt=0.01, adaptive=False, G=1.0, softening=0.1)
        self.barnes_hut = BarnesHutTree(theta=0.8, softening=0.1, G=1.0)  # Higher theta for faster performance
        
        # Disable GPU gravity due to CUDA library issues
        self.use_gpu = False
        print("Using CPU Barnes-Hut for physics")
        
        # Renderer
        self.renderer = OpenGLRenderer(size=(1024, 768))
        
        # Timer for simulation loop
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)
        self.timer.setInterval(16)  # ~60 FPS target
        
        # Setup UI
        self.setup_ui()
        self.setup_menu()
        
        # Initialize with default galaxy
        self.generate_galaxy()
        
    def setup_ui(self):
        """Setup user interface."""
        # Central widget with renderer
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)
        
        # Embed vispy canvas in PyQt6
        layout.addWidget(self.renderer.canvas.native, stretch=3)
        
        # Control panel dock
        control_dock = QDockWidget("Controls", self)
        control_dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        self.control_panel = self.create_control_panel()
        control_dock.setWidget(self.control_panel)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, control_dock)
        
        # Analysis panel dock
        analysis_dock = QDockWidget("Analysis", self)
        analysis_dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        self.analysis_panel = self.create_analysis_panel()
        analysis_dock.setWidget(self.analysis_panel)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, analysis_dock)
        
    def create_control_panel(self) -> QWidget:
        """Create control panel widget."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Simulation controls
        sim_group = QGroupBox("Simulation")
        sim_layout = QVBoxLayout()
        
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.toggle_simulation)
        sim_layout.addWidget(self.play_button)
        
        step_button = QPushButton("Step")
        step_button.clicked.connect(self.step_simulation)
        sim_layout.addWidget(step_button)
        
        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(self.reset_simulation)
        sim_layout.addWidget(reset_button)
        
        snapshot_button = QPushButton("Snapshot")
        snapshot_button.clicked.connect(self.save_snapshot)
        sim_layout.addWidget(snapshot_button)
        
        sim_group.setLayout(sim_layout)
        layout.addWidget(sim_group)
        
        # Speed control
        speed_group = QGroupBox("Speed")
        speed_layout = QVBoxLayout()
        
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setRange(1, 100)
        self.speed_slider.setValue(10)
        self.speed_slider.valueChanged.connect(self.update_speed)
        speed_layout.addWidget(self.speed_slider)
        
        self.speed_label = QLabel("Speed: 1.0x")
        speed_layout.addWidget(self.speed_label)
        
        speed_group.setLayout(speed_layout)
        layout.addWidget(speed_group)
        
        # Galaxy generation
        galaxy_group = QGroupBox("Galaxy")
        galaxy_layout = QVBoxLayout()
        
        self.galaxy_type = QComboBox()
        self.galaxy_type.addItems(["Milky Way", "Andromeda", "Random", "Head-on Collision", "Fly-by Collision"])
        self.galaxy_type.currentTextChanged.connect(self.generate_galaxy)
        galaxy_layout.addWidget(self.galaxy_type)
        
        particle_count_layout = QHBoxLayout()
        particle_count_layout.addWidget(QLabel("Particles:"))
        self.particle_count = QSpinBox()
        self.particle_count.setRange(100, 5000)
        self.particle_count.setValue(2000)
        self.particle_count.setSingleStep(500)
        particle_count_layout.addWidget(self.particle_count)
        galaxy_layout.addLayout(particle_count_layout)
        
        generate_button = QPushButton("Generate")
        generate_button.clicked.connect(self.generate_galaxy)
        galaxy_layout.addWidget(generate_button)
        
        galaxy_group.setLayout(galaxy_layout)
        layout.addWidget(galaxy_group)
        
        layout.addStretch()
        return panel
    
    def create_analysis_panel(self) -> QWidget:
        """Create analysis panel widget."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Energy metrics
        energy_group = QGroupBox("Energy")
        energy_layout = QVBoxLayout()
        
        self.total_energy_label = QLabel("Total: 0.00")
        energy_layout.addWidget(self.total_energy_label)
        
        self.kinetic_energy_label = QLabel("Kinetic: 0.00")
        energy_layout.addWidget(self.kinetic_energy_label)
        
        self.potential_energy_label = QLabel("Potential: 0.00")
        energy_layout.addWidget(self.potential_energy_label)
        
        energy_group.setLayout(energy_layout)
        layout.addWidget(energy_group)
        
        # Momentum metrics
        momentum_group = QGroupBox("Momentum")
        momentum_layout = QVBoxLayout()
        
        self.momentum_label = QLabel("Momentum: (0.00, 0.00, 0.00)")
        momentum_layout.addWidget(self.momentum_label)
        
        self.angular_momentum_label = QLabel("Angular L: (0.00, 0.00, 0.00)")
        momentum_layout.addWidget(self.angular_momentum_label)
        
        self.center_of_mass_label = QLabel("Center of Mass: (0.00, 0.00, 0.00)")
        momentum_layout.addWidget(self.center_of_mass_label)
        
        momentum_group.setLayout(momentum_layout)
        layout.addWidget(momentum_group)
        
        # Performance metrics
        perf_group = QGroupBox("Performance")
        perf_layout = QVBoxLayout()
        
        self.fps_label = QLabel("FPS: 0")
        perf_layout.addWidget(self.fps_label)
        
        self.physics_fps_label = QLabel("Physics FPS: 0")
        perf_layout.addWidget(self.physics_fps_label)
        
        self.particle_count_label = QLabel("Particles: 0")
        perf_layout.addWidget(self.particle_count_label)
        
        perf_group.setLayout(perf_layout)
        layout.addWidget(perf_group)
        
        layout.addStretch()
        return panel
    
    def setup_menu(self):
        """Setup menu bar."""
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu("File")
        
        save_action = QAction("Save State", self)
        save_action.triggered.connect(self.save_state)
        file_menu.addAction(save_action)
        
        load_action = QAction("Load State", self)
        load_action.triggered.connect(self.load_state)
        file_menu.addAction(load_action)
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
    
    def generate_galaxy(self):
        """Generate galaxy based on selection."""
        galaxy_type = self.galaxy_type.currentText()
        num_particles = self.particle_count.value()
        
        generator = SpiralGalaxyGenerator()
        
        if galaxy_type == "Milky Way":
            params = SpiralGalaxyGenerator.MILKY_WAY
            params.num_particles = num_particles
            self.particles = generator.generate(params)
        elif galaxy_type == "Andromeda":
            params = SpiralGalaxyGenerator.ANDROMEDA
            params.num_particles = num_particles
            self.particles = generator.generate(params)
        elif galaxy_type == "Random":
            self.particles = generator.generate_random(num_particles)
        elif galaxy_type == "Head-on Collision":
            self.particles = CollisionPresets.head_on_collision(num_particles)
        elif galaxy_type == "Fly-by Collision":
            self.particles = CollisionPresets.fly_by_collision(num_particles)
        
        # Store initial state for reset (deep copy)
        self.initial_particles = [Particle(p.position.copy(), p.velocity.copy(), p.mass, np.array(p.color), p.radius) for p in self.particles]
        
        # Update renderer
        self.renderer.set_particles(self.particles)
        self.renderer.update()
        
        # Update analysis
        self.update_analysis()
        
        # Reset integrator and frame count
        self.integrator.reset()
        self.frame_count = 0
    
    def toggle_simulation(self):
        """Toggle simulation play/pause."""
        if self.running:
            self.timer.stop()
            self.play_button.setText("Play")
            self.running = False
        else:
            self.timer.start()
            self.play_button.setText("Pause")
            self.running = True
    
    def step_simulation(self):
        """Step simulation by one timestep."""
        if self.particles:
            self.barnes_hut.build(self.particles)
            self.integrator.step(self.particles, use_barnes_hut=True, barnes_hut_tree=self.barnes_hut)
            self.renderer.set_particles(self.particles)
            self.renderer.update()
            self.update_analysis()
    
    def reset_simulation(self):
        """Reset simulation to initial state."""
        if self.running:
            self.toggle_simulation()
        
        if self.initial_particles:
            self.particles = [Particle(p.position.copy(), p.velocity.copy(), p.mass, np.array(p.color), p.radius) for p in self.initial_particles]
        else:
            self.particles = []
        
        self.integrator.reset()
        self.renderer.set_particles(self.particles)
        self.renderer.update()
        self.update_analysis()
        self.frame_count = 0
    
    def update_simulation(self):
        """Update simulation (called by timer)."""
        if self.running and self.particles:
            # Use CPU Barnes-Hut for physics
            self.barnes_hut.build(self.particles)
            self.integrator.step(self.particles, use_barnes_hut=True, barnes_hut_tree=self.barnes_hut)
            
            # Update renderer
            self.renderer.set_particles(self.particles)
            self.renderer.update()
            
            # Disable analysis updates during simulation for performance
            self.frame_count += 1
    
    def update_speed(self):
        """Update simulation speed."""
        value = self.speed_slider.value() / 10.0
        self.speed_multiplier = value
        self.speed_label.setText(f"Speed: {value:.1f}x")
    
    def update_analysis(self):
        """Update analysis panel with current metrics."""
        if not self.particles:
            return
        
        # Energy
        total_e = compute_total_energy(self.particles, softening=0.1, G=1.0)
        kinetic_e = compute_kinetic_energy(self.particles)
        potential_e = compute_potential_energy(self.particles, softening=0.1, G=1.0)
        
        self.total_energy_label.setText(f"Total: {total_e:.2f}")
        self.kinetic_energy_label.setText(f"Kinetic: {kinetic_e:.2f}")
        self.potential_energy_label.setText(f"Potential: {potential_e:.2f}")
        
        # Momentum
        momentum = compute_momentum(self.particles)
        angular_momentum = compute_angular_momentum(self.particles)
        center_of_mass = compute_center_of_mass(self.particles)
        
        self.momentum_label.setText(f"Momentum: ({momentum[0]:.2f}, {momentum[1]:.2f}, {momentum[2]:.2f})")
        self.angular_momentum_label.setText(f"Angular L: ({angular_momentum[0]:.2f}, {angular_momentum[1]:.2f}, {angular_momentum[2]:.2f})")
        self.center_of_mass_label.setText(f"Center of Mass: ({center_of_mass[0]:.2f}, {center_of_mass[1]:.2f}, {center_of_mass[2]:.2f})")
        
        # Performance
        fps = self.renderer.get_fps()
        self.fps_label.setText(f"FPS: {fps:.1f}")
        self.physics_fps_label.setText(f"Physics FPS: {fps:.1f}")
        self.particle_count_label.setText(f"Particles: {len(self.particles)}")
    
    def save_snapshot(self):
        """Save current frame as snapshot."""
        if self.particles:
            import os
            from datetime import datetime
            
            # Create snapshots directory if it doesn't exist
            if not os.path.exists('snapshots'):
                os.makedirs('snapshots')
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'snapshots/galaxy_{timestamp}.png'
            
            # Save the vispy canvas
            self.renderer.canvas.save(filename)
            print(f"Snapshot saved: {filename}")
        else:
            print("No particles to snapshot")
    
    def save_state(self):
        """Save simulation state."""
        # Placeholder for save functionality
        print("State saved (placeholder)")
    
    def load_state(self):
        """Load simulation state."""
        # Placeholder for load functionality
        print("State loaded (placeholder)")
    
    def closeEvent(self, event):
        """Handle window close event."""
        self.renderer.close()
        event.accept()
        event.accept()


def main():
    """Main entry point."""
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
