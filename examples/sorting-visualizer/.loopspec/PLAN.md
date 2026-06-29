# Implementation Plan

## Iteration: 1
## Status: ✅ APPROVED (pre-approved by human)

## Summary

Build a premium sorting algorithm visualizer as a single-page vanilla web app. The app will render arrays as colored bar charts, support 4 sorting algorithms with real-time animation, offer controls for speed/size, a step-by-step mode, a side-by-side comparison mode, and a live statistics dashboard — all wrapped in a dark glassmorphism UI. The architecture uses a single HTML entry point, a CSS file with custom properties and responsive grid layout, and a JS file that implements all sorting logic using async/await with configurable delays for animation.

## Learnings Applied

- No prior learnings (first iteration, LEARNINGS.md is empty)

## Changes Required

### 1. App Shell & Layout

#### File: `index.html` — CREATE
- **What**: Create the full HTML structure:
  - `<header>` with app title and tagline
  - Controls panel: algorithm selector `<select>`, array size `<input type="range">`, speed `<select>`, buttons (Generate, Sort, Step, Reset, Compare Mode toggle)
  - Single visualizer `<div id="visualizer">` with a bar container
  - Comparison panel `<div id="comparison-panel">` (hidden by default) with two side-by-side bar containers + two algorithm selectors
  - Statistics panel: comparisons, swaps, elapsed time, Big-O notation
  - Link to `style.css`, defer `app.js`
- **Why**: Addresses Criteria 1, 4, 5, 6, 7, 8

### 2. Premium Visual Design

#### File: `style.css` — CREATE
- **What**: Create the complete stylesheet:
  - CSS custom properties for color palette (dark purples, cyans, gradients)
  - Dark background with subtle gradient animation
  - Glassmorphism cards: `backdrop-filter: blur()`, semi-transparent backgrounds, subtle borders
  - Bar styling: gradient fills, border-radius, smooth height transitions
  - Color states: default (gradient), comparing (amber/orange), swapping (red), sorted (green)
  - Button micro-animations: hover scale, glow effects, ripple
  - Responsive breakpoints: desktop (>1024px), tablet (768-1024px), mobile (<768px)
  - CSS Grid for main layout, Flexbox for internal components
  - Comparison mode: CSS Grid with 2 equal columns
- **Why**: Addresses Criteria 3, 8, 9

### 3. Application Logic

#### File: `app.js` — CREATE
- **What**: Create the complete application JavaScript:
  
  **State Management (~50 lines)**
  - App state object: array, sorting flag, speed, algorithm, step mode, comparison mode
  - Array generation: random values scaled to container height
  
  **DOM Rendering (~80 lines)**
  - `renderBars(containerId, array)`: create/update bar divs with height, color, labels
  - `highlightBars(indices, color)`: add/remove highlight classes
  - `updateStats(stats)`: update statistics DOM elements
  
  **Sorting Algorithms (~300 lines)**
  - Each algorithm: async function with `await delay()` calls
  - `bubbleSort(arr, render, stats)`: nested loops, swap animation
  - `insertionSort(arr, render, stats)`: shift animation
  - `mergeSort(arr, render, stats)`: recursive with auxiliary array visualization
  - `quickSort(arr, render, stats)`: partition with pivot highlighting
  - All algorithms accept a `stepController` for step-by-step mode
  - All algorithms increment comparison/swap counters in stats object
  
  **Step-by-Step Controller (~40 lines)**
  - Promise-based pause: `await stepController.waitForStep()`
  - Resolves on "Next Step" button click
  
  **Comparison Mode (~60 lines)**
  - Clone array, run two algorithms simultaneously with `Promise.all`
  - Each operates on its own container and stats panel
  
  **Speed/Delay (~20 lines)**
  - Speed mapping: slow=150ms, medium=50ms, fast=5ms
  - `delay(ms)` using Promise + setTimeout
  
  **Event Handlers (~80 lines)**
  - Generate button → new random array + render
  - Sort button → run selected algorithm
  - Speed slider → update delay
  - Size slider → regenerate array
  - Step button → resolve step promise
  - Compare toggle → show/hide comparison panel
  
  **Initialization (~30 lines)**
  - DOMContentLoaded → generate initial array, bind events
  
- **Why**: Addresses Criteria 1, 2, 3, 4, 5, 6, 7, 10, 12

### 4. Test Harness

#### File: `test.html` — CREATE
- **What**: Create a browser-based test page:
  - Import sorting algorithm functions (extracted as testable pure functions)
  - Test each algorithm with: random arrays, already sorted, reverse sorted, single element, empty, duplicates
  - Display pass/fail results in the page
  - Also create a Node.js-compatible version in the `<script>` for CLI verification
- **Why**: Addresses Criterion 10

## Order of Operations

1. Create `style.css` — design system and all styles first (no dependencies)
2. Create `index.html` — semantic structure, link CSS and JS
3. Create `app.js` — all application logic
4. Create `test.html` — test harness for sorting correctness
5. Verify — run tests, review code, check all criteria

## Risks & Mitigations

- **Risk**: Merge sort visualization is complex (auxiliary arrays)
  **Mitigation**: Use in-place merge sort variant, or visualize by updating bar positions to match the merged result at each level

- **Risk**: Step-by-step mode and comparison mode interaction
  **Mitigation**: Disable step mode when comparison mode is active (comparison always runs continuous)

- **Risk**: Responsive layout breaks with many bars
  **Mitigation**: Dynamically calculate bar width from container width / array size, remove gaps at high counts

- **Risk**: CSS transitions may conflict with rapid JS DOM updates
  **Mitigation**: Use `transition` on height property only, keep transitions short (200ms) to avoid queue buildup

---

> **HUMAN APPROVAL**: [x] APPROVED
> 
> _Plan pre-approved by human. Proceeding to Phase 3._
