# Implementation Plan

## Iteration: 1 — Core Physics + Rendering + GUI Foundation
## Status: APPROVED

## Summary

Build the complete application foundation: physics engine (gravity, Barnes-Hut, integrator), galaxy generator with presets, GPU rendering via Vispy, PyQt6 GUI with all controls, analysis panel, and automated tests. This iteration targets C1-C5, C7, C9-C14, C16-C22, C23-C25, C28, C31, C37-C44, C49-C57, C62-C67, C68-C74.

## Learnings Applied

- From previous galaxy-collision-sim: CuPy nvrtc DLL issues on this system — use CuPy only for array operations (not custom kernels) or fallback to CPU Barnes-Hut
- From previous: Vispy SceneCanvas works well with PyQt6 for GPU rendering
- From previous: Fixed timestep more stable than adaptive for initial implementation; add adaptive later
- From previous: Barnes-Hut theta=0.8 gives good balance of speed vs accuracy

## Changes Required

### Iteration 1 (Foundation — ~40 criteria)
1. Project structure: `src/`, `tests/`, `main.py`, `requirements.txt`
2. Physics engine: particles, gravity (direct + Barnes-Hut), leapfrog integrator
3. Galaxy generator: spiral galaxies, presets (Milky Way, Andromeda, random)
4. Collision presets: head-on, fly-by, retrograde, prograde, elliptical, random
5. GPU rendering: Vispy SceneCanvas with point sprites, camera controls
6. UI: PyQt6 main window with controls panel, analysis panel
7. Tests: physics validation tests
8. Serialization: save/load JSON
9. Documentation: README with architecture, physics, user guide

### Iteration 2 (Advanced Features — ~20 criteria)
- Visualization modes (density, velocity, potential fields)
- Effects (bloom, trails, heatmap, dynamic sizing)
- Export (PNG, GIF, MP4)
- GPU compute (CuPy acceleration)
- Performance optimization (multithreading, frame interpolation)
- Adaptive timestep

### Iteration 3 (Polish + 50K particles)
- 50K particle support optimization
- Final performance tuning
- Any remaining criteria

## Traceability Matrix

| Criterion | Planned Changes | Test Strategy |
|-----------|----------------|---------------|
| C1 | `gravity.py` — direct N-body force calculation | `test_physics.py` unit test |
| C2 | `octree.py` — Barnes-Hut tree, `gravity.py` — tree walk | Performance scaling test |
| C3 | Softening param in physics + UI slider | Manual: verify no singularities |
| C4 | `integrator.py` — leapfrog kick-drift-kick | Energy conservation test |
| C5 | Adaptive dt in integrator | Manual: no ejection artifacts |
| C7 | Full pipeline optimized for 10K @ 30FPS | FPS counter verification |
| C9 | `particles.py` — structured NumPy array | Data structure test |
| C10-C14 | `generator.py` — spiral generation, presets | Manual: visible arms |
| C15 | `serialization.py` — save/load galaxy params | Automated: round-trip test |
| C16-C21 | `presets.py` — 6 collision configurations | Manual: correct trajectories |
| C22 | Vispy renderer + FPS counter | Automated: FPS > 30 |
| C23-C25 | Vispy camera (turntable) | Manual: zoom/pan/orbit |
| C28 | Color mapping in renderer | Manual: mass-based coloring |
| C31 | Default particle view mode | Manual: points visible |
| C37-C44 | PyQt6 control panel | Manual: all buttons work |
| C49-C56 | Analysis computation + display | Manual: values update |
| C57 | Barnes-Hut octree = spatial partitioning | Code review |
| C62-C67 | `test_physics.py` — full test suite | pytest passes |
| C68-C69 | `serialization.py` save/load state | Automated test |
| C70-C74 | `README.md` with all documentation | Manual review |

## Order of Operations

1. Create project structure + requirements.txt
2. Implement `src/physics/particles.py` (C9)
3. Implement `src/physics/gravity.py` — direct + Barnes-Hut (C1, C2, C57)
4. Implement `src/physics/octree.py` (C2, C57)
5. Implement `src/physics/integrator.py` — leapfrog + adaptive (C4, C5)
6. Implement `src/galaxy/generator.py` + presets (C10-C14)
7. Implement `src/galaxy/presets.py` — collision configs (C16-C21)
8. Implement `src/galaxy/serialization.py` (C15, C68-C69)
9. Implement `src/rendering/renderer.py` — Vispy GPU rendering (C22, C23-C25, C28, C31)
10. Implement `src/ui/main_window.py` + controls + analysis (C37-C44, C49-C56)
11. Implement `main.py` entry point
12. Write `tests/test_physics.py` (C62-C67)
13. Write `README.md` (C70-C74)
14. Performance test: verify 10K @ 30FPS (C7, C22)

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| CuPy CUDA kernel compilation fails | High | Fallback to CPU Barnes-Hut (proven to work at 5K+) |
| Vispy canvas crash on init | Medium | Test canvas creation first, use pyqt6 backend |
| 10K particles too slow | High | Barnes-Hut theta=0.8 + skip frames + reduce physics rate |
| PyQt6 + Vispy threading issues | Medium | Physics on QThread, render on main thread |

## Scope Boundary

**In scope (Iteration 1)**: C1-C5, C7, C9-C22, C23-C25, C28, C31, C37-C44, C49-C57, C62-C74
**Out of scope (Iteration 2+)**: C6, C8, C26-C27, C29-C30, C32-C36, C45-C48, C58-C61

---

> **HUMAN APPROVAL**: [x] APPROVED
>
> **Human Notes**: User approved: "I won't interrupt the testing in between"
>
