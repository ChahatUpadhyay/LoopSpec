# Project Context

## Tech Stack

- **Language**: HTML5 + JavaScript (ES6+) + CSS3
- **3D Engine**: Three.js (r160+) via CDN
- **Controls**: Three.js OrbitControls (addon)
- **Build**: None — vanilla files served directly
- **Runtime**: Browser (Chrome 120+, Firefox 120+, Edge 120+)

## Project Structure

```
oxygen-atom-sim/
├── index.html          # Single-page app (main entry)
├── test-verify.html    # Automated test harness (browser-based)
├── .loopspec/          # Protocol files
└── AGENTS.md           # AI discovery file
```

## Architecture Overview

Single-page Three.js application:
- Scene setup → Nucleus group (16 spheres) → Orbital groups (s/p clouds) → Animation loop
- OrbitControls for camera interaction
- Info panel as HTML overlay on the WebGL canvas
- No state management needed — purely visual simulation

## Key Files & Their Roles

| File | Role | Relevant to Criteria |
|------|------|---------------------|
| `index.html` | Main app: scene, nucleus, orbitals, animation, UI | C1-C10 |
| `test-verify.html` | Automated test harness that loads index.html in iframe | C1-C6, C8-C10 |

## Dependencies

- Three.js r160+ (CDN: https://unpkg.com/three@0.160.0/build/three.module.js)
- OrbitControls (CDN: https://unpkg.com/three@0.160.0/examples/jsm/controls/OrbitControls.js)
- No other external dependencies

## Existing Tests

- None (greenfield project)
- Test strategy: Browser-based test harness that inspects the Three.js scene graph
- Will use embedded `<script>` tests that run on load and report results

## Baseline State

```
$ dir oxygen-atom-sim
 Volume in drive C is OS
 Directory of C:\Users\chaha\Documents\Codex\2026-06-28\e\LoopSpec\examples\oxygen-atom-sim

02-07-2026  21:19    <DIR>          .
02-07-2026  21:19    <DIR>          .loopspec
02-07-2026  21:19             1,207 AGENTS.md
```

- Working: .loopspec/ initialized with v2 templates
- Broken: Nothing exists yet (greenfield)
- No source files to test

## Available Runtimes

- Windows 11
- PowerShell 5.1+ / CMD
- Browser (can open HTML files directly)
- No Node.js required (pure browser project)
- No test framework installed — will use browser-embedded tests

## Physics Reference (for C7)

Real quantum mechanical orbital data for Oxygen (Z=8):

| Orbital | n | l | Electrons | Mean radius (a₀ units) | Approx (Å) |
|---------|---|---|-----------|----------------------|-------------|
| 1s | 1 | 0 | 2 | ~0.33 | 0.17 |
| 2s | 2 | 0 | 2 | ~1.45 | 0.77 |
| 2p | 2 | 1 | 4 | ~1.20 | 0.64 |

Sources:
- Slater's rules for effective nuclear charge: Z_eff(1s)≈5.7, Z_eff(2s)≈3.9, Z_eff(2p)≈3.9
- Mean orbital radius formula: r̄ = (a₀/Z_eff) × [3n² - l(l+1)] / 2
- Bohr radius a₀ = 0.529 Å

Scale ratios used in visualization (exaggerated for visibility):
- Nucleus radius: 0.5 units (real: 10⁻⁵ relative to atom — invisible)
- 1s orbital cloud: radius 2.0 units
- 2s orbital cloud: radius 4.5 units (ratio ~2.2× bigger than 1s, close to real 4.4×)
- 2p orbital lobes: extend to 4.0 units from center

Hund's rule for 2p⁴: px²(paired), py¹(unpaired), pz¹(unpaired)
- 3 p-orbitals (px, py, pz) × 2 lobes each = 6 lobes
- 4 electrons fill: px gets 2 (both lobes bright), py gets 1 (one lobe bright), pz gets 1 (one lobe bright)

## Patterns & Conventions

- Single-file app (index.html contains all JS/CSS inline)
- ES6 module syntax for Three.js imports via importmap or direct URL
- Naming: camelCase for variables, PascalCase for classes/groups
- Comments for physics explanations
