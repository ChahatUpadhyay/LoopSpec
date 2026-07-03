# Implementation Plan

<!--
  MODEL: Fill this during Phase 2 (PLAN).
  HUMAN: Review and mark as APPROVED before the model proceeds.

  RULES:
  - Every change must reference at least one criterion ID (C1, C2, ...)
  - If iteration > 1, the approach MUST be materially different from the last attempt
  - All prevention rules from LEARNINGS.md must be addressed
  - The model will NOT begin implementation until approval is given
-->

## Iteration: 1
## Status: PENDING_APPROVAL

## Summary

Create a single HTML file (index.html) containing a complete 3D black hole simulation using Three.js with custom GLSL shaders for realistic rendering. The implementation will include an event horizon, accretion disk with particle system, gravitational lensing effect, photon sphere, Doppler beaming, post-processing bloom, star field background, interactive camera controls, time controls, parameter adjustment UI, educational information panel, FPS counter, keyboard shortcuts, and responsive design. All code will be embedded in one file with no external assets, using procedural generation for textures and effects.

## Learnings Applied

First iteration — no prior learnings

## Changes Required

<!-- Group by component or feature area -->
<!-- EVERY change must reference criterion IDs -->

### HTML Structure & CSS

#### File: `index.html` — CREATE
- **What**: Create complete HTML5 document with embedded CSS styling for UI overlay, controls, and information panels
- **Why**: Single file architecture required by constraints, CSS needed for UI layout and styling
- **Criteria**: C1

### Three.js Setup & CDN Integration

#### File: `index.html` — CREATE
- **What**: Add importmap for Three.js v0.162.0 from unpkg CDN, import OrbitControls, EffectComposer, UnrealBloomPass, RenderPass, ShaderPass
- **Why**: 3D rendering library and post-processing effects required for black hole visualization
- **Criteria**: C2

### Scene Initialization

#### File: `index.html` — CREATE
- **What**: Initialize Three.js scene, perspective camera, WebGL renderer with antialiasing and high pixel ratio for 4K quality
- **Why**: Basic 3D scene setup required for all rendering
- **Criteria**: C16

### Event Horizon

#### File: `index.html` — CREATE
- **What**: Create black sphere mesh at center (0,0,0) with radius representing Schwarzschild radius, using MeshBasicMaterial with black color
- **Why**: Event horizon is the defining feature of a black hole - the point of no return
- **Criteria**: C3, C20

### Accretion Disk Particle System

#### File: `index.html` — CREATE
- **What**: Create particle system with >1000 particles using BufferGeometry, custom shader for Doppler beaming effect (blue/red shift based on velocity), particles arranged in disk formation around event horizon
- **Why**: Accretion disk is the most visible feature of black holes, Doppler beaming adds scientific accuracy
- **Criteria**: C4, C7

### Gravitational Lensing Shader

#### File: `index.html` — CREATE
- **What**: Implement custom GLSL fragment shader that simulates light bending around the black hole using ray marching or refraction techniques, apply to fullscreen quad or accretion disk
- **Why**: Gravitational lensing is a key prediction of general relativity and creates the iconic black hole visual
- **Criteria**: C5

### Photon Sphere

#### File: `index.html` — CREATE
- **What**: Create glowing ring/sphere at 1.5x Schwarzschild radius using TorusGeometry or RingGeometry with emissive material and bloom effect
- **Why**: Photon sphere is the orbit where photons can circle the black hole, creating the bright ring seen in Interstellar
- **Criteria**: C6

### Post-Processing Bloom

#### File: `index.html` — CREATE
- **What**: Set up EffectComposer with RenderPass and UnrealBloomPass for cinematic glow effect on accretion disk and photon sphere
- **Why**: Bloom effect creates the cinematic, high-quality visual appearance requested
- **Criteria**: C11

### Star Field Background

#### File: `index.html` — CREATE
- **What**: Create particle system for background stars with varying brightness, size, and depth using BufferGeometry with random positions
- **Why**: Star field provides context and depth to the black hole visualization
- **Criteria**: C12

### Camera Controls

#### File: `index.html` — CREATE
- **What**: Initialize OrbitControls with enableRotate, enableZoom, enablePan all set to true, position camera at optimal viewing angle
- **Why**: Interactive camera manipulation required for user exploration
- **Criteria**: C8

### Time Control System

#### File: `index.html` — CREATE
- **What**: Implement timeControl object with pause(), play(), setSpeed(speed), reverseTime() functions, connect to animation loop
- **Why**: Time control allows users to slow down or speed up accretion disk rotation
- **Criteria**: C9

### Parameter Controls UI

#### File: `index.html` — CREATE
- **What**: Create HTML UI with sliders for black hole mass, spin parameter, accretion rate, connect to shader uniforms and simulation parameters
- **Why**: Parameter adjustment allows users to explore different black hole configurations
- **Criteria**: C10

### Educational Information Panel

#### File: `index.html` — CREATE
- **What**: Create info panel displaying black hole physics data (Schwarzschild radius, mass, type, scientific facts), update based on current parameters
- **Why**: Educational component requested to cover science and other info
- **Criteria**: C13

### FPS Counter

#### File: `index.html` — CREATE
- **What**: Implement fpsCounter object with frame counting and 1-second update interval, display in UI overlay
- **Why**: Performance monitoring required to verify 60fps target
- **Criteria**: C14

### Keyboard Shortcuts

#### File: `index.html` — CREATE
- **What**: Add event listener for keydown events handling Space (pause/play), ArrowUp/Down (speed), +/- (zoom), Escape (reset camera)
- **Why**: Keyboard controls provide efficient interaction
- **Criteria**: C15

### Responsive Design

#### File: `index.html` — CREATE
- **What**: Add window resize event listener that updates camera aspect ratio and renderer size
- **Why**: Responsive design required for different screen sizes
- **Criteria**: C16

### Physics Engine

#### File: `index.html` — CREATE
- **What**: Implement Schwarzschild radius calculation: Rs = 2GM/c², use to scale event horizon and photon sphere based on mass parameter
- **Why**: Scientific accuracy required for physics calculations
- **Criteria**: C20

### Global Object Exposure

#### File: `index.html` — CREATE
- **What**: Expose window.__BLACK_HOLE_SIM__ object containing scene, camera, renderer, controls, timeControl, fpsCounter, blackHole parameters for automated testing
- **Why**: Required for automated test access per constraints
- **Criteria**: C1-C20

## Traceability Matrix

<!--
  Verify every criterion has at least one planned change:

| Criterion | Planned Changes | Test Strategy |
|-----------|----------------|---------------|
| C1 | index.html (single file) | File system check for only index.html |
| C2 | index.html (CDN importmap) | Code review for unpkg.com script tag |
| C3 | index.html (event horizon mesh) | Code review for black sphere mesh |
| C4 | index.html (accretion disk particles) | Code review for particle count >1000 |
| C5 | index.html (lensing shader) | Code review for shader implementation |
| C6 | index.html (photon sphere) | Code review for 1.5x radius ring |
| C7 | index.html (Doppler shader) | Code review for color gradient shader |
| C8 | index.html (OrbitControls) | Code review for controls initialization |
| C9 | index.html (timeControl object) | Code review for time control functions |
| C10 | index.html (parameter UI) | Code review for slider controls |
| C11 | index.html (bloom pass) | Code review for EffectComposer setup |
| C12 | index.html (star particles) | Code review for star field system |
| C13 | index.html (info panel) | Code review for info panel HTML |
| C14 | index.html (fpsCounter) | Code review for FPS counter logic |
| C15 | index.html (keyboard events) | Code review for event listeners |
| C16 | index.html (resize handler) | Code review for resize event listener |
| C17 | index.html (file size) | File size measurement <200KB |
| C18 | index.html (no errors) | Browser console check |
| C19 | index.html (performance) | FPS measurement >=55fps |
| C20 | index.html (Rs formula) | Code review for Schwarzschild calculation |
| C21 | index.html (Hawking radiation) | Code review for particle emission (optional) |
| C22 | index.html (singularity) | Code review for central point (optional) |
| C23 | index.html (type selector) | Code review for UI selector (optional) |

## Order of Operations

<!-- Numbered list — dependencies first -->

1. Create HTML structure with embedded CSS (C1)
2. Add Three.js CDN importmap and module imports (C2)
3. Initialize scene, camera, renderer (C16)
4. Create event horizon black sphere (C3, C20)
5. Implement Schwarzschild radius calculation (C20)
6. Create accretion disk particle system with Doppler shader (C4, C7)
7. Implement gravitational lensing shader (C5)
8. Create photon sphere glowing ring (C6)
9. Set up post-processing bloom effect (C11)
10. Create star field background (C12)
11. Initialize OrbitControls (C8)
12. Implement time control system (C9)
13. Create parameter adjustment UI (C10)
14. Create educational information panel (C13)
15. Implement FPS counter (C14)
16. Add keyboard shortcuts (C15)
17. Add resize handler (C16)
18. Expose window.__BLACK_HOLE_SIM__ object (C1-C20)
19. Test file size (C17)
20. Test for console errors (C18)
21. Test performance (C19)

## Risks & Mitigations

- **Risk**: Custom GLSL shaders may not compile on all browsers
  **Mitigation**: Use standard GLSL ES 3.0 syntax, test on Chrome/Firefox/Edge, provide fallback to simpler rendering if shaders fail
- **Risk**: Post-processing bloom may impact performance below 60fps target
  **Mitigation**: Optimize bloom parameters, use reasonable resolution, provide option to disable bloom
- **Risk**: File size may exceed 200KB limit with complex shaders
  **Mitigation**: Minify shader code, use procedural generation instead of large data arrays, optimize CSS
- **Risk**: Gravitational lensing shader may be too complex for real-time rendering
  **Mitigation**: Simplify to refraction-based approach, reduce ray marching steps, optimize shader performance
- **Risk**: Particle system with >1000 particles may cause performance issues
  **Mitigation**: Use BufferGeometry efficiently, limit particle count to minimum needed for visual quality, use instanced rendering if needed

## Scope Boundary

<!--
  Explicitly list what is IN scope and what is NOT:
  - IN: [files/modules that will be touched]
  - OUT: [files/modules that must NOT be touched]
-->

**IN Scope**:
- Create: index.html (single file with all simulation code)
- Modify: .loopspec/ files (STATUS.md, STATUS.json, CHANGELOG.md for protocol tracking)

**OUT Scope**:
- No separate CSS files
- No separate JavaScript files
- No external texture files (all procedural)
- No external model files
- No build tools or bundlers
- No server-side code
- No database
- No authentication
- No API endpoints
- No optional criteria (C21-C23) unless time permits

---

> **HUMAN APPROVAL**: [x] APPROVED
>
> _Model will not proceed to Phase 3 until this checkbox is marked `[x]`._
>
> **Human Notes** _(optional)_:
> User requested end-to-end execution of LoopSpec protocol. Plan approved for implementation.>
