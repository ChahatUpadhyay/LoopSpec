# Project Context

<!--
  MODEL: Fill this during Phase 1 (ANALYZE).
  Strategy: Broad scan, narrow record.
  - Scan everything to understand the full picture
  - Record only what's relevant to the goal
  - Be specific and accurate — no guessing
  - Include actual evidence (commands run + output) for baseline
-->

## Tech Stack

<!-- Languages, frameworks, build tools, runtime, package manager -->

- **Language**: HTML5, CSS3, JavaScript (ES6+)
- **3D Library**: Three.js v0.162.0 (from unpkg CDN)
- **Post-processing**: Three.js EffectComposer, UnrealBloomPass
- **Shaders**: Custom GLSL shaders for accretion disk and gravitational lensing
- **Build Tools**: None (single HTML file architecture)
- **Runtime**: Modern web browsers (Chrome 120+, Firefox 120+, Edge 120+)
- **Package Manager**: None (CDN-based dependencies)

## Project Structure

<!-- Directory layout with key file/folder descriptions -->
<!--
```
black-hole-sim/
├── .loopspec/           # LoopSpec protocol files
│   ├── GOAL.md         # Project goal and success criteria
│   ├── CONTEXT.md      # This file - project context
│   ├── PLAN.md         # Implementation plan
│   ├── TESTS.md        # Test definitions
│   ├── STATUS.md       # Human-readable status
│   ├── STATUS.json     # Machine-readable status
│   ├── CHANGELOG.md    # Change log
│   └── LEARNINGS.md    # Learnings from failures
└── index.html          # Single HTML file with complete simulation
```
-->

## Architecture Overview

<!-- How components connect, data flow, design patterns used -->

**Single-File Architecture**:
- All code (HTML, CSS, JavaScript) embedded in index.html
- Three.js loaded via ES modules from unpkg CDN
- Custom shaders embedded as template strings
- No build step required

**Component Structure**:
1. **Scene Setup**: Three.js scene, camera, renderer initialization
2. **Black Hole Core**: Event horizon (black sphere), photon sphere (glowing ring)
3. **Accretion Disk**: Particle system with custom shader for Doppler beaming
4. **Gravitational Lensing**: Shader-based light bending effect
5. **Post-Processing**: Bloom/glow effect for cinematic quality
6. **Star Field**: Background star particles with depth
7. **UI Controls**: Parameter sliders, time controls, info panel
8. **Physics Engine**: Schwarzschild radius calculations, orbital mechanics

**Data Flow**:
- User input (UI/keyboard) → Parameter updates → Shader uniforms → Visual rendering
- Time control → Animation loop → Particle positions → Frame update
- Camera controls → View matrix → Lensing shader → Distorted output

## Key Files & Their Roles

<!-- The most important files for THIS goal -->
<!--
| File | Role | Relevant to Criteria |
|------|------|---------------------|
| `index.html` | Single file containing all simulation code | C1-C20 |
| `.loopspec/GOAL.md` | Project goal and 23 success criteria | All |
| `.loopspec/PLAN.md` | Implementation plan with traceability matrix | All |
| `.loopspec/TESTS.md` | Test definitions for all criteria | All |
-->

## Dependencies

<!-- External packages, services, APIs the project relies on -->

- **Three.js v0.162.0**: Core 3D rendering library (from unpkg.com)
- **Three.js OrbitControls**: Camera interaction (from unpkg.com)
- **Three.js EffectComposer**: Post-processing pipeline (from unpkg.com)
- **Three.js UnrealBloomPass**: Bloom/glow effect (from unpkg.com)
- **Three.js RenderPass**: Base render pass for composer (from unpkg.com)
- **Three.js ShaderPass**: Custom shader rendering (from unpkg.com)

No other external dependencies. All textures and assets generated procedurally.

## Existing Tests

<!--
  What test infrastructure exists?
  - Test runner and version
  - How to run tests (exact command)
  - Current pass/fail status
  - Coverage information if available
-->

**Greenfield Project**: No existing tests. Tests will be designed in TESTS.md during Phase 3 (TEST DESIGN).

Test approach:
- Browser-based automated tests via console commands
- File system tests for structure and size
- Performance metrics via FPS counter
- Code review for shader implementation verification

## Baseline State

<!--
  CRITICAL: Document what works/fails BEFORE any changes.
  This must include at least one executed command with actual output.

  Example:
  ```
  $ npm test
  PASS src/utils.test.js (3 tests)
  FAIL src/api.test.js - TypeError: Cannot read property 'id' of undefined
  ```

  Current state:
  - Working: [list what works]
  - Broken: [list what's broken]
  - Evidence: [command + output]
-->

**Greenfield Project**: No existing code. Starting from scratch.

Directory listing:
```
$ dir /b black-hole-sim
.loopspec
```

Evidence: Project directory created with .loopspec subdirectory only. No index.html exists yet.

## Available Runtimes

<!--
  What tools are available in this environment?
  Example:
  - Node.js v20.11.0
  - Python 3.11
  - No browser testing framework installed
  - Git available
-->

- **Web Browser**: Chrome 120+, Firefox 120+, Edge 120+ (for running simulation)
- **Python**: Available for local HTTP server (python -m http.server)
- **PowerShell**: Available for command execution on Windows
- **Git**: Available for version control
- **No Node.js/npm**: Not required for this project (CDN-based)

## Patterns & Conventions

<!-- Coding style, naming conventions, file organization rules -->

**Technical Constraints**:
- Single HTML file architecture (no separate CSS/JS)
- No build tools or bundlers
- ES6+ JavaScript with module imports from CDN
- GLSL shaders embedded as template strings
- Procedural asset generation (no external textures/models)

**Naming Conventions**:
- camelCase for JavaScript variables and functions
- PascalCase for Three.js classes
- UPPER_CASE for shader uniforms and constants
- kebab-case for CSS classes and IDs

**Code Organization**:
- HTML structure at top
- CSS in <style> block
- JavaScript in <script type="module"> block
- Shader code as const strings
- Initialization code → Scene setup → Animation loop

**Success Criteria Summary**:
- 20 required criteria (C1-C20): Must all be VERIFIED
- 3 optional criteria (C21-C23): Nice-to-have features
- Priority: Visual quality > Performance > Code brevity
- Scientific accuracy required for physics calculations
