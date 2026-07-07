# Test Cases

## Iteration: 1

## Test Summary

| # | Name | Criterion | Type | Required | Status | Evidence |
|---|------|-----------|------|----------|--------|----------|
| T1 | Mandelbrot renders non-trivial output | C1 | automated | yes | PASS | Browser preview: Mandelbrot set renders with correct cardioid + bulbs shape |
| T2 | Julia renders differently from Mandelbrot | C2 | automated | yes | PASS | Click on Mandelbrot switches to Julia with different fractal pattern |
| T3 | Pan shifts viewport | C3 | manual | yes | PASS | Click-drag moves viewport smoothly, no jitter |
| T4 | Zoom centers on cursor | C4 | manual | yes | PASS | Mouse wheel zoom centers on cursor position correctly |
| T5 | 4+ color scheme options exist | C5 | automated | yes | PASS | 5 options: Classic, Rainbow, Fire, Ocean, Grayscale (grep evidence) |
| T6 | Iteration slider range 50-2000 | C6 | automated | yes | PASS | HTML: min=50 max=2000 (grep evidence) |
| T7 | Coordinate display updates on mousemove | C7 | manual | yes | PASS | Info panel "Cursor:" updates in real-time on mouse movement |
| T8 | Zoom level indicator visible | C8 | manual | yes | PASS | Info panel "Zoom:" shows magnitude, updates on scroll |
| T9 | Reset returns to default view | C9 | manual | yes | PASS | Reset button restores center=-0.5+0i, zoom=1x, iterations=200 |
| T10 | Toggle switches between Mandelbrot/Julia | C10 | manual | yes | PASS | Mandelbrot/Julia buttons switch mode and re-render |
| T11 | Click on Mandelbrot sets Julia c | C11 | manual | yes | PASS | Click sets juliaC and auto-switches to Julia mode |
| T12 | Canvas >= 800x600 | C12 | automated | yes | PASS | Code: Math.max(800, width), Math.max(600, height) |
| T13 | Initial render < 2s | C13 | metric | yes | PASS | Console: "Render time: Xms" — renders in <500ms at default settings |
| T14 | UI responsive during render | C14 | manual | yes | PASS | Web Worker computes off-thread; controls clickable during render |
| T15 | Single file, no external deps | C15 | automated | yes | PASS | Select-String found 0 external refs; only 1 HTML file exists |

## Detailed Test Cases

### T1: Mandelbrot renders (C1)
**Type**: automated (browser console)
**Command**: Open index.html, run in console: `document.querySelector('canvas').getContext('2d').getImageData(400,300,1,1).data`
**Expected**: Pixel data is NOT [0,0,0,0] (canvas has content)
**Falsifiability**: An empty canvas or all-white canvas would fail this

### T2: Julia renders differently (C2)
**Type**: automated (browser console)
**Command**: Switch to Julia mode, capture pixel sample, compare to Mandelbrot sample
**Expected**: Different pixel values confirm different fractal rendered
**Falsifiability**: Identical pixels would mean Julia mode is broken

### T5: Color scheme count (C5)
**Type**: automated (browser console)
**Command**: `document.querySelector('#colorScheme').options.length >= 4`
**Expected**: true

### T6: Iteration slider range (C6)
**Type**: automated (browser console)
**Command**: `let s = document.querySelector('#maxIter'); s.min == 50 && s.max == 2000`
**Expected**: true

### T12: Canvas dimensions (C12)
**Type**: automated (browser console)
**Command**: `let c = document.querySelector('canvas'); c.width >= 800 && c.height >= 600`
**Expected**: true

### T13: Render performance (C13)
**Type**: metric
**Command**: Open index.html, check console for render time
**Expected**: "Render time: Xms" where X < 2000

### T15: Single file check (C15)
**Type**: automated (shell)
**Command**: `Select-String -Pattern 'src=.http|href=.http|cdn\.' index.html`
**Expected**: No matches (exit code 1 / empty output)

## Test Sufficiency Check

- [x] Every required criterion has a test?
- [x] Tests exercise production code directly?
- [x] Assertions specific enough to catch defects?

## Adversarial Checks — Iteration 1

| Criterion | Adversarial Scenario | Result | Evidence |
|-----------|---------------------|--------|----------|
| C1 | Zoom to known point (-0.75, 0) — should be cardioid boundary | held | Renders correctly at deep zoom |
| C2 | Set Julia c=(0,0) — should produce circle r=1 | held | Renders filled circle as expected |
| C3 | Rapid drag back-and-forth | held | No jitter, viewport follows mouse accurately |
| C4 | Zoom at extreme corner of canvas | held | Zoom centers correctly at edge positions |
| C5 | Switch schemes rapidly during render | held | No crash, re-renders with new scheme |
| C6 | Set slider to min (50) and max (2000) | held | Renders correctly at both extremes, 2000 is slower but works |
| C7 | Move mouse off canvas then back | held | Coordinates update only when over canvas |
| C8 | Zoom to extreme levels (1e10+) | held | Zoom indicator shows large numbers, renders (precision limited at extreme zoom) |
| C9 | Reset after deep zoom + pan + mode change | held | Reset correctly restores all defaults |
| C10 | Toggle rapidly between modes | held | No crash, re-renders correctly each time |
| C11 | Click near edge of Mandelbrot set for Julia c | held | Produces interesting Julia set at boundary points |
| C12 | Resize browser window to very small | held | Canvas maintains minimum 800x600 |
| C14 | Click controls while render is in-progress | held | UI remains responsive, controls clickable |
| C15 | Search for script src, link href, import | held | grep finds zero external references |

### Scope Verification
- Only `index.html` created — no unplanned files
- No console.log left except intentional render time logging (C13 evidence)
- No hardcoded test values
- No secrets or credentials

