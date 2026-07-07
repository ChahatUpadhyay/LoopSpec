# Goal

## Objective

Build an **Interactive Fractal Explorer** — a web-based Mandelbrot and Julia Set visualizer with real-time zoom, pan, multiple color schemes, coordinate display, iteration control, and smooth performance. Single-file HTML/JS/CSS application using Canvas API.

## Success Criteria

| ID | Criterion | Verifier | Threshold | Required |
|----|-----------|----------|-----------|----------|
| C1 | Mandelbrot set renders correctly on HTML Canvas | automated | Visual output matches known Mandelbrot shape | yes |
| C2 | Julia set renders correctly with configurable c parameter | automated | Visual output matches known Julia set shapes | yes |
| C3 | Click-drag pan moves the viewport smoothly | manual | No jitter, viewport follows mouse | yes |
| C4 | Mouse wheel zoom works centered on cursor position | manual | Zoom in/out centered where cursor points | yes |
| C5 | At least 4 distinct color schemes selectable via UI | automated | Dropdown with 4+ schemes, each produces different colors | yes |
| C6 | Max iteration count adjustable via slider (50-2000) | manual | Slider changes detail level visibly | yes |
| C7 | Coordinate display shows current mouse position in fractal space | manual | Updates in real-time as mouse moves | yes |
| C8 | Zoom level indicator displayed in UI | manual | Shows current zoom magnitude | yes |
| C9 | Reset button returns to default view | manual | One click restores original viewport | yes |
| C10 | Toggle between Mandelbrot and Julia set modes | manual | Button/toggle switches mode, re-renders | yes |
| C11 | Julia set c-parameter adjustable via mouse click on Mandelbrot | manual | Clicking Mandelbrot view sets Julia c value | yes |
| C12 | Canvas renders at minimum 800x600 resolution | automated | Canvas dimensions >= 800x600 | yes |
| C13 | Initial render completes in < 2 seconds on modern browser | metric | Time from load to first paint < 2s | yes |
| C14 | Responsive UI — controls don't block during render | manual | UI remains interactive, uses Web Workers or chunked rendering | yes |
| C15 | Single HTML file, no external dependencies | automated | One .html file, no CDN/npm imports | yes |

## Permissions

- [x] Read all project files
- [x] Create new files
- [x] Modify existing files
- [x] Delete files
- [x] Execute shell commands
- [x] Run tests
- [x] Git operations
- [ ] Install dependencies
- [ ] Network / external APIs
- [ ] Deploy
- [ ] Secrets/credentials
- [ ] Irreversible operations

## Constraints

- Single HTML file — no build tools, no npm, no external dependencies
- Must work in modern browsers (Chrome, Firefox, Edge)
- Canvas API only (no WebGL required, but allowed for performance)
- Responsive layout

## Priority

C1 > C2 > C4 > C3 > C5 > C14 > C6 > C10 > C11 > C7 > C8 > C9 > C12 > C13 > C15

## Max Iterations

max_iterations: 5

## Additional Context

This project serves as an independent test of the LoopSpec v3 protocol by an AI auditor. All 7 phases will be followed strictly with evidence documented at every step.

