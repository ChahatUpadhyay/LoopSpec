# Implementation Plan

## Iteration: 2
## Status: APPROVED

## Summary

Iteration 2 focuses on adding GPU-accelerated rendering with vispy/OpenGL, camera controls, basic UI controls with PyQt6, analysis panel for real-time metrics, and collision presets. This builds on the physics engine foundation from Iteration 1.

## Learnings Applied

- Use absolute imports (not relative) to avoid import errors
- Install package in editable mode: `pip install -e .`
- Python-based implementation (pivoted from JavaScript due to Node.js unavailability)

## Changes Required

### Iteration 2 Scope (Rendering and UI)
- vispy/OpenGL GPU-accelerated renderer
- Camera controls (zoom, pan, orbit)
- PyQt6 main window with control panel
- Pause/play, step, reset controls
- Snapshot save functionality
- Speed slider and particle count selector
- Analysis panel (energy, momentum, angular momentum, FPS)
- Head-on and fly-by collision presets
- Performance test with 10K particles

### Future Iterations (Out of Scope for Iteration 2)
- Advanced visualization modes (density, velocity, potential fields)
- All collision presets (retrograde, prograde, elliptical, random)
- Recording/export features (GIF, MP4)
- Performance optimizations (multithreading, GPU compute shaders)
- Full documentation suite (architecture diagram, performance analysis)

## Traceability Matrix

| Criterion | Planned Changes | Test Strategy |
|-----------|----------------|---------------|
| C7 | Performance test with 10K particles | Automated FPS measurement |
| C16 | Add head-on collision preset | Manual verification |
| C17 | Add fly-by collision preset | Manual verification |
| C22 | Implement real-time rendering loop with FPS counter | Automated FPS measurement |
| C23 | Implement mouse wheel zoom | Manual verification |
| C24 | Implement click-drag pan | Manual verification |
| C25 | Implement right-click-drag orbit | Manual verification |
| C37 | Add pause/play button | Manual verification |
| C38 | Add step button | Manual verification |
| C39 | Add reset button | Manual verification |
| C40 | Add snapshot save button | Manual verification |
| C42 | Add speed slider for time scale | Manual verification |
| C43 | Add particle count selector | Manual verification |
| C44 | Add galaxy parameters panel | Manual verification |
| C49 | Implement total energy computation | Manual verification - displays in panel |
| C50 | Implement potential energy computation | Manual verification - displays in panel |
| C51 | Implement kinetic energy computation | Manual verification - displays in panel |
| C52 | Implement momentum computation | Manual verification - displays in panel |
| C53 | Implement angular momentum computation | Manual verification - displays in panel |
| C54 | Implement center of mass computation | Manual verification - displays in panel |
| C55 | Display simulation FPS | Manual verification - shows in panel |
| C56 | Display physics FPS | Manual verification - shows in panel |

## Order of Operations

### Phase 1: Renderer Setup
1. Create `src/renderer/__init__.py`
2. Create `src/renderer/opengl_renderer.py` with vispy canvas
3. Implement particle rendering with GPU instancing
4. Add FPS counter to renderer

### Phase 2: Camera Controls
5. Implement mouse wheel zoom (C23)
6. Implement click-drag pan (C24)
7. Implement right-click-drag orbit (C25)

### Phase 3: PyQt6 UI Framework
8. Create `src/ui/__init__.py`
9. Create `src/ui/main_window.py` with PyQt6 main window
10. Integrate vispy canvas into PyQt6 window

### Phase 4: Control Panel
11. Create `src/ui/control_panel.py`
12. Add pause/play button (C37)
13. Add step button (C38)
14. Add reset button (C39)
15. Add snapshot button (C40)
16. Add speed slider (C42)
17. Add particle count selector (C43)
18. Add galaxy parameters panel (C44)

### Phase 5: Analysis Panel
19. Create `src/ui/analysis_panel.py`
20. Implement energy computations (C49, C50, C51)
21. Implement momentum (C52)
22. Implement angular momentum (C53)
23. Implement center of mass (C54)
24. Display simulation FPS (C55)
25. Display physics FPS (C56)

### Phase 6: Collision Presets
26. Create `src/galaxy/collision_presets.py`
27. Add head-on collision preset (C16)
28. Add fly-by collision preset (C17)

### Phase 7: Integration and Testing
29. Integrate physics engine with renderer
30. Create simulation loop
31. Performance test with 10K particles (C7)
32. Manual verification of all UI controls

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| vispy/OpenGL compatibility issues | High | Test on Windows first, verify OpenGL version |
| PyQt6 integration complexity | Medium | Start with simple window, add controls incrementally |
| Performance with 10K particles in UI | High | Use separate thread for physics, optimize rendering |
| Camera control implementation complexity | Medium | Use vispy's built-in camera controls if available |
| UI blocking physics simulation | Medium | Use QTimer for non-blocking updates |

## Scope Boundary

### In Scope (Iteration 2)
- vispy/OpenGL GPU-accelerated renderer
- Camera controls (zoom, pan, orbit)
- PyQt6 main window with basic controls
- Analysis panel with real-time metrics
- Head-on and fly-by collision presets
- Performance test with 10K particles

### Out of Scope (Future Iterations)
- Advanced visualization modes (C31-C36)
- All collision presets (C18-C21)
- Recording/export (C45-C48)
- Performance optimizations (C58-C61)
- Full documentation suite (C70-C72)

### Success Criteria for Iteration 2
- Renderer displays particles at 30+ FPS with 10K particles (C7, C22)
- Camera controls work smoothly (C23-C25)
- Basic UI controls functional (C37-C40, C42-C44)
- Analysis panel displays real-time metrics (C49-C56)
- Collision presets work (C16-C17)

---

> **HUMAN APPROVAL**: [x] APPROVED
>
> **Human Notes**: User requested to continue and execute next iterations
>
