# Project Context

## Tech Stack

- **Language**: Python 3.11.9
- **GUI Framework**: PyQt6 6.11.0
- **GPU Rendering**: Vispy 0.16.2 (OpenGL via Qt backend)
- **GPU Compute**: CuPy 13.6.0 (CUDA for physics)
- **Math**: NumPy 1.26.4
- **Imaging**: Pillow 10.4.0
- **Hardware**: Ryzen 7 5800H (8C/16T), RTX 3050 4GB VRAM, CUDA driver 592.27

## Project Structure

```
galaxy-collision-v3-test/
├── .loopspec/              # Protocol files
├── src/
│   ├── __init__.py
│   ├── physics/
│   │   ├── __init__.py
│   │   ├── gravity.py         # Direct N-body + Barnes-Hut
│   │   ├── gravity_gpu.py     # CuPy GPU gravity
│   │   ├── integrator.py      # Leapfrog integrator
│   │   ├── octree.py          # Barnes-Hut octree
│   │   └── particles.py       # Particle data structure
│   ├── galaxy/
│   │   ├── __init__.py
│   │   ├── generator.py       # Galaxy generation
│   │   ├── presets.py         # Collision presets
│   │   └── serialization.py   # Save/load state
│   ├── rendering/
│   │   ├── __init__.py
│   │   ├── renderer.py        # Vispy OpenGL renderer
│   │   └── effects.py         # Bloom, trails, heatmap
│   └── ui/
│       ├── __init__.py
│       ├── main_window.py     # PyQt6 main window
│       ├── controls.py        # UI controls panel
│       └── analysis.py        # Analysis panel
├── tests/
│   ├── test_physics.py        # C62-C67 automated tests
│   └── test_serialization.py  # C68-C69 tests
├── main.py                    # Entry point
├── requirements.txt
└── README.md
```

## Architecture Overview

- **Physics Layer**: NumPy arrays for particle state, Barnes-Hut octree for O(N log N), CuPy for GPU-accelerated gravity when N > 5000
- **Rendering Layer**: Vispy SceneCanvas with OpenGL point sprites, bloom via fragment shader
- **UI Layer**: PyQt6 widgets wrapping Vispy canvas, control panels, analysis plots
- **Threading**: Physics on separate QThread, rendering on main thread with frame interpolation

## Key Files & Their Roles

- `main.py` — Application entry point
- `src/physics/gravity.py` — Core gravity computation (CPU Barnes-Hut)
- `src/physics/gravity_gpu.py` — CuPy CUDA gravity kernel
- `src/physics/integrator.py` — Leapfrog with adaptive timestep
- `src/rendering/renderer.py` — Vispy OpenGL renderer with effects
- `src/ui/main_window.py` — PyQt6 main window orchestrating everything

## Dependencies

- PyQt6 6.11.0 ✓ (installed)
- vispy 0.16.2 ✓ (installed)
- numpy 1.26.4 ✓ (installed)
- cupy 13.6.0 ✓ (installed, RTX 3050 detected)
- Pillow 10.4.0 ✓ (installed)
- imageio (needed for GIF/MP4 export — to install)
- pyqtgraph (needed for live plots — to install)

## Existing Tests

None — greenfield project.

## Baseline State

Empty project directory with only `.loopspec/` and `AGENTS.md`.

## Available Runtimes

- Python 3.11.9 ✓
- NVIDIA CUDA (CuPy 13.6.0, driver 592.27, RTX 3050 4GB) ✓
- PyQt6 + Vispy (OpenGL) ✓
- Git (Loop_Spec_v3 branch) ✓
- PowerShell 5.1 ✓

## Patterns & Conventions

- Absolute imports: `from src.physics.gravity import compute_forces`
- NumPy arrays as primary data structure for particle state
- CuPy arrays for GPU operations (transparent NumPy API)
- QThread for physics computation, QTimer for render loop
- Type hints on all public functions
- Docstrings on all modules and classes

