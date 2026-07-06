# Project Context

## Tech Stack

- **Target platform**: Desktop application (Python)
- **Primary language**: Python 3.11.9
- **Rendering engine**: vispy (OpenGL) for GPU-accelerated rendering
- **Physics computation**: NumPy for vectorized calculations
- **UI framework**: PyQt6 for desktop GUI
- **Testing**: pytest
- **OS**: Windows 11 (primary dev), must support macOS and Linux

## Project Structure

```
galaxy-collision-sim/
├── .loopspec/          # LoopSpec protocol files
├── src/
│   ├── physics/        # Physics engine (particle, gravity, barnes_hut, integrator)
│   ├── galaxy/         # Galaxy generation (spiral_generator)
│   ├── renderer/       # OpenGL/vispy renderer (to be added in Iteration 2)
│   ├── ui/             # PyQt6 UI components (to be added in Iteration 2)
│   └── serialization.py # Save/load functionality
├── tests/              # Test suite
├── requirements.txt     # Python dependencies
├── pyproject.toml      # Project configuration
└── README.md           # User guide
```

## Architecture Overview

**Completed (Iteration 1):**
- **Physics Engine**: N-body simulation with Barnes-Hut octree acceleration
- **Integrator**: Leapfrog integration with adaptive timestep
- **Galaxy Generator**: Procedural spiral galaxy generation with presets
- **Serialization**: JSON-based save/load system

**Planned (Iteration 2):**
- **Renderer**: vispy OpenGL renderer with GPU acceleration
- **Camera Controls**: Zoom, pan, orbit using mouse input
- **UI Controls**: PyQt6 interface with pause/play, step, reset, snapshot
- **Analysis Panel**: Real-time display of energy, momentum, angular momentum, FPS
- **Collision Presets**: Head-on and fly-by collision configurations

## Key Files & Their Roles

**Completed:**
- `src/physics/particle.py` - Particle class with position, velocity, mass, color, radius
- `src/physics/gravity.py` - Newtonian gravity calculations
- `src/physics/barnes_hut.py` - Barnes-Hut octree for O(N log N) force calculation
- `src/physics/integrator.py` - Leapfrog integrator with adaptive timestep
- `src/galaxy/spiral_generator.py` - Procedural spiral galaxy generator
- `src/serialization.py` - Save/load simulation state

**To be added (Iteration 2):**
- `src/renderer/opengl_renderer.py` - vispy-based GPU renderer
- `src/ui/main_window.py` - PyQt6 main window
- `src/ui/control_panel.py` - UI controls for simulation
- `src/ui/analysis_panel.py` - Real-time analysis display

## Dependencies

**Installed:**
- numpy>=1.24.0
- PyQt6>=6.4.0
- PyOpenGL>=3.1.6
- vispy>=0.9.5
- pytest>=7.4.0

## Existing Tests

**Completed (Iteration 1):**
- 26 tests passing
- Particle structure validation
- Gravity calculation accuracy
- Barnes-Hut octree construction and accuracy
- Leapfrog integrator energy conservation
- Galaxy generation validation
- Serialization correctness

## Baseline State

**Command**: `python -m pytest tests/ -v`
**Output**: 26 passed
**Status**: Physics engine, galaxy generator, and serialization complete and tested

## Available Runtimes

- Python 3.11.9 ✓
- PyQt6 ✓
- vispy ✓
- PyOpenGL ✓
- PowerShell 5.1 ✓
- Git 2.x ✓

## Patterns & Conventions

- Follow LoopSpec v3 protocol strictly
- Evidence-based development
- Test-first approach
- Scientific accuracy over performance when conflicts arise
- Absolute imports (not relative) to avoid import errors
- Install package in editable mode: `pip install -e .`
- Cross-platform compatibility

