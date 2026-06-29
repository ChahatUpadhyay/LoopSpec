# 🎯 Goal

Build a **premium, interactive sorting algorithm visualizer** as a single-page web application using vanilla HTML, CSS, and JavaScript. The app must visually demonstrate how different sorting algorithms work in real-time with animated bar charts, controls for speed/array-size, step-by-step mode, algorithm comparison mode, and a statistics dashboard — all with a polished, dark-themed glassmorphism UI.

## Success Criteria

- [ ] Criterion 1: App renders an array of colored bars representing values, with heights proportional to value
- [ ] Criterion 2: Implements at least 4 sorting algorithms: Bubble Sort, Quick Sort, Merge Sort, and Insertion Sort
- [ ] Criterion 3: Sorting is animated in real-time — bars swap/move with smooth CSS transitions, active comparisons highlighted in a distinct color, sorted elements highlighted in green
- [ ] Criterion 4: User can control: array size (10-100 via slider), animation speed (slow/medium/fast), and generate a new random array
- [ ] Criterion 5: Step-by-step mode: user can click "Next Step" to advance one comparison at a time, showing which elements are being compared
- [ ] Criterion 6: Algorithm comparison mode: run 2 algorithms side-by-side simultaneously on identical arrays
- [ ] Criterion 7: Statistics panel displays: number of comparisons, number of swaps, time elapsed, and time complexity (Big-O) for the selected algorithm
- [ ] Criterion 8: Responsive design — works on desktop (1920px) down to mobile (375px) without horizontal scroll
- [ ] Criterion 9: Dark theme with glassmorphism cards, smooth gradients, micro-animations on hover for buttons, and a professional color palette (no plain primary colors)
- [ ] Criterion 10: All sorting algorithms produce a correctly sorted array (ascending order) — verified by automated test
- [ ] Criterion 11: App loads with no console errors
- [ ] Criterion 12: Code is clean, well-commented, and uses ES6+ features (const/let, arrow functions, template literals, async/await)

## Permissions

- [x] Read all project files
- [x] Create new files
- [x] Modify existing files
- [ ] Delete files
- [x] Execute shell commands
- [x] Run tests
- [ ] Git operations (commit, branch, push)
- [ ] Install dependencies (npm, pip, cargo, etc.)
- [ ] Access network / external APIs
- [x] Modify configuration files
- [ ] Modify database schemas

## Constraints

- No frameworks or libraries — vanilla HTML, CSS, JS only
- No CDNs or external resources — fully self-contained
- Single `index.html`, `style.css`, and `app.js` file structure (plus an optional `test.html`)
- Must work in modern browsers (Chrome, Firefox, Edge — no IE11)
- No build tools required — open index.html directly in browser

## Priority

correctness > visual polish > performance > code quality

## Max Iterations

max_iterations: 5

## Additional Context

This is a dogfood test of the LoopSpec protocol. All phases should be followed strictly.
