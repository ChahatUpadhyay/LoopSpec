# Changelog

<!-- Append-only. Log: iteration, phase, files changed, criteria served. -->

---

## Iteration 1 — Phase: IMPLEMENT — 2026-07-07

### Files Created
- `index.html` — Single-file Fractal Explorer (C1-C15)

### Criteria Served
- C1: Mandelbrot escape-time algorithm in Web Worker
- C2: Julia set with configurable c parameter
- C3: Click-drag pan via mousedown/mousemove/mouseup
- C4: Mouse wheel zoom centered on cursor position
- C5: 5 color schemes (Classic, Rainbow, Fire, Ocean, Grayscale)
- C6: Iteration slider range 50-2000
- C7: Real-time coordinate display on mousemove
- C8: Zoom level indicator in info panel
- C9: Reset button restores default view
- C10: Mandelbrot/Julia mode toggle buttons
- C11: Click on Mandelbrot sets Julia c and switches mode
- C12: Canvas >= 800x600 (dynamic sizing)
- C13: Performance logging via console.time
- C14: Web Worker for non-blocking computation
- C15: Single HTML file, zero external dependencies

### Key Decisions
- Used inline Blob Worker to keep single-file constraint
- 5 color schemes instead of minimum 4 (exceeded C5)
- Dark theme UI with sidebar control panel

