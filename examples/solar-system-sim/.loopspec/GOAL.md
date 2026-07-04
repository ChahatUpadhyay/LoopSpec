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

Build a complete, interactive 3D Solar System Simulator with realistic orbital mechanics, accurate planetary data, and rich user controls. The simulator should be educational, visually stunning, and performant, running entirely in a single HTML file with no build tools or external dependencies beyond Three.js from CDN.

Key features:
- All 8 planets with accurate relative sizes, orbital distances, and orbital periods
- Realistic orbital mechanics using Kepler's laws
- Interactive camera controls (zoom, pan, rotate)
- Time controls (pause, play, speed up, slow down, reverse)
- Planet information panels with real astronomical data
- Orbital trails showing planetary paths
- Sun with glow effect and proper lighting
- Asteroid belt visualization
- Moon orbiting Earth
- Responsive design that works on different screen sizes
- Performance monitoring (FPS counter)
- Keyboard shortcuts for common actions

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
| C1 | Single HTML file with embedded CSS/JS (no build tools, no bundler) | automated | File count = 1, no .css/.js files in directory | yes |
| C2 | Three.js loaded from CDN (unpkg or cdnjs) | automated | HTML contains CDN script tag for Three.js | yes |
| C3 | All 8 planets rendered (Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune) | automated | Window.__SOLAR_SIM__.planets.length = 8 with correct names | yes |
| C4 | Sun rendered at center with glow effect | automated | Window.__SOLAR_SIM__.sun exists and has glow material | yes |
| C5 | Planets have accurate relative sizes (Jupiter > Saturn > Uranus/Neptune > Earth/Venus > Mars > Mercury) | automated | Size ratios match expected order within 10% tolerance | yes |
| C6 | Planets have accurate relative orbital distances (Mercury closest, Neptune farthest) | automated | Distance ratios match expected order within 15% tolerance | yes |
| C7 | Planets orbit at different speeds based on Kepler's laws (inner planets faster) | automated | Orbital periods decrease with distance from sun | yes |
| C8 | Camera controls enabled (OrbitControls for zoom, pan, rotate) | automated | Window.__SOLAR_SIM__.controls exists with enableRotate, enableZoom, enablePan = true | yes |
| C9 | Time controls work (pause, play, speed adjustment) | automated | Window.__SOLAR_SIM__.timeControl exists with pause/play/speed functions | yes |
| C10 | Orbital trails visible for all planets | automated | Each planet has a trail object with >100 points | yes |
| C11 | Asteroid belt rendered between Mars and Jupiter | automated | Window.__SOLAR_SIM__.asteroidBelt exists with >100 particles | yes |
| C12 | Moon orbiting Earth | automated | Window.__SOLAR_SIM__.moon exists and is child of Earth mesh | yes |
| C13 | Planet information panels display real astronomical data (mass, diameter, orbital period) | automated | Each planet has data object with mass, diameter, orbitalPeriod properties | yes |
| C14 | FPS counter displayed and running | automated | Window.__SOLAR_SIM__.fpsCounter exists and updates every second | yes |
| C15 | Keyboard shortcuts implemented (space=pause, arrows=speed, +/- = zoom) | automated | Event listeners for Space, ArrowUp, ArrowDown, +, - keys | yes |
| C16 | Responsive design (canvas resizes with window) | automated | Resize event listener updates camera aspect and renderer size | yes |
| C17 | Saturn has visible rings | automated | Saturn mesh has ring geometry with >1000 vertices | yes |
| C18 | File size under 100KB (excluding Three.js CDN) | automated | HTML file size < 100KB | yes |
| C19 | No console errors on load | automated | Console.error count = 0 after page load | yes |
| C20 | Animation loop runs at 60fps on modern hardware | metric | Average FPS >= 55 over 10 seconds | yes |

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
- [ ] Run tests
- [ ] Git operations (commit, branch, push)
- [ ] Install dependencies (npm, pip, cargo, etc.)
- [ ] Modify configuration files

### Safety-Gated Permissions (require explicit approval per action)
- [ ] Access network / external APIs
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

- Single HTML file only - no separate CSS or JS files
- No build tools, bundlers, or package managers
- Three.js must be loaded from CDN (unpkg.com or cdnjs)
- No server-side code - pure client-side
- File size must stay under 100KB (excluding Three.js CDN)
- Must work in Chrome 120+, Firefox 120+, Edge 120+
- No external assets (textures, models) - procedural generation only
- No paid APIs or cloud services
- No secrets or credentials in code

## Priority

<!--
  What matters most? This helps the model make trade-off decisions.
  Examples: correctness > speed, readability > cleverness, test coverage > features
-->

1. Correctness (accurate orbital mechanics and planetary data)
2. Performance (60fps on modern hardware)
3. Code quality (clean, readable, well-organized)
4. User experience (smooth controls, responsive design)
5. Visual appeal (good lighting, colors, effects)

## Quality Threshold

<!--
  Optional: define what "good enough" means for this task.
  Examples:
  - "All automated tests pass on first run"
  - ">80% test coverage on new code"
  - "Zero console errors in browser"
  - "Response time < 200ms for all endpoints"
-->

- All automated tests pass on first run
- Zero console errors in browser
- Average FPS >= 55 on modern hardware
- File size < 100KB
- All required criteria verified with evidence

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

Planetary data reference (approximate values for visualization):
- Mercury: 0.38 Earth radii, 0.39 AU orbital distance, 88 day orbital period
- Venus: 0.95 Earth radii, 0.72 AU orbital distance, 225 day orbital period
- Earth: 1.00 Earth radii, 1.00 AU orbital distance, 365 day orbital period
- Mars: 0.53 Earth radii, 1.52 AU orbital distance, 687 day orbital period
- Jupiter: 11.2 Earth radii, 5.20 AU orbital distance, 12 year orbital period
- Saturn: 9.45 Earth radii, 9.58 AU orbital distance, 29 year orbital period
- Uranus: 4.00 Earth radii, 19.2 AU orbital distance, 84 year orbital period
- Neptune: 3.88 Earth radii, 30.1 AU orbital distance, 165 year orbital period

Note: Distances and sizes should be scaled for visual clarity (not 1:1 scale) but relative proportions should be preserved.
