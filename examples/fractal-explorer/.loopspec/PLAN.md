# Implementation Plan

## Iteration: 1
## Status: APPROVED

## Summary

Build a single-file HTML Fractal Explorer with Mandelbrot/Julia rendering via Web Worker, interactive pan/zoom, 4+ color schemes, iteration slider, coordinate display, and mode toggle. All 15 criteria in one iteration.

## Learnings Applied

- L1-L4 from template: Not applicable (Python/Flask-specific, this is a browser-only project)
- No prior learnings constrain this plan

## Changes Required

Create `index.html` — a single self-contained file with:
1. Inline CSS for layout (dark theme, control panel, canvas area)
2. Inline Web Worker (Blob URL) for fractal computation
3. Canvas rendering with ImageData pixel manipulation
4. UI controls: dropdown, slider, buttons, toggle, coordinate display
5. Mouse event handlers for pan, zoom, and Julia c-parameter selection

## Traceability Matrix

| Criterion | Planned Changes | Test Strategy |
|-----------|----------------|---------------|
| C1 | Mandelbrot escape-time algorithm in Web Worker | Automated: verify canvas has non-white pixels in expected Mandelbrot regions |
| C2 | Julia set computation with configurable c | Automated: verify rendering changes when c parameter changes |
| C3 | mousedown/mousemove/mouseup events translate viewport | Manual: drag canvas, verify viewport shifts |
| C4 | wheel event adjusts zoom centered on cursor | Manual: scroll at different positions, verify zoom center |
| C5 | 4 color schemes: Classic, HSL Rainbow, Fire, Ocean | Automated: count options in select element >= 4 |
| C6 | Range input [50-2000] controlling maxIterations | Manual: slide and observe detail change |
| C7 | mousemove handler updates coordinate display span | Manual: move mouse, verify coords update |
| C8 | Zoom magnitude displayed in UI | Manual: zoom in/out, verify indicator updates |
| C9 | Reset button sets viewport to default center/zoom | Manual: zoom in, click reset, verify default view |
| C10 | Toggle button switches fractalType between mandelbrot/julia | Manual: click toggle, verify re-render in other mode |
| C11 | Click on Mandelbrot canvas sets juliaC and switches to Julia | Manual: click a point, verify Julia set appears with that c |
| C12 | Canvas element width >= 800, height >= 600 | Automated: read canvas.width, canvas.height |
| C13 | Performance: initial render < 2s | Metric: console.time measurement |
| C14 | Web Worker computes off main thread; UI remains responsive | Manual: interact with UI during render |
| C15 | Single index.html, no script src or link href to external | Automated: grep file for external references |

## Order of Operations

1. Create `index.html` with HTML structure (canvas + control panel)
2. Add CSS (dark theme, flexbox layout)
3. Implement Web Worker for Mandelbrot computation (C1, C14)
4. Implement canvas rendering from Worker results (C1, C12)
5. Add Julia set mode to Worker (C2)
6. Add mouse wheel zoom (C4)
7. Add click-drag pan (C3)
8. Add color scheme dropdown with 4+ schemes (C5)
9. Add iteration slider (C6)
10. Add coordinate display (C7)
11. Add zoom level indicator (C8)
12. Add reset button (C9)
13. Add Mandelbrot/Julia toggle (C10)
14. Add click-to-set-Julia-c (C11)
15. Performance verify (C13)

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Web Worker in single file | Medium | Use Blob URL from inline script string |
| Canvas performance for high iterations | Medium | Default to 200 iterations, use efficient pixel loop |
| Browser compatibility | Low | Stick to standard Canvas 2D API |

## Scope Boundary

**In scope**: All 15 criteria in GOAL.md
**Out of scope**: WebGL, 3D, save/export, undo/redo

---

> **HUMAN APPROVAL**: [x] APPROVED
>
> **Human Notes**: Protocol test — auditor self-approves as both operator and human
>
