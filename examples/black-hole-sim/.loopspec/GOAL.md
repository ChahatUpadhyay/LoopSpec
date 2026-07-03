# Goal

<!--
  INSTRUCTIONS FOR HUMAN:
  Fill in the sections below to define what you want the AI model to achieve.
  Be as specific as possible — the model will use this as its north star.

  Each criterion MUST have a unique ID (C1, C2, ...) — the model uses these
  for traceability throughout the protocol.

  After filling this out, tell the model: "Read .loopspec/PROTOCOL.md and begin."
-->

## Objective

Create an ultra-realistic, cinematic 3D Black Hole Simulation in a single HTML file. The simulation must feature scientifically accurate visual representation of a black hole including event horizon, accretion disk, gravitational lensing, and photon sphere. The visualization should be 4K-quality with advanced shader effects, particle systems, and real-time physics-based rendering. Include interactive controls for camera manipulation, time control, and parameter adjustment. Provide comprehensive educational information about black hole physics, types, and scientific discoveries.

## Success Criteria

<!--
  Each criterion must have:
  - A unique ID (C1, C2, ...)
  - A clear, objectively verifiable description
  - A verifier type: how it will be checked (automated test, manual check, metric)
  - A threshold: what "pass" means (exact value, range, or condition)
  - Required flag: is this mandatory or nice-to-have?

  The model will not stop until ALL required criteria are VERIFIED with evidence.
-->

| ID | Criterion | Verifier | Threshold | Required |
|----|-----------|----------|-----------|----------|
| C1 | Single HTML file with embedded CSS/JS | automated | Only index.html exists, no separate .css/.js files | yes |
| C2 | Three.js loaded from CDN (unpkg or cdnjs) | automated | HTML contains CDN script tag for Three.js | yes |
| C3 | Event horizon rendered as black sphere | automated | Black sphere mesh exists at center with radius > 0 | yes |
| C4 | Accretion disk with realistic particle system | automated | Particle system with >1000 particles exists | yes |
| C5 | Gravitational lensing effect (bending light) | automated | Shader or refraction effect implemented | yes |
| C6 | Photon sphere visualization | automated | Glowing ring/sphere at 1.5x Schwarzschild radius | yes |
| C7 | Doppler beaming effect (blue/red shift) | automated | Color gradient in accretion disk based on velocity | yes |
| C8 | Interactive camera controls (OrbitControls) | automated | OrbitControls initialized with rotate/zoom/pan enabled | yes |
| C9 | Time control (pause, play, speed adjustment) | automated | Time control object with pause/play/speed functions | yes |
| C10 | Parameter controls (mass, spin, accretion rate) | automated | UI controls for adjusting black hole parameters | yes |
| C11 | Bloom/glow post-processing effect | automated | Post-processing bloom effect enabled | yes |
| C12 | Star field background with depth | automated | Star particles with varying brightness and depth | yes |
| C13 | Educational information panel | automated | Info panel with black hole physics data | yes |
| C14 | FPS counter with real-time updates | automated | FPS counter updates every second | yes |
| C15 | Keyboard shortcuts for controls | automated | Event listeners for Space, Arrows, +/- keys | yes |
| C16 | Responsive design with resize handler | automated | Window resize updates camera and renderer | yes |
| C17 | File size under 200KB (excluding Three.js CDN) | automated | index.html size < 204800 bytes | yes |
| C18 | No console errors on load | automated | Zero console.error calls | yes |
| C19 | Performance target 60fps (>=55fps average) | metric | Average FPS >= 55 over 10 seconds | yes |
| C20 | Scientific accuracy in Schwarzschild radius calculation | automated | Schwarzschild radius formula: Rs = 2GM/c² implemented | yes |
| C21 | Hawking radiation visualization (optional) | automated | Particle emission from event horizon | no |
| C22 | Singularity visualization (optional) | automated | Central point mass representation | no |
| C23 | Multiple black hole types selector (optional) | automated | UI to switch between Schwarzschild, Kerr, Reissner-Nordström | no |

## Permissions

<!--
  Check what the model is ALLOWED to do.
  Unchecked items are FORBIDDEN — the model must ask before doing them.
-->

### Standard Permissions
- [x] Read all project files
- [x] Create new files
- [x] Modify existing files
- [ ] Delete files
- [x] Execute shell commands
- [x] Run tests
- [ ] Git operations (commit, branch, push)
- [ ] Install dependencies (npm, pip, cargo, etc.)
- [ ] Modify configuration files

### Safety-Gated Permissions (require explicit approval per action)
- [x] Access network / external APIs (CDN for Three.js only)
- [ ] Modify database schemas
- [ ] Deploy to production/staging
- [ ] Actions involving secrets/credentials
- [ ] Paid API calls or cloud resource creation
- [ ] Irreversible operations (publish, send, delete remote)

## Constraints

<!--
  Boundaries the model must respect. Examples:
  - "Don't change the public API"
  - "Must support Node 18+"
  - "Keep bundle size under 500KB"
  - "Follow existing code style"
  - "No new dependencies without approval"
-->

- Single HTML file architecture (no separate CSS/JS files)
- No build tools or bundlers
- No external assets (textures, models) - generate procedurally
- Three.js loaded from CDN (unpkg.com or cdnjs.net)
- No paid APIs or cloud services
- No server-side code
- File size limit: < 200KB (excluding Three.js CDN)
- Browsers: Chrome 120+, Firefox 120+, Edge 120+
- Expose global object `window.__BLACK_HOLE_SIM__` for testing

## Priority

<!--
  What matters most? This helps the model make trade-off decisions.
  Examples: correctness > speed, readability > cleverness, test coverage > features
-->

Visual quality > Performance > Code brevity
Scientific accuracy > Cinematic effects
User experience > Feature completeness

## Quality Threshold

<!--
  Optional: define what "good enough" means for this task.
  Examples:
  - "All automated tests pass on first run"
  - ">80% test coverage on new code"
  - "Zero console errors in browser"
  - "Response time < 200ms for all endpoints"
-->

- All required criteria (C1-C20) must be VERIFIED with evidence
- Zero console errors on page load
- Performance: >=55fps average on modern hardware
- File size: <200KB (excluding Three.js CDN)
- All tests must pass in first verification cycle

## Max Iterations

<!--
  How many full plan->implement->verify->evaluate cycles before stopping?
  Default is 10. Set lower for simple tasks, higher for complex ones.
-->
max_iterations: 15

## Additional Context

<!--
  Optional: anything else the model should know.
  Links to docs, design decisions, related PRs, user stories, etc.
-->

This is a visualization project focusing on cinematic quality and scientific accuracy. Key physics concepts to implement:
- Schwarzschild radius: Rs = 2GM/c²
- Photon sphere at 1.5 × Rs
- Event horizon at Rs
- Accretion disk dynamics with Doppler beaming
- Gravitational lensing (light bending around black hole)
- Hawking radiation (optional visualization)

Visual style should match Interstellar movie's Gargantua black hole for cinematic reference. Use custom shaders for realistic accretion disk and gravitational lensing effects.
