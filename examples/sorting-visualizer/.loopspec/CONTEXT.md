# 🔍 Project Context

<!-- MODEL: Fill this during Phase 1: ANALYZE. Be thorough and accurate. -->

## Tech Stack

- **Languages**: HTML5, CSS3, JavaScript (ES6+)
- **Frameworks**: None — vanilla only (per GOAL.md constraints)
- **Build Tools**: None — open `index.html` directly in browser
- **Runtime**: Modern browsers (Chrome, Firefox, Edge)
- **External Dependencies**: None — fully self-contained, no CDNs

## Project Structure

```
loopspec-test-project/
├── .loopspec/           # Protocol control files
│   ├── PROTOCOL.md      # Operating manual (read-only)
│   ├── GOAL.md          # Success criteria & permissions (read-only)
│   ├── CONTEXT.md       # This file — project analysis
│   ├── PLAN.md          # Implementation plan
│   ├── TESTS.md         # Test cases and results
│   ├── CHANGELOG.md     # Append-only change log
│   ├── LEARNINGS.md     # Append-only error/fix log
│   ├── QUESTIONS.md     # Human Q&A
│   ├── STATUS.md        # Current execution state
│   └── iterations/      # Archived iteration snapshots
├── index.html           # Main app entry point (TO CREATE)
├── style.css            # Premium dark-theme styles (TO CREATE)
├── app.js               # All sorting logic + UI (TO CREATE)
└── test.html            # Browser-based test harness (TO CREATE)
```

## Architecture Overview

**Single-page application (SPA)** with no routing:

1. **index.html** — Semantic HTML structure: header, controls panel, visualizer area (single + comparison), statistics panel, footer
2. **style.css** — Dark glassmorphism theme with CSS custom properties, grid/flexbox layout, transitions/animations
3. **app.js** — Entire application logic:
   - Array generation and state management
   - 4 sorting algorithms (Bubble, Quick, Merge, Insertion) using async/await with configurable delays
   - DOM rendering: bars rendered as `<div>` elements with dynamic heights
   - UI controls: sliders, buttons, dropdowns
   - Comparison mode: dual-panel side-by-side visualization
   - Step-by-step mode: manual advancement with yield-like pausing
   - Statistics tracking: comparisons, swaps, elapsed time, Big-O display
   - Responsive behavior

**Data Flow**:
- User adjusts controls → JS generates new array → Bars rendered via DOM
- User clicks Sort → async sorting algorithm runs → each step updates DOM with delay → stats update in real-time
- Comparison mode → two independent sorting instances run simultaneously on cloned arrays

## Key Files & Their Roles

| File | Role |
|------|------|
| `index.html` | App shell: layout, controls, visualizer containers, stats panel |
| `style.css` | All visual styling: dark theme, glassmorphism, animations, responsive breakpoints |
| `app.js` | All logic: sorting algorithms, DOM manipulation, event handlers, state management |
| `test.html` | Standalone test page: imports sorting functions, runs correctness tests, displays results |

## Dependencies

- **External packages**: None
- **External services/APIs**: None
- **Browser APIs used**: DOM, CSS Transitions, `requestAnimationFrame`, `performance.now()`

## Existing Tests

- **Test infrastructure**: None yet — `test.html` will be created in Phase 3
- **Coverage**: 0% — new project

## Current State / Known Issues

- **Current state**: Empty project — only `.loopspec/` directory exists with template files
- **Known issues**: None (greenfield project)
- **STATUS.md**: IDLE, Iteration 0

## Patterns & Conventions

- **Code style**: ES6+ (const/let, arrow functions, template literals, async/await) per Criterion 12
- **File organization**: Single file per concern (HTML, CSS, JS)
- **Naming**: camelCase for JS variables/functions, kebab-case for CSS classes, BEM-lite for component styles
- **Comments**: Descriptive section comments, JSDoc-style for algorithm functions
- **Priority order**: correctness > visual polish > performance > code quality
