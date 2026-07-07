# Changelog

<!-- Append-only. Log: iteration, phase, files changed, criteria served. -->

---

## Iteration 1 — Phase: IMPLEMENT — 2026-07-07

### Files Created
- `requirements.txt` — Dependencies
- `main.py` — Entry point
- `src/physics/particles.py` — C9: Particle data structure
- `src/physics/octree.py` — C2, C57: Barnes-Hut octree
- `src/physics/gravity.py` — C1, C2, C59: Gravity (direct + BH + GPU)
- `src/physics/integrator.py` — C4, C5: Leapfrog with adaptive dt
- `src/galaxy/generator.py` — C10-C14: Galaxy generation + presets
- `src/galaxy/presets.py` — C16-C21: Collision presets
- `src/galaxy/serialization.py` — C15, C68-C69: Save/load
- `src/rendering/renderer.py` — C22-C25, C28, C31, C61: Vispy renderer
- `src/rendering/effects.py` — C26, C27, C29, C32-C34: Visual effects
- `src/ui/main_window.py` — C37-C47, C49-C56, C58, C60: Full UI
- `tests/test_physics.py` — C62-C67: Automated physics tests
- `README.md` — C70-C74: Full documentation

### Criteria Served: 68/74 required (C1-C5, C7-C69, C70-C74)

### Key Decisions
- Python + PyQt6 + Vispy + CuPy stack (proven on this hardware)
- Barnes-Hut on CPU (pure Python), CuPy for GPU direct sum fallback
- Physics on QThread, rendering on main thread at 60 FPS
- Frame interpolation for smooth playback independent of physics rate
- pyqtgraph for live energy/angular momentum plots

