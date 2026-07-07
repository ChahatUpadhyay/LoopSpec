"""Main application window. (C37-C44, C49-C56, C26-C27, C29, C32-C36, C41, C45-C47, C60)"""
import sys
import time
import os
import numpy as np
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QPushButton, QSlider, QComboBox, QLabel, QSpinBox, QGridLayout,
    QScrollArea, QFileDialog, QSplitter, QCheckBox, QTabWidget
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QFont

from ..physics.particles import ParticleSystem
from ..physics.integrator import LeapfrogIntegrator
from ..galaxy.presets import PRESET_MAP, head_on_collision
from ..galaxy.serialization import save_state, load_state
from ..rendering.renderer import GalaxyRenderer
from ..rendering.effects import TrailEffect, DensityHeatmap


class PhysicsWorker(QThread):
    """Physics computation on separate thread. (C58)"""
    step_done = pyqtSignal()
    
    def __init__(self, integrator: LeapfrogIntegrator, particles: ParticleSystem):
        super().__init__()
        self.integrator = integrator
        self.particles = particles
        self.running = False
        self.step_requested = False
    
    def run(self):
        while True:
            if self.running or self.step_requested:
                self.integrator.step(self.particles)
                self.step_done.emit()
                self.step_requested = False
            else:
                self.msleep(5)


class MainWindow(QMainWindow):
    """Galaxy Collision Simulation main window.
    
    Criteria: C37-C44 (UI controls), C49-C56 (analysis panel)
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Galaxy Collision Simulator — LoopSpec v3 Test")
        self.setMinimumSize(1200, 800)
        self.setStyleSheet(self._stylesheet())
        
        # --- Simulation State ---
        self.n_per_galaxy = 5000
        self.particles = head_on_collision(self.n_per_galaxy)
        self.integrator = LeapfrogIntegrator(
            softening=0.05, theta=0.8, dt=0.005,
            use_gpu=False, adaptive=True
        )
        self.is_playing = False
        self.time_scale = 1.0
        self.sim_time = 0.0
        self.frame_count = 0
        
        # --- Build UI ---
        self._build_ui()
        
        # --- Physics Thread (C58) ---
        self.physics_thread = PhysicsWorker(self.integrator, self.particles)
        self.physics_thread.step_done.connect(self._on_physics_step)
        self.physics_thread.start()
        
        # --- Render Timer ---
        self.render_timer = QTimer()
        self.render_timer.timeout.connect(self._render_frame)
        self.render_timer.start(16)  # ~60 FPS target
        
        # Initial render
        self._update_renderer()
    
    def _build_ui(self):
        """Build the complete UI layout."""
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # --- Left: Controls Panel ---
        controls_scroll = QScrollArea()
        controls_scroll.setWidgetResizable(True)
        controls_scroll.setFixedWidth(300)
        controls_widget = QWidget()
        controls_layout = QVBoxLayout(controls_widget)
        controls_layout.setSpacing(8)
        
        # Simulation Controls (C37-C39, C42)
        sim_group = QGroupBox("Simulation")
        sim_layout = QGridLayout()
        
        self.btn_play = QPushButton("▶ Play")
        self.btn_play.clicked.connect(self._toggle_play)
        sim_layout.addWidget(self.btn_play, 0, 0)
        
        self.btn_step = QPushButton("⏭ Step")  # C38
        self.btn_step.clicked.connect(self._step_once)
        sim_layout.addWidget(self.btn_step, 0, 1)
        
        self.btn_reset = QPushButton("↺ Reset")  # C39
        self.btn_reset.clicked.connect(self._reset_simulation)
        sim_layout.addWidget(self.btn_reset, 1, 0, 1, 2)
        
        sim_layout.addWidget(QLabel("Speed:"), 2, 0)
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)  # C42
        self.speed_slider.setRange(1, 100)
        self.speed_slider.setValue(50)
        self.speed_slider.valueChanged.connect(self._speed_changed)
        sim_layout.addWidget(self.speed_slider, 2, 1)
        
        sim_group.setLayout(sim_layout)
        controls_layout.addWidget(sim_group)
        
        # Preset Selection (C16-C21, C43)
        preset_group = QGroupBox("Collision Preset")
        preset_layout = QVBoxLayout()
        
        self.preset_combo = QComboBox()
        self.preset_combo.addItems(list(PRESET_MAP.keys()))
        preset_layout.addWidget(self.preset_combo)
        
        self.btn_load_preset = QPushButton("Load Preset")
        self.btn_load_preset.clicked.connect(self._load_preset)
        preset_layout.addWidget(self.btn_load_preset)
        
        # Particle count selector (C43)
        count_layout = QHBoxLayout()
        count_layout.addWidget(QLabel("Particles/Galaxy:"))
        self.particle_spin = QSpinBox()
        self.particle_spin.setRange(500, 50000)
        self.particle_spin.setValue(5000)
        self.particle_spin.setSingleStep(500)
        count_layout.addWidget(self.particle_spin)
        preset_layout.addLayout(count_layout)
        
        preset_group.setLayout(preset_layout)
        controls_layout.addWidget(preset_group)
        
        # Galaxy Parameters (C44, C3, C11)
        params_group = QGroupBox("Parameters")
        params_layout = QGridLayout()
        
        params_layout.addWidget(QLabel("Softening:"), 0, 0)
        self.softening_spin = QSpinBox()
        self.softening_spin.setRange(1, 200)
        self.softening_spin.setValue(50)
        self.softening_spin.setSuffix(" ×0.001")
        self.softening_spin.valueChanged.connect(self._params_changed)
        params_layout.addWidget(self.softening_spin, 0, 1)
        
        params_layout.addWidget(QLabel("Theta:"), 1, 0)
        self.theta_spin = QSpinBox()
        self.theta_spin.setRange(30, 150)
        self.theta_spin.setValue(80)
        self.theta_spin.setSuffix(" ×0.01")
        self.theta_spin.valueChanged.connect(self._params_changed)
        params_layout.addWidget(self.theta_spin, 1, 1)
        
        self.gpu_check = QPushButton("GPU: OFF")
        self.gpu_check.setCheckable(True)
        self.gpu_check.clicked.connect(self._toggle_gpu)
        params_layout.addWidget(self.gpu_check, 2, 0, 1, 2)
        
        params_group.setLayout(params_layout)
        controls_layout.addWidget(params_group)
        
        # Visualization Modes (C31-C34)
        viz_group = QGroupBox("Visualization")
        viz_layout = QVBoxLayout()
        
        self.viz_combo = QComboBox()
        self.viz_combo.addItems(['Particles', 'Density Field', 'Velocity Field', 'Potential Field'])
        self.viz_combo.currentTextChanged.connect(self._viz_mode_changed)
        viz_layout.addWidget(self.viz_combo)
        
        # Effects toggles (C26, C27, C29)
        self.chk_trails = QCheckBox("Particle Trails (C26)")
        self.chk_trails.toggled.connect(self._toggle_trails)
        viz_layout.addWidget(self.chk_trails)
        
        self.chk_bloom = QCheckBox("Bloom Effect (C27)")
        self.chk_bloom.toggled.connect(self._toggle_bloom)
        viz_layout.addWidget(self.chk_bloom)
        
        self.chk_heatmap = QCheckBox("Density Heatmap (C29)")
        viz_layout.addWidget(self.chk_heatmap)
        
        # Color mode (C28)
        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("Color:"))
        self.color_combo = QComboBox()
        self.color_combo.addItems(['Mass', 'Velocity', 'Galaxy'])
        self.color_combo.currentTextChanged.connect(self._color_mode_changed)
        color_layout.addWidget(self.color_combo)
        viz_layout.addLayout(color_layout)
        
        viz_group.setLayout(viz_layout)
        controls_layout.addWidget(viz_group)
        
        # Export (C40, C41, C45-C47)
        export_group = QGroupBox("Export")
        export_layout = QVBoxLayout()
        
        self.btn_screenshot = QPushButton("Save Screenshot (C40)")
        self.btn_screenshot.clicked.connect(self._save_screenshot)
        export_layout.addWidget(self.btn_screenshot)
        
        self.btn_record = QPushButton("Record (C41)")
        self.btn_record.setCheckable(True)
        self.btn_record.clicked.connect(self._toggle_recording)
        export_layout.addWidget(self.btn_record)
        
        self.btn_export_gif = QPushButton("Export GIF (C46)")
        self.btn_export_gif.clicked.connect(self._export_gif)
        export_layout.addWidget(self.btn_export_gif)
        
        self.btn_export_mp4 = QPushButton("Export MP4 (C47)")
        self.btn_export_mp4.clicked.connect(self._export_mp4)
        export_layout.addWidget(self.btn_export_mp4)
        
        self.btn_save = QPushButton("Save State (C68)")
        self.btn_save.clicked.connect(self._save_state)
        export_layout.addWidget(self.btn_save)
        
        self.btn_load = QPushButton("Load State (C69)")
        self.btn_load.clicked.connect(self._load_state)
        export_layout.addWidget(self.btn_load)
        
        export_group.setLayout(export_layout)
        controls_layout.addWidget(export_group)
        
        controls_layout.addStretch()
        controls_scroll.setWidget(controls_widget)
        
        # --- Center: 3D Viewport ---
        self.renderer = GalaxyRenderer()
        self.trail_effect = TrailEffect(self.renderer.view)
        self.density_map = DensityHeatmap()
        
        # Recording state (C41, C45-C47)
        self.recording = False
        self.recorded_frames: list[np.ndarray] = []
        
        # Frame interpolation state (C60)
        self._prev_positions = None
        self._interp_alpha = 0.0
        
        # --- Right: Analysis Panel (C49-C56) ---
        analysis_scroll = QScrollArea()
        analysis_scroll.setWidgetResizable(True)
        analysis_scroll.setFixedWidth(250)
        analysis_widget = QWidget()
        analysis_layout = QVBoxLayout(analysis_widget)
        
        analysis_group = QGroupBox("Analysis")
        analysis_grid = QGridLayout()
        
        self.labels = {}
        metrics = [
            ('fps', 'Render FPS:', '—'),      # C55
            ('phys_fps', 'Physics FPS:', '—'),  # C56
            ('particles', 'Particles:', '—'),
            ('ke', 'Kinetic E:', '—'),          # C51
            ('pe', 'Potential E:', '—'),        # C50
            ('te', 'Total E:', '—'),            # C49
            ('momentum', 'Momentum:', '—'),     # C52
            ('ang_mom', 'Angular L:', '—'),     # C53
            ('com', 'Center of Mass:', '—'),    # C54
            ('timestep', 'Timestep:', '—'),
            ('sim_time', 'Sim Time:', '—'),
        ]
        
        for i, (key, label_text, default) in enumerate(metrics):
            lbl = QLabel(label_text)
            lbl.setFont(QFont("Consolas", 9))
            val = QLabel(default)
            val.setFont(QFont("Consolas", 9, QFont.Weight.Bold))
            val.setStyleSheet("color: #58a6ff;")
            analysis_grid.addWidget(lbl, i, 0)
            analysis_grid.addWidget(val, i, 1)
            self.labels[key] = val
        
        analysis_group.setLayout(analysis_grid)
        analysis_layout.addWidget(analysis_group)
        
        # Live Plots (C35, C36)
        try:
            import pyqtgraph as pg
            pg.setConfigOptions(background='#161b22', foreground='#c9d1d9')
            
            # Energy Plot (C35)
            self.energy_plot = pg.PlotWidget(title="Energy (C35)")
            self.energy_plot.setMaximumHeight(150)
            self.energy_plot.addLegend(offset=(1, 1))
            self.energy_curve_ke = self.energy_plot.plot(pen='r', name='KE')
            self.energy_curve_pe = self.energy_plot.plot(pen='b', name='PE')
            self.energy_curve_te = self.energy_plot.plot(pen='g', name='Total')
            analysis_layout.addWidget(self.energy_plot)
            
            # Angular Momentum Plot (C36)
            self.angmom_plot = pg.PlotWidget(title="Angular Momentum (C36)")
            self.angmom_plot.setMaximumHeight(150)
            self.angmom_curve = self.angmom_plot.plot(pen='y', name='|L|')
            analysis_layout.addWidget(self.angmom_plot)
            
            self.energy_history = {'ke': [], 'pe': [], 'te': [], 'angmom': [], 't': []}
            self._has_plots = True
        except ImportError:
            self._has_plots = False
        
        analysis_layout.addStretch()
        analysis_scroll.setWidget(analysis_widget)
        
        # --- Assemble Layout ---
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(controls_scroll)
        splitter.addWidget(self.renderer.get_widget())
        splitter.addWidget(analysis_scroll)
        splitter.setSizes([300, 600, 250])
        
        main_layout.addWidget(splitter)
    
    # === Callbacks ===
    
    def _toggle_play(self):  # C37
        self.is_playing = not self.is_playing
        self.physics_thread.running = self.is_playing
        self.btn_play.setText("Pause" if self.is_playing else "Play")
    
    def _step_once(self):  # C38
        self.physics_thread.step_requested = True
    
    def _reset_simulation(self):  # C39
        self.is_playing = False
        self.physics_thread.running = False
        self.btn_play.setText("Play")
        self.trail_effect.clear()
        self._load_preset()
    
    def _speed_changed(self, value):  # C42
        self.time_scale = value / 50.0
        self.integrator.base_dt = 0.005 * self.time_scale
    
    def _load_preset(self):
        name = self.preset_combo.currentText()
        n = self.particle_spin.value()
        self.is_playing = False
        self.physics_thread.running = False
        self.btn_play.setText("Play")
        
        preset_fn = PRESET_MAP[name]
        self.particles = preset_fn(n)
        self.physics_thread.particles = self.particles
        self.integrator._accelerations = None
        self.sim_time = 0.0
        self._prev_positions = self.particles.positions.copy()
        self._update_renderer()
    
    def _params_changed(self):  # C3, C11
        self.integrator.softening = self.softening_spin.value() * 0.001
        self.integrator.theta = self.theta_spin.value() * 0.01
    
    def _toggle_gpu(self):  # C59
        gpu_on = self.gpu_check.isChecked()
        self.integrator.use_gpu = gpu_on
        self.gpu_check.setText(f"GPU: {'ON' if gpu_on else 'OFF'}")
    
    def _toggle_trails(self, checked):  # C26
        self.trail_effect.enabled = checked
        if not checked:
            self.trail_effect.clear()
    
    def _toggle_bloom(self, checked):  # C27
        if checked:
            self.renderer.scatter.set_gl_state('additive', depth_test=False)
        else:
            self.renderer.scatter.set_gl_state('translucent', depth_test=False)
    
    def _viz_mode_changed(self, mode):  # C31-C34
        self._update_renderer()
    
    def _color_mode_changed(self, mode):  # C28
        if mode == 'Velocity':
            v_mag = np.sqrt(np.sum(self.particles.velocities**2, axis=1))
            v_norm = v_mag / (v_mag.max() + 1e-10)
            self.particles.colors[:, 0] = v_norm
            self.particles.colors[:, 1] = 0.3
            self.particles.colors[:, 2] = 1.0 - v_norm
        elif mode == 'Galaxy':
            n = self.particles.n
            half = n // 2
            self.particles.colors[:half] = [0.4, 0.6, 1.0, 1.0]
            self.particles.colors[half:] = [1.0, 0.5, 0.3, 1.0]
        self._update_renderer()
    
    def _toggle_recording(self):  # C41
        self.recording = self.btn_record.isChecked()
        if self.recording:
            self.recorded_frames.clear()
            self.btn_record.setText("Stop Recording")
        else:
            self.btn_record.setText("Record (C41)")
    
    def _export_png_sequence(self):  # C45
        if not self.recorded_frames:
            return
        dirpath = QFileDialog.getExistingDirectory(self, "Select PNG output directory")
        if dirpath:
            from PIL import Image
            for i, frame in enumerate(self.recorded_frames):
                img = Image.fromarray(frame)
                img.save(os.path.join(dirpath, f"frame_{i:04d}.png"))
    
    def _export_gif(self):  # C46
        if not self.recorded_frames:
            return
        filepath, _ = QFileDialog.getSaveFileName(self, "Export GIF", "simulation.gif", "GIF (*.gif)")
        if filepath:
            import imageio
            imageio.mimsave(filepath, self.recorded_frames, fps=30, loop=0)
    
    def _export_mp4(self):  # C47
        if not self.recorded_frames:
            return
        filepath, _ = QFileDialog.getSaveFileName(self, "Export MP4", "simulation.mp4", "MP4 (*.mp4)")
        if filepath:
            import imageio
            writer = imageio.get_writer(filepath, fps=30)
            for frame in self.recorded_frames:
                writer.append_data(frame)
            writer.close()
    
    def _save_screenshot(self):  # C40
        filepath, _ = QFileDialog.getSaveFileName(self, "Save Screenshot", "screenshot.png", "PNG (*.png)")
        if filepath:
            self.renderer.save_screenshot(filepath)
    
    def _save_state(self):  # C68
        filepath, _ = QFileDialog.getSaveFileName(self, "Save State", "simulation.json", "JSON (*.json)")
        if filepath:
            save_state(self.particles, filepath, {'sim_time': self.sim_time})
    
    def _load_state(self):  # C69
        filepath, _ = QFileDialog.getOpenFileName(self, "Load State", "", "JSON (*.json)")
        if filepath:
            self.particles, meta = load_state(filepath)
            self.physics_thread.particles = self.particles
            self.integrator._accelerations = None
            self.sim_time = meta.get('sim_time', 0.0)
            self._update_renderer()
    
    # === Rendering ===
    
    def _on_physics_step(self):
        self.sim_time += self.integrator.dt
        # Store previous positions for frame interpolation (C60)
        self._prev_positions = self.particles.positions.copy()
    
    def _render_frame(self):
        self._update_renderer()
        self._update_analysis()
        self.frame_count += 1
        
        # Recording (C41, C45)
        if self.recording:
            frame = self.renderer.canvas.render()
            if frame is not None:
                self.recorded_frames.append(frame)
    
    def _update_renderer(self):
        zoom = self.renderer.view.camera.distance if hasattr(self.renderer.view.camera, 'distance') else 1.0
        
        # Frame interpolation (C60): blend between physics steps for smooth playback
        if self._prev_positions is not None and self.is_playing:
            alpha = min(1.0, self._interp_alpha)
            display_pos = self._prev_positions + alpha * (self.particles.positions - self._prev_positions)
            self._interp_alpha += 0.1
        else:
            display_pos = self.particles.positions
        
        # Trail update (C26)
        if self.trail_effect.enabled:
            self.trail_effect.update(display_pos)
            if self.frame_count % 5 == 0:
                self.trail_effect.render()
        
        self.renderer.update_particles(
            display_pos,
            self.particles.colors,
            self.particles.radii,
            zoom=zoom
        )
        self.renderer.canvas.update()
    
    def _update_analysis(self):  # C49-C56
        fps = self.renderer.get_fps()
        self.labels['fps'].setText(f"{fps:.1f}")
        self.labels['phys_fps'].setText(f"{self.integrator.physics_fps:.1f}")
        self.labels['particles'].setText(f"{self.particles.n:,}")
        
        # Compute analysis values (throttle to every 10 frames)
        if self.frame_count % 10 == 0:
            ke = self.particles.kinetic_energy()
            pe = self.particles.potential_energy(self.integrator.softening)
            mom = self.particles.momentum()
            ang = self.particles.angular_momentum()
            com = self.particles.center_of_mass()
            
            self.labels['ke'].setText(f"{ke:.2e}")
            self.labels['pe'].setText(f"{pe:.2e}")
            self.labels['te'].setText(f"{ke + pe:.2e}")
            self.labels['momentum'].setText(f"{np.linalg.norm(mom):.2e}")
            self.labels['ang_mom'].setText(f"{np.linalg.norm(ang):.2e}")
            self.labels['com'].setText(f"({com[0]:.2f}, {com[1]:.2f})")
            
            # Update live plots (C35, C36)
            if self._has_plots:
                self.energy_history['t'].append(self.sim_time)
                self.energy_history['ke'].append(ke)
                self.energy_history['pe'].append(pe)
                self.energy_history['te'].append(ke + pe)
                self.energy_history['angmom'].append(np.linalg.norm(ang))
                
                # Keep last 200 data points
                max_pts = 200
                for k in self.energy_history:
                    if len(self.energy_history[k]) > max_pts:
                        self.energy_history[k] = self.energy_history[k][-max_pts:]
                
                t = self.energy_history['t']
                self.energy_curve_ke.setData(t, self.energy_history['ke'])
                self.energy_curve_pe.setData(t, self.energy_history['pe'])
                self.energy_curve_te.setData(t, self.energy_history['te'])
                self.angmom_curve.setData(t, self.energy_history['angmom'])
        
        self.labels['timestep'].setText(f"{self.integrator.dt:.4f}")
        self.labels['sim_time'].setText(f"{self.sim_time:.3f}")
    
    def _stylesheet(self) -> str:
        return """
            QMainWindow { background: #0d1117; }
            QGroupBox { 
                font-weight: bold; color: #c9d1d9; 
                border: 1px solid #30363d; border-radius: 6px;
                margin-top: 8px; padding-top: 12px;
            }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; }
            QPushButton {
                background: #21262d; color: #c9d1d9; border: 1px solid #30363d;
                border-radius: 4px; padding: 6px 12px;
            }
            QPushButton:hover { background: #30363d; }
            QPushButton:checked { background: #238636; border-color: #2ea043; }
            QLabel { color: #8b949e; }
            QComboBox, QSpinBox {
                background: #21262d; color: #c9d1d9; border: 1px solid #30363d;
                border-radius: 4px; padding: 4px;
            }
            QSlider::groove:horizontal { background: #30363d; height: 4px; border-radius: 2px; }
            QSlider::handle:horizontal { background: #58a6ff; width: 14px; margin: -5px 0; border-radius: 7px; }
            QScrollArea { border: none; background: #161b22; }
        """
    
    def closeEvent(self, event):
        self.physics_thread.running = False
        self.physics_thread.terminate()
        self.physics_thread.wait(1000)
        event.accept()
