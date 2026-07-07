# Goal

## Objective

Build a scientifically plausible, GPU-accelerated visualization of two colliding galaxies with interactive controls. The final result should look comparable to a simplified research visualization rather than a game.

## Success Criteria

### Physics Engine (C1-C6)

| ID | Criterion | Verifier | Threshold | Required |
|----|-----------|----------|-----------|----------|
| C1 | Newtonian gravity implementation with N-body simulation | automated | Unit tests pass for force calculation accuracy | yes |
| C2 | Barnes-Hut Octree acceleration (O(N log N)) implemented | automated | Performance test shows O(N log N) scaling | yes |
| C3 | Softening parameter configurable and applied | manual | UI shows softening parameter, simulation runs without singularities | yes |
| C4 | Leapfrog integrator implemented | automated | Energy conservation test shows <1% drift over 1000 steps | yes |
| C5 | Adaptive timestep based on particle proximity | manual | Simulation adapts timestep, no particle ejection artifacts | yes |
| C6 | Collision handling between particles | optional | Particles merge or bounce on close approach | no |

### Particle Support (C7-C9)

| ID | Criterion | Verifier | Threshold | Required |
|----|-----------|----------|-----------|----------|
| C7 | Support for 10,000 particles at 30+ FPS | automated | Simulation runs at 30+ FPS with 10K particles on RTX 3050 | yes |
| C8 | Support for 50,000+ particles | automated | UI allows selection, simulation runs with acceptable performance | yes |
| C9 | Each particle stores position, velocity, mass, color, radius | automated | Data structure validation test passes | yes |

### Galaxy Generator (C10-C15)

| ID | Criterion | Verifier | Threshold | Required |
|----|-----------|----------|-----------|----------|
| C10 | Procedural spiral galaxy generation | manual | UI generates spiral galaxies with visible arms | yes |
| C11 | Configurable parameters: arms, bulge radius, disk radius, rotation velocity, mass distribution | manual | UI controls exist and affect galaxy generation | yes |
| C12 | Milky Way preset | manual | Preset generates realistic Milky Way-like galaxy | yes |
| C13 | Andromeda preset | manual | Preset generates realistic Andromeda-like galaxy | yes |
| C14 | Random galaxy generation | manual | Random button generates varied galaxies | yes |
| C15 | Galaxy parameters saveable/loadable | automated | Serialization test passes | yes |

### Collision Presets (C16-C21)

| ID | Criterion | Verifier | Threshold | Required |
|----|-----------|----------|-----------|----------|
| C16 | Head-on collision preset | manual | Preset initializes galaxies on collision course | yes |
| C17 | Fly-by collision preset | manual | Preset initializes galaxies for close fly-by | yes |
| C18 | Retrograde collision preset | manual | Preset initializes with retrograde rotation | yes |
| C19 | Prograde collision preset | manual | Preset initializes with prograde rotation | yes |
| C20 | Elliptical merger preset | manual | Preset initializes elliptical orbit merger | yes |
| C21 | Random collision preset | manual | Random collision generates varied scenarios | yes |

### Rendering (C22-C30)

| ID | Criterion | Verifier | Threshold | Required |
|----|-----------|----------|-----------|----------|
| C22 | Real-time GPU rendering at 30+ FPS | automated | FPS counter shows 30+ with 10K particles on RTX 3050 | yes |
| C23 | Zoom camera control | manual | Mouse wheel zooms in/out smoothly | yes |
| C24 | Pan camera control | manual | Click-drag pans the view | yes |
| C25 | Orbit camera control | manual | Right-click-drag orbits around center | yes |
| C26 | Particle trails | manual | Trails toggle shows particle paths | yes |
| C27 | Bloom post-processing effect | manual | Bloom toggle adds glow effect | yes |
| C28 | Particle coloring based on properties | manual | Colors reflect mass/velocity/age | yes |
| C29 | Density heatmap mode | manual | Heatmap toggle shows density visualization | yes |
| C30 | HDR rendering (optional) | optional | HDR toggle enables high dynamic range | no |

### Visualization Modes (C31-C36)

| ID | Criterion | Verifier | Threshold | Required |
|----|-----------|----------|-----------|----------|
| C31 | Particle View mode (stars only) | manual | Mode switch shows individual particles | yes |
| C32 | Density Field mode (kernel density estimate) | manual | Mode switch shows density field visualization | yes |
| C33 | Velocity Field mode (arrow glyphs) | manual | Mode switch shows velocity vectors | yes |
| C34 | Potential Field mode (false-color map) | manual | Mode switch shows gravitational potential | yes |
| C35 | Energy Plot live graph | manual | Graph shows total energy over time | yes |
| C36 | Angular Momentum Plot live graph | manual | Graph shows angular momentum over time | yes |

### UI Controls (C37-C44)

| ID | Criterion | Verifier | Threshold | Required |
|----|-----------|----------|-----------|----------|
| C37 | Pause/Play control | manual | Button pauses/resumes simulation | yes |
| C38 | Step simulation button | manual | Button advances simulation by one step | yes |
| C39 | Reset simulation button | manual | Button resets to initial state | yes |
| C40 | Save snapshot button | manual | Button saves current frame as image | yes |
| C41 | Record animation button | manual | Button records simulation to video | yes |
| C42 | Speed slider (time scale) | manual | Slider adjusts simulation speed | yes |
| C43 | Particle count selector | manual | Dropdown selects particle count | yes |
| C44 | Galaxy parameters panel | manual | Panel shows/edits galaxy parameters | yes |

### Recording Export (C45-C48)

| ID | Criterion | Verifier | Threshold | Required |
|----|-----------|----------|-----------|----------|
| C45 | PNG sequence export | manual | Export saves PNG sequence of frames | yes |
| C46 | GIF export | manual | Export saves animated GIF | yes |
| C47 | MP4 export | manual | Export saves MP4 video | yes |
| C48 | Camera path recording | optional | Camera path can be recorded and replayed | no |

### Analysis Panel (C49-C56)

| ID | Criterion | Verifier | Threshold | Required |
|----|-----------|----------|-----------|----------|
| C49 | Total energy computation and display | manual | Panel shows total energy in real-time | yes |
| C50 | Potential energy computation and display | manual | Panel shows potential energy | yes |
| C51 | Kinetic energy computation and display | manual | Panel shows kinetic energy | yes |
| C52 | Momentum computation and display | manual | Panel shows total momentum | yes |
| C53 | Angular momentum computation and display | manual | Panel shows angular momentum | yes |
| C54 | Center of mass computation and display | manual | Panel shows center of mass position | yes |
| C55 | Simulation FPS display | manual | Panel shows current FPS | yes |
| C56 | Physics FPS display | manual | Panel shows physics computation rate | yes |

### Performance Optimizations (C57-C61)

| ID | Criterion | Verifier | Threshold | Required |
|----|-----------|----------|-----------|----------|
| C57 | Spatial partitioning implemented | automated | Code review confirms spatial data structure | yes |
| C58 | Multithreading for physics computation | automated | Performance test shows speedup on multi-core (Ryzen 7 5800H 8-core) | yes |
| C59 | GPU compute for physics (RTX 3050 CUDA) | metric | GPU acceleration shows measurable speedup | yes |
| C60 | Frame interpolation for smooth playback | manual | Playback is smooth even at lower physics FPS | yes |
| C61 | Dynamic particle sizing based on zoom | manual | Particles scale appropriately with zoom | yes |

### Testing (C62-C67)

| ID | Criterion | Verifier | Threshold | Required |
|----|-----------|----------|-----------|----------|
| C62 | Automated test for integrator correctness | automated | Test suite includes integrator validation | yes |
| C63 | Automated test for energy conservation | automated | Test suite includes energy conservation check | yes |
| C64 | Automated test for momentum conservation | automated | Test suite includes momentum conservation check | yes |
| C65 | Automated test for Barnes-Hut accuracy | automated | Test suite compares Barnes-Hut to direct summation | yes |
| C66 | Automated test for tree construction | automated | Test suite validates octree structure | yes |
| C67 | Automated test for galaxy initialization | automated | Test suite validates galaxy parameters | yes |

### Serialization (C68-C69)

| ID | Criterion | Verifier | Threshold | Required |
|----|-----------|----------|-----------|----------|
| C68 | Save simulation state to JSON | automated | Save function writes valid JSON | yes |
| C69 | Load simulation state from JSON | automated | Load function restores state correctly | yes |

### Documentation (C70-C74)

| ID | Criterion | Verifier | Threshold | Required |
|----|-----------|----------|-----------|----------|
| C70 | Architecture diagram | manual | README includes architecture diagram | yes |
| C71 | Physics explanation documentation | manual | README explains physics implementation | yes |
| C72 | Performance analysis documentation | manual | README includes performance benchmarks | yes |
| C73 | API documentation | manual | Code has API documentation comments | yes |
| C74 | User guide | manual | README includes user guide | yes |

## Permissions

- [x] Read all project files
- [x] Create new files
- [x] Modify existing files
- [x] Delete files
- [x] Execute shell commands
- [x] Run tests
- [x] Git operations
- [x] Install dependencies
- [ ] Network / external APIs
- [ ] Deploy
- [ ] Secrets/credentials
- [ ] Irreversible operations

## Constraints

- **Hardware**: AMD Ryzen 7 5800H (8-core/16-thread), NVIDIA RTX 3050 (4GB VRAM, CUDA)
- Must be scientifically plausible (not game physics)
- GPU-accelerated rendering required (RTX 3050 via CUDA/OpenGL)
- Interactive controls must be responsive
- Python desktop application (PyQt6 + Vispy/ModernGL for GPU rendering)
- No external API keys required
- Must run on Windows 11

## Priority

scientific_accuracy > performance > features > usability > elegance

## Max Iterations

max_iterations: 10

## Additional Context

- **Hardware Target**: Ryzen 7 5800H + RTX 3050 GPU (4GB VRAM)
- This is an independent protocol test — same criteria as original galaxy-collision-sim
- Python + PyQt6 for GUI, Vispy or ModernGL for GPU rendering
- CuPy or Numba CUDA for GPU-accelerated physics
- Barnes-Hut algorithm is required for performance with large N
- GPU acceleration is essential for real-time rendering at 10K+ particles
- Target: 30+ FPS for 10K particles, playable for 50K particles
- Use all 8 cores of Ryzen 7 for parallel physics when not on GPU

