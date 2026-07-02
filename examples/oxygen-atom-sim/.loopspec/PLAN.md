# Implementation Plan

## Iteration: 1
## Status: APPROVED

## Summary

Build a single-page Three.js app (`index.html`) that renders an oxygen atom with a physically-accurate orbital model. The nucleus uses 16 individual sphere meshes in a clustered group. Electron orbitals use probability-cloud meshes: spherical for s-orbitals (semi-transparent spheres), dumbbell shapes for p-orbitals (pairs of ellipsoid lobes). Hund's rule is visualized by varying opacity (filled vs empty lobes). A separate `test-verify.html` inspects the scene graph programmatically to verify all criteria.

## Learnings Applied

First iteration — no prior learnings.

## Changes Required

### Core Application

#### File: `index.html` — CREATE
- **What**: Single-page app with inline JS/CSS. Creates Three.js scene with:
  - Nucleus group: 8 red spheres (protons) + 8 gray-blue spheres (neutrons) packed in a cluster
  - 1s orbital: 2 concentric semi-transparent spheres (inner shell)
  - 2s orbital: 2 larger concentric semi-transparent spheres
  - 2p orbitals: 3 dumbbell pairs (px, py, pz) with Hund's rule coloring (px bright, py/pz half-bright)
  - OrbitControls for camera
  - Info panel overlay with atom data
  - Animation loop with subtle rotation
- **Why**: This is the entire application — all criteria depend on it
- **Criteria**: C1, C2, C3, C4, C5, C6, C7, C8, C9, C10

### Test Harness

#### File: `test-verify.html` — CREATE
- **What**: Automated browser test that loads index.html, waits for scene ready, then inspects:
  - Nucleus group children count and colors
  - Electron orbital counts and geometry types
  - OrbitControls properties
  - DOM text content
  - Console error interception
  - Frame timing measurement
- **Why**: Provides executable evidence for all automated criteria
- **Criteria**: C1, C2, C3, C4, C5, C6, C8, C9, C10

## Traceability Matrix

| Criterion | Planned Changes | Test Strategy |
|-----------|----------------|---------------|
| C1 | Nucleus group in index.html | Count scene.getObjectByName('nucleus').children, verify colors |
| C2 | Orbital groups in index.html | Count all electron representations across orbital groups |
| C3 | s-orbital meshes with SphereGeometry + opacity | Check geometry type and material.opacity < 1 |
| C4 | p-orbital lobes as scaled ellipsoids on x/y/z | Check lobe mesh positions align to axes |
| C5 | requestAnimationFrame loop | Measure frame deltas over 60 frames |
| C6 | OrbitControls instantiation | Check controls.enableRotate/Zoom/Pan === true |
| C7 | Physics data in CONTEXT.md | Manual verification (already documented) |
| C8 | Clean initialization | Intercept console.error/warn before page load |
| C9 | Hund's rule: 4/6 lobes filled | Check opacity/color differences in p-orbital lobes |
| C10 | Info panel DOM | querySelector for text content |

## Order of Operations

1. Create `index.html` with complete Three.js scene
2. Verify it opens in browser without errors (manual quick-check)
3. Create `test-verify.html` with automated assertions
4. Run tests and collect evidence

## Risks & Mitigations

- **Risk**: Three.js CDN import might fail with ES module CORS on file:// protocol
  **Mitigation**: Use importmap with CDN URL, or fall back to global script tag (non-module)

- **Risk**: p-orbital dumbbell geometry might not look correct
  **Mitigation**: Use scaled SphereGeometry (scale.z * 2) to create ellipsoid lobes

- **Risk**: Test harness cannot access iframe scene due to same-origin policy on file://
  **Mitigation**: Embed tests directly in index.html behind a `?test=true` URL parameter

## Scope Boundary

- **IN**: index.html, test-verify.html, .loopspec/ files
- **OUT**: .loopspec/PROTOCOL.md (read-only), AGENTS.md (no changes needed)

---

> **HUMAN APPROVAL**: [x] APPROVED
>
> _Model will not proceed to Phase 3 until this checkbox is marked `[x]`._
>
> **Human Notes**: Proceed. The file:// CORS risk is real — use the ?test=true fallback approach.
