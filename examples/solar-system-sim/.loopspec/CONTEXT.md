# Project Context

<!--
  MODEL: Fill this during Phase 1 (ANALYZE).
  Strategy: Broad scan, narrow record.
  - Scan everything to understand the full picture
  - Record only what's relevant to the goal
  - Be specific and accurate — no guessing
  - Include actual evidence (commands run + output) for baseline
-->

## Tech Stack

- **Language**: HTML5, CSS3, JavaScript (ES6+)
- **3D Graphics Library**: Three.js (loaded from CDN)
- **Build Tools**: None (single HTML file, no bundlers)
- **Runtime**: Modern web browsers (Chrome 120+, Firefox 120+, Edge 120+)
- **Deployment**: Static file serving (no server required)

## Project Structure

```
solar-system-sim/
├── .loopspec/           # LoopSpec protocol files
│   ├── PROTOCOL.md      # Operating manual (read-only)
│   ├── GOAL.md          # Goal and success criteria (read-only)
│   ├── CONTEXT.md       # This file - project analysis
│   ├── PLAN.md          # Implementation plan
│   ├── TESTS.md         # Test cases and evidence
│   ├── CHANGELOG.md     # Change log
│   ├── LEARNINGS.md     # Mistakes and fixes
│   ├── QUESTIONS.md     # Human questions
│   ├── STATUS.md        # Current phase and status
│   ├── STATUS.json      # Machine-readable status
│   └── iterations/      # Archive snapshots
└── index.html           # Single HTML file (to be created)
```
## Architecture Overview

The Solar System Simulator will be a single-page 3D application with the following architecture:

1. **Scene Setup**: Three.js scene, camera, renderer, and lighting
2. **Celestial Bodies**: 
   - Sun (central light source with glow effect)
   - 8 Planets (Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune)
   - Moon (orbiting Earth)
   - Asteroid belt (particle system between Mars and Jupiter)
3. **Orbital Mechanics**: Kepler's laws implementation for realistic orbital motion
4. **Camera Controls**: OrbitControls for user interaction (zoom, pan, rotate)
5. **Time Controls**: Pause/play, speed adjustment, reverse time
6. **UI Elements**: 
   - FPS counter
   - Planet information panels
   - Control buttons
7. **Orbital Trails**: Line objects showing planetary paths
8. **Event Handling**: Keyboard shortcuts, window resize, user interactions

Data Flow:
- User input (keyboard/mouse) → Event handlers → State updates → Animation loop → Scene rendering
- Time system → Orbital calculations → Position updates → Visual updates

## Key Files & Their Roles

| File | Role | Relevant to Criteria |
|------|------|---------------------|
| `index.html` (to be created) | Single file containing all HTML, CSS, and JavaScript | All criteria (C1-C20) |

## Dependencies

- **Three.js**: Loaded from CDN (unpkg.com or cdnjs)
  - Core 3D rendering engine
  - OrbitControls for camera manipulation
  - No other external dependencies

## Existing Tests

No existing tests. This is a greenfield project. Tests will be designed in Phase 3 (TEST DESIGN).

## Baseline State

**Current State**: Empty project directory with only LoopSpec protocol files.

**Evidence**:
```bash
$ dir solar-system-sim
 Directory: C:\Users\chaha\Documents\Codex\2026-06-28\e\LoopSpec\examples\solar-system-sim

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----        02-07-2026     22:17                .loopspec
```

No index.html file exists yet. No code has been written.

Current state:
- Working: LoopSpec protocol files initialized
- Broken: No implementation exists
- Evidence: Directory listing shows only .loopspec folder

## Available Runtimes

- **Operating System**: Windows
- **Web Browsers**: Chrome 120+, Firefox 120+, Edge 120+ (as specified in constraints)
- **Node.js**: Not required (pure client-side)
- **Package Managers**: Not used (no npm, yarn, etc.)
- **Build Tools**: Not used (no webpack, vite, etc.)

## Patterns & Conventions

- **Single File Architecture**: All code in one HTML file for simplicity
- **Procedural Generation**: No external assets - all visuals generated programmatically
- **Component-Based**: Each celestial body as a separate object/function
- **State Management**: Central state object for time, camera, and simulation parameters
- **Event-Driven**: User interactions trigger state changes
- **Performance-First**: Optimized for 60fps on modern hardware
- **Naming Conventions**: camelCase for JavaScript, kebab-case for CSS classes

## Technical Constraints

- File size must stay under 100KB (excluding Three.js CDN)
- No external assets (textures, models) - procedural generation only
- No server-side code - pure client-side
- Must work offline after initial Three.js cache
- Responsive design for different screen sizes
- No console errors on load
- 60fps performance target on modern hardware

## Success Criteria Summary

20 criteria covering:
- File structure (C1, C18)
- Three.js integration (C2)
- Celestial bodies (C3, C4, C11, C12, C17)
- Orbital mechanics (C5, C6, C7, C10)
- User controls (C8, C9, C15, C16)
- Information display (C13, C14)
- Quality assurance (C19, C20)
