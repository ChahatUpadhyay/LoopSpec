# Goal

## Objective

Build an interactive 3D simulation of an Oxygen atom that accurately models:
- The nucleus (8 protons + 8 neutrons) as a clustered core with distinguishable particles
- All 8 electrons in their correct orbital shells (1s², 2s², 2p⁴) with realistic probability-cloud behavior
- Quantum mechanical orbital shapes (s-orbitals = spherical, p-orbitals = dumbbell/figure-8)
- Real physics constants for scale relationships (not Bohr model circles — use probabilistic electron clouds)
- Smooth 60fps animation with orbital rotation and electron probability density visualization
- Interactive camera controls (rotate, zoom, pan)

The simulation must be a single-page web app using Three.js (no server required), opening directly via `index.html` in any modern browser.

## Success Criteria

| ID | Criterion | Verifier | Threshold | Required |
|----|-----------|----------|-----------|----------|
| C1 | Nucleus contains exactly 8 protons (red) and 8 neutrons (blue/gray) clustered in a sphere | automated | Count particles in nucleus group === 16, with 8 red + 8 blue/gray | yes |
| C2 | Electron configuration matches oxygen: 1s²(2), 2s²(2), 2p⁴(4) = 8 total electrons | automated | Count electron representations === 8, distributed as 2+2+4 across shells | yes |
| C3 | s-orbitals render as spherical probability clouds (not circular orbits) | automated | s-orbital mesh geometry is SphereGeometry or IcosahedronGeometry with opacity < 1 | yes |
| C4 | p-orbitals render as dumbbell/lobe shapes along correct axes (px, py, pz) | automated | p-orbital meshes have two-lobe geometry, oriented on x/y/z axes | yes |
| C5 | Animation runs at >= 55fps on a standard machine (no dropped frames) | metric | requestAnimationFrame delta consistently < 18ms (55fps) | yes |
| C6 | Camera controls allow rotate, zoom, and pan via mouse/touch | automated | OrbitControls instantiated with enableRotate, enableZoom, enablePan all true | yes |
| C7 | Physics scale ratios are documented and based on real quantum mechanical data | manual | CONTEXT.md contains cited electron orbital radii ratios (1s:2s:2p) | yes |
| C8 | Page loads without any console errors or warnings | automated | Zero console.error or console.warn calls during initialization and first 3 seconds | yes |
| C9 | Electrons in 2p orbitals show partial filling (4 of 6 possible) per Hund's rule | automated | Only 4 of the 6 p-orbital lobes are "occupied" (visually distinct filled vs empty) | yes |
| C10 | Info panel displays atom name, atomic number, electron configuration, and orbital legend | automated | DOM contains elements with text: "Oxygen", "8", "1s² 2s² 2p⁴" | yes |

## Permissions

### Standard Permissions
- [x] Read all project files
- [x] Create new files
- [x] Modify existing files
- [ ] Delete files
- [x] Execute shell commands
- [x] Run tests
- [ ] Git operations (commit, branch, push)
- [ ] Install dependencies (npm, pip, cargo, etc.)
- [x] Modify configuration files

### Safety-Gated Permissions (require explicit approval per action)
- [x] Access network / external APIs (CDN for Three.js only)
- [ ] Modify database schemas
- [ ] Deploy to production/staging
- [ ] Actions involving secrets/credentials
- [ ] Paid API calls or cloud resource creation
- [ ] Irreversible operations (publish, send, delete remote)

## Constraints

- Single HTML file + JS/CSS (no build tools, no bundler, no npm)
- Three.js loaded from CDN (unpkg or cdnjs)
- Must work offline after initial Three.js cache
- No server-side code — pure client-side
- File size: total JS+HTML+CSS under 50KB (excluding Three.js CDN)
- Must work in Chrome 120+, Firefox 120+, Edge 120+

## Priority

Physics accuracy > Visual beauty > Performance > Code elegance

## Quality Threshold

- All 10 automated/metric criteria pass with evidence
- Zero console errors on page load
- Smooth animation (no visible jank for 10 seconds)
- Orbital shapes recognizable by someone with basic chemistry knowledge

## Max Iterations

max_iterations: 5

## Additional Context

- Oxygen: Z=8, electron config [He] 2s² 2p⁴
- Real orbital radii ratios (approximate): 1s ≈ 0.53Å, 2s ≈ 2.12Å, 2p ≈ 2.12Å (n²×a₀ simplified)
- Hund's rule: 2p⁴ means px², py¹, pz¹ (or equivalent — 2 paired + 2 unpaired)
- Use probability density visualization, not fixed-position particles for electrons
- Nucleus scale is greatly exaggerated for visibility (real: 10⁻¹⁵m vs atom 10⁻¹⁰m)
