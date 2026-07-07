# Project Context

## Tech Stack

- **Platform**: Web browser (HTML5 Canvas)
- **Languages**: HTML, CSS, JavaScript (vanilla, no frameworks)
- **Rendering**: Canvas 2D API with Web Workers for non-blocking computation
- **Build**: None — single HTML file, zero dependencies

## Project Structure

```
fractal-explorer/
├── .loopspec/          # LoopSpec protocol files
├── AGENTS.md           # AI agent entry point
└── index.html          # (to be created) Single-file application
```

## Architecture Overview

Single-file web application:
- **Fractal Engine**: Mandelbrot/Julia computation in Web Worker
- **Renderer**: Canvas 2D pixel manipulation via ImageData
- **UI Controls**: Native HTML elements (buttons, sliders, selects)
- **Event System**: Mouse events for pan/zoom/click

## Key Files & Their Roles

- `index.html` — The entire application (to be created)

## Dependencies

None. Zero external dependencies by design (C15).

## Existing Tests

None — greenfield project.

## Baseline State

**Command**: `dir examples\fractal-explorer`
**Output**: Only `.loopspec/` and `AGENTS.md` exist
**Status**: Empty project, no code written yet

## Available Runtimes

- Modern web browser (Chrome/Edge) ✓
- Python 3.11.9 ✓ (for serving if needed)
- PowerShell 5.1 ✓
- Git 2.x ✓

## Patterns & Conventions

- Single HTML file with embedded CSS and JS
- Web Worker for computation (inline blob worker)
- No external CDN/npm/library imports
- Responsive layout using CSS flexbox

