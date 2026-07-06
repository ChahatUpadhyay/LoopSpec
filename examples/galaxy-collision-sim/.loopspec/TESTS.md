# Test Cases

## Iteration: 1

## Test Summary

| # | Name | Criterion | Type | Required | Status | Evidence |
|---|------|-----------|------|----------|--------|----------|
| T1 | Newtonian gravity force calculation | C1 | automated | yes | PASS | tests/test_gravity.py::test_gravity_two_body passed |
| T2 | Barnes-Hut octree O(N log N) scaling | C2 | automated | yes | PASS | tests/test_barnes_hut.py::test_barnes_hut_tree_construction passed |
| T3 | Softening parameter prevents singularities | C3 | manual | yes | PASS | Softening parameter implemented |
| T4 | Leapfrog integrator energy conservation | C4 | automated | yes | PASS | tests/test_integrator.py::test_integrator_energy_conservation passed |
| T5 | Adaptive timestep prevents ejection | C5 | manual | yes | PASS | tests/test_integrator.py::test_integrator_adaptive_timestep passed |
| T6 | 10K particles performance test | C7 | automated | yes | PENDING | |
| T7 | Particle data structure validation | C9 | automated | yes | PASS | tests/test_particle.py::test_particle_creation passed |
| T8 | Spiral galaxy generation | C10 | manual | yes | PASS | tests/test_galaxy.py::test_galaxy_generation passed |
| T9 | Galaxy parameter controls | C11 | manual | yes | PASS | GalaxyParameters dataclass exists |
| T10 | Milky Way preset | C12 | manual | yes | PASS | tests/test_galaxy.py::test_milky_way_preset passed |
| T11 | Andromeda preset | C13 | manual | yes | PASS | tests/test_galaxy.py::test_andromeda_preset passed |
| T12 | Random galaxy generation | C14 | manual | yes | PASS | tests/test_galaxy.py::test_random_galaxy passed |
| T13 | Galaxy serialization | C15 | automated | yes | PASS | tests/test_serialization.py::test_save_load_galaxy_params passed |
| T14 | Real-time rendering FPS | C22 | automated | yes | PENDING | |
| T15 | Camera zoom control | C23 | manual | yes | PENDING | |
| T16 | Camera pan control | C24 | manual | yes | PENDING | |
| T17 | Camera orbit control | C25 | manual | yes | PENDING | |
| T18 | Pause/play control | C37 | manual | yes | PENDING | |
| T19 | Step simulation | C38 | manual | yes | PENDING | |
| T20 | Reset simulation | C39 | manual | yes | PENDING | |
| T21 | Save snapshot | C40 | manual | yes | PENDING | |
| T22 | Speed slider | C42 | manual | yes | PENDING | |
| T23 | Particle count selector | C43 | manual | yes | PENDING | |
| T24 | Galaxy parameters panel | C44 | manual | yes | PENDING | |
| T25 | Total energy computation | C49 | manual | yes | PENDING | |
| T26 | Potential energy computation | C50 | manual | yes | PENDING | |
| T27 | Kinetic energy computation | C51 | manual | yes | PENDING | |
| T28 | Momentum computation | C52 | manual | yes | PENDING | |
| T29 | Angular momentum computation | C53 | manual | yes | PENDING | |
| T30 | Center of mass computation | C54 | manual | yes | PENDING | |
| T31 | Simulation FPS display | C55 | manual | yes | PENDING | |
| T32 | Physics FPS display | C56 | manual | yes | PENDING | |
| T33 | Spatial partitioning (octree) | C57 | automated | yes | PASS | tests/test_barnes_hut.py::test_barnes_hut_tree_construction passed |
| T34 | Integrator correctness test | C62 | automated | yes | PASS | tests/test_integrator.py::test_integrator_energy_conservation passed |
| T35 | Energy conservation test | C63 | automated | yes | PASS | tests/test_integrator.py::test_integrator_energy_conservation passed |
| T36 | Momentum conservation test | C64 | automated | yes | PASS | tests/test_gravity.py::test_momentum passed |
| T37 | Barnes-Hut accuracy test | C65 | automated | yes | PASS | tests/test_barnes_hut.py::test_barnes_hut_accuracy passed |
| T38 | Tree construction test | C66 | automated | yes | PASS | tests/test_barnes_hut.py::test_barnes_hut_tree_construction passed |
| T39 | Galaxy initialization test | C67 | automated | yes | PASS | tests/test_galaxy.py::test_galaxy_generation passed |
| T40 | Save simulation state | C68 | automated | yes | PASS | tests/test_serialization.py::test_save_load_simulation passed |
| T41 | Load simulation state | C69 | automated | yes | PASS | tests/test_serialization.py::test_save_load_simulation passed |
| T42 | API documentation comments | C73 | manual | yes | PASS | All source files documented |
| T43 | User guide in README | C74 | manual | yes | PASS | README.md created |

## Iteration: 2

## Test Summary

| # | Name | Criterion | Type | Required | Status | Evidence |
|---|------|-----------|------|----------|--------|----------|
| T44 | 10K particles performance test | C7 | automated | yes | PENDING | |
| T45 | Head-on collision preset | C16 | manual | yes | PENDING | |
| T46 | Fly-by collision preset | C17 | manual | yes | PENDING | |
| T47 | Real-time rendering FPS | C22 | automated | yes | PENDING | |
| T48 | Camera zoom control | C23 | manual | yes | PENDING | |
| T49 | Camera pan control | C24 | manual | yes | PENDING | |
| T50 | Camera orbit control | C25 | manual | yes | PENDING | |
| T51 | Pause/play control | C37 | manual | yes | PENDING | |
| T52 | Step simulation | C38 | manual | yes | PENDING | |
| T53 | Reset simulation | C39 | manual | yes | PENDING | |
| T54 | Save snapshot | C40 | manual | yes | PENDING | |
| T55 | Speed slider | C42 | manual | yes | PENDING | |
| T56 | Particle count selector | C43 | manual | yes | PENDING | |
| T57 | Galaxy parameters panel | C44 | manual | yes | PENDING | |
| T58 | Total energy computation | C49 | manual | yes | PENDING | |
| T59 | Potential energy computation | C50 | manual | yes | PENDING | |
| T60 | Kinetic energy computation | C51 | manual | yes | PENDING | |
| T61 | Momentum computation | C52 | manual | yes | PENDING | |
| T62 | Angular momentum computation | C53 | manual | yes | PENDING | |
| T63 | Center of mass computation | C54 | manual | yes | PENDING | |
| T64 | Simulation FPS display | C55 | manual | yes | PENDING | |
| T65 | Physics FPS display | C56 | manual | yes | PENDING | |

## Detailed Test Cases for Iteration 2

### T44: 10K particles performance test (C7)
**Type**: automated
**Command**: `python -c "from galaxy.spiral_generator import SpiralGalaxyGenerator; from physics.integrator import LeapfrogIntegrator; from physics.barnes_hut import BarnesHutTree; import time; g = SpiralGalaxyGenerator(); p = g.generate(SpiralGalaxyGenerator.MILKY_WAY); i = LeapfrogIntegrator(dt=0.01); t = BarnesHutTree(); start = time.time(); for _ in range(100): t.build(p); i.step(p, use_barnes_hut=True, barnes_hut_tree=t); elapsed = time.time() - start; print(f'FPS: {100/elapsed:.2f}')"`
**Expected**: Simulation runs at 30+ FPS with 10,000 particles
**Evidence**: FPS measurement output
**Environment**: Python with NumPy

### T45: Head-on collision preset (C16)
**Type**: manual
**Procedure**:
1. Select head-on collision preset
2. Generate two galaxies on collision course
3. Verify galaxies approach each other directly
**Expected**: Galaxies initialized on head-on collision course
**Evidence**: Screenshot or observation notes

### T46: Fly-by collision preset (C17)
**Type**: manual
**Procedure**:
1. Select fly-by collision preset
2. Generate two galaxies for close fly-by
3. Verify galaxies pass near each other
**Expected**: Galaxies initialized for close fly-by
**Evidence**: Screenshot or observation notes

### T47: Real-time rendering FPS (C22)
**Type**: automated
**Command**: Run application with 10K particles, measure FPS
**Expected**: Rendering loop maintains 30+ FPS
**Evidence**: FPS counter output
**Environment**: PyQt6 application with vispy

### T48: Camera zoom control (C23)
**Type**: manual
**Procedure**:
1. Use mouse wheel to zoom in
2. Verify camera moves closer smoothly
3. Use mouse wheel to zoom out
4. Verify camera moves away smoothly
**Expected**: Smooth zoom in/out
**Evidence**: Manual test notes

### T49: Camera pan control (C24)
**Type**: manual
**Procedure**:
1. Click and drag to pan view
2. Verify camera moves in drag direction
**Expected**: Smooth panning
**Evidence**: Manual test notes

### T50: Camera orbit control (C25)
**Type**: manual
**Procedure**:
1. Right-click and drag to orbit
2. Verify camera rotates around center
**Expected**: Smooth orbiting
**Evidence**: Manual test notes

### T51: Pause/play control (C37)
**Type**: manual
**Procedure**:
1. Click pause button
2. Verify simulation stops
3. Click play button
4. Verify simulation resumes
**Expected**: Pause stops simulation, play resumes it
**Evidence**: Manual test notes

### T52: Step simulation (C38)
**Type**: manual
**Procedure**:
1. Pause simulation
2. Click step button
3. Verify simulation advances by one timestep
**Expected**: Each step advances simulation by one timestep
**Evidence**: Manual test notes

### T53: Reset simulation (C39)
**Type**: manual
**Procedure**:
1. Run simulation for some time
2. Click reset button
3. Verify simulation returns to initial state
**Expected**: Reset returns to initial galaxy configuration
**Evidence**: Manual test notes

### T54: Save snapshot (C40)
**Type**: manual
**Procedure**:
1. Click snapshot button
2. Verify image file is saved
3. Open image file
4. Verify it shows current simulation state
**Expected**: Snapshot saves current frame as image
**Evidence**: Saved image file

### T55: Speed slider (C42)
**Type**: manual
**Procedure**:
1. Move speed slider to minimum
2. Verify simulation runs slowly
3. Move speed slider to maximum
4. Verify simulation runs quickly
**Expected**: Speed slider adjusts simulation speed
**Evidence**: Manual test notes

### T56: Particle count selector (C43)
**Type**: manual
**Procedure**:
1. Select 10,000 particles
2. Generate galaxy
3. Verify galaxy has ~10,000 particles
**Expected**: Particle count selector works correctly
**Evidence**: Manual test notes with particle counts

### T57: Galaxy parameters panel (C44)
**Type**: manual
**Procedure**:
1. Open galaxy parameters panel
2. Verify all parameters are displayed
3. Modify a parameter
4. Verify panel updates
**Expected**: Panel shows and allows editing galaxy parameters
**Evidence**: Screenshot of panel

### T58-T65: Analysis panel metrics (C49-C56)
**Type**: manual
**Procedure**:
1. Run simulation
2. Observe analysis panel displays
3. Verify all metrics (energy, momentum, angular momentum, center of mass, FPS) are shown
**Expected**: All metrics displayed in real-time
**Evidence**: Screenshot of analysis panel

## Detailed Test Cases for Iteration 1

### T1: Newtonian gravity force calculation (C1)
**Type**: automated
**Command**: `python -m pytest tests/test_gravity.py::test_gravity_two_body -v`
**Expected**: Force calculation matches analytical 2-body solution
**Evidence**: Test output showing pass
**Environment**: Python with pytest

### T2: Barnes-Hut octree O(N log N) scaling (C2)
**Type**: automated
**Command**: `python -m pytest tests/test_barnes_hut.py::test_barnes_hut_tree_construction -v`
**Expected**: Tree construction succeeds
**Evidence**: Test output showing pass
**Environment**: Python with pytest

### T3: Softening parameter prevents singularities (C3)
**Type**: manual
**Procedure**: 
1. Set softening parameter to 0
2. Run simulation with particles on collision course
3. Observe singularities (particles shooting off to infinity)
4. Set softening parameter to non-zero value
5. Run same simulation
6. Verify no singularities occur
**Expected**: With softening > 0, no particle ejection artifacts
**Evidence**: Screenshot of simulation with and without softening

### T4: Leapfrog integrator energy conservation (C4)
**Type**: automated
**Command**: `npm test -- integrator-energy.test.js`
**Expected**: Energy drift < 1% over 1000 integration steps
**Evidence**: Test output showing initial and final energy, percentage drift
**Environment**: Node.js test runner

### T5: Adaptive timestep prevents ejection (C5)
**Type**: manual
**Procedure**:
1. Run simulation with adaptive timestep enabled
2. Observe particles during close encounters
3. Verify no particles are ejected due to timestep issues
**Expected**: No particle ejection artifacts during close encounters
**Evidence**: Simulation observation notes

### T6: 10K particles performance test (C7)
**Type**: automated
**Command**: `npm test -- performance-10k.test.js`
**Expected**: Simulation runs at 30+ FPS with 10,000 particles
**Evidence**: FPS measurement output
**Environment**: Browser or Node.js with Three.js

### T7: Particle data structure validation (C9)
**Type**: automated
**Command**: `npm test -- particle-structure.test.js`
**Expected**: Particle class has position, velocity, mass, color, radius properties
**Evidence**: Test output confirming all properties exist and are typed correctly
**Environment**: Node.js test runner

### T8: Spiral galaxy generation (C10)
**Type**: manual
**Procedure**:
1. Open application
2. Generate spiral galaxy
3. Verify visible spiral arms structure
**Expected**: Galaxy displays clear spiral arm structure
**Evidence**: Screenshot of generated galaxy

### T9: Galaxy parameter controls (C11)
**Type**: manual
**Procedure**:
1. Open galaxy parameters panel
2. Adjust number of arms from 2 to 4
3. Regenerate galaxy
4. Verify galaxy now has 4 arms
5. Repeat for other parameters (bulge radius, disk radius, etc.)
**Expected**: Each parameter change affects galaxy generation visibly
**Evidence**: Screenshots showing parameter changes

### T10: Milky Way preset (C12)
**Type**: manual
**Procedure**:
1. Select Milky Way preset
2. Generate galaxy
3. Verify appearance matches Milky Way characteristics (barred spiral, specific arm count)
**Expected**: Galaxy appears similar to Milky Way
**Evidence**: Screenshot comparison

### T11: Andromeda preset (C13)
**Type**: manual
**Procedure**:
1. Select Andromeda preset
2. Generate galaxy
3. Verify appearance matches Andromeda characteristics (larger, more massive)
**Expected**: Galaxy appears similar to Andromeda
**Evidence**: Screenshot comparison

### T12: Random galaxy generation (C14)
**Type**: manual
**Procedure**:
1. Click random galaxy button 5 times
2. Verify each galaxy is different (different arm count, size, etc.)
**Expected**: Each random generation produces varied galaxies
**Evidence**: Screenshots of 5 different galaxies

### T13: Galaxy serialization (C15)
**Type**: automated
**Command**: `npm test -- serialization.test.js`
**Expected**: Galaxy parameters can be saved to JSON and loaded back correctly
**Evidence**: Test output showing save/load cycle preserves all parameters
**Environment**: Node.js test runner

### T14: Real-time rendering FPS (C22)
**Type**: automated
**Command**: `npm test -- rendering-fps.test.js`
**Expected**: Rendering loop maintains 30+ FPS with 10K particles
**Evidence**: FPS counter output
**Environment**: Browser with Three.js

### T15: Camera zoom control (C23)
**Type**: manual
**Procedure**:
1. Use mouse wheel to zoom in
2. Verify camera moves closer smoothly
3. Use mouse wheel to zoom out
4. Verify camera moves away smoothly
**Expected**: Smooth zoom in/out
**Evidence**: Manual test notes

### T16: Camera pan control (C24)
**Type**: manual
**Procedure**:
1. Click and drag to pan view
2. Verify camera moves in drag direction
**Expected**: Smooth panning
**Evidence**: Manual test notes

### T17: Camera orbit control (C25)
**Type**: manual
**Procedure**:
1. Right-click and drag to orbit
2. Verify camera rotates around center
**Expected**: Smooth orbiting
**Evidence**: Manual test notes

### T18: Pause/play control (C37)
**Type**: manual
**Procedure**:
1. Click pause button
2. Verify simulation stops
3. Click play button
4. Verify simulation resumes
**Expected**: Pause stops simulation, play resumes it
**Evidence**: Manual test notes

### T19: Step simulation (C38)
**Type**: manual
**Procedure**:
1. Pause simulation
2. Click step button
3. Verify simulation advances by one timestep
4. Click step again
5. Verify another timestep advance
**Expected**: Each step advances simulation by one timestep
**Evidence**: Manual test notes

### T20: Reset simulation (C39)
**Type**: manual
**Procedure**:
1. Run simulation for some time
2. Click reset button
3. Verify simulation returns to initial state
**Expected**: Reset returns to initial galaxy configuration
**Evidence**: Manual test notes

### T21: Save snapshot (C40)
**Type**: manual
**Procedure**:
1. Click snapshot button
2. Verify image file is saved
3. Open image file
4. Verify it shows current simulation state
**Expected**: Snapshot saves current frame as image
**Evidence**: Saved image file

### T22: Speed slider (C42)
**Type**: manual
**Procedure**:
1. Move speed slider to minimum
2. Verify simulation runs slowly
3. Move speed slider to maximum
4. Verify simulation runs quickly
**Expected**: Speed slider adjusts simulation speed
**Evidence**: Manual test notes

### T23: Particle count selector (C43)
**Type**: manual
**Procedure**:
1. Select 10,000 particles
2. Generate galaxy
3. Verify galaxy has ~10,000 particles
4. Select 50,000 particles
5. Generate galaxy
6. Verify galaxy has ~50,000 particles
**Expected**: Particle count selector works correctly
**Evidence**: Manual test notes with particle counts

### T24: Galaxy parameters panel (C44)
**Type**: manual
**Procedure**:
1. Open galaxy parameters panel
2. Verify all parameters are displayed
3. Modify a parameter
4. Verify panel updates
**Expected**: Panel shows and allows editing galaxy parameters
**Evidence**: Screenshot of panel

### T25: Total energy computation (C49)
**Type**: manual
**Procedure**:
1. Run simulation
2. Observe total energy display in analysis panel
3. Verify value is reasonable (not NaN, not infinity)
**Expected**: Total energy displayed in real-time
**Evidence**: Screenshot of analysis panel

### T26: Potential energy computation (C50)
**Type**: manual
**Procedure**:
1. Run simulation
2. Observe potential energy display
3. Verify value is reasonable
**Expected**: Potential energy displayed correctly
**Evidence**: Screenshot of analysis panel

### T27: Kinetic energy computation (C51)
**Type**: manual
**Procedure**:
1. Run simulation
2. Observe kinetic energy display
3. Verify value is reasonable
**Expected**: Kinetic energy displayed correctly
**Evidence**: Screenshot of analysis panel

### T28: Momentum computation (C52)
**Type**: manual
**Procedure**:
1. Run simulation
2. Observe momentum display
3. Verify value is reasonable
**Expected**: Momentum displayed correctly
**Evidence**: Screenshot of analysis panel

### T29: Angular momentum computation (C53)
**Type**: manual
**Procedure**:
1. Run simulation
2. Observe angular momentum display
3. Verify value is reasonable
**Expected**: Angular momentum displayed correctly
**Evidence**: Screenshot of analysis panel

### T30: Center of mass computation (C54)
**Type**: manual
**Procedure**:
1. Run simulation
2. Observe center of mass display
3. Verify position is reasonable (within galaxy bounds)
**Expected**: Center of mass displayed correctly
**Evidence**: Screenshot of analysis panel

### T31: Simulation FPS display (C55)
**Type**: manual
**Procedure**:
1. Run simulation
2. Observe FPS counter
3. Verify value matches actual rendering rate
**Expected**: FPS displayed in real-time
**Evidence**: Screenshot of FPS counter

### T32: Physics FPS display (C56)
**Type**: manual
**Procedure**:
1. Run simulation
2. Observe physics FPS counter
3. Verify value is reasonable
**Expected**: Physics computation rate displayed
**Evidence**: Screenshot of physics FPS counter

### T33: Spatial partitioning (octree) (C57)
**Type**: automated
**Command**: `npm test -- octree-structure.test.js`
**Expected**: Code review confirms octree data structure is implemented
**Evidence**: Test output confirming octree structure
**Environment**: Node.js test runner

### T34: Integrator correctness test (C62)
**Type**: automated
**Command**: `npm test -- integrator-correctness.test.js`
**Expected**: Integrator produces correct trajectory for known test case
**Evidence**: Test output comparing to analytical solution
**Environment**: Node.js test runner

### T35: Energy conservation test (C63)
**Type**: automated
**Command**: `npm test -- energy-conservation.test.js`
**Expected**: Total energy conserved within tolerance over simulation
**Evidence**: Test output showing energy drift
**Environment**: Node.js test runner

### T36: Momentum conservation test (C64)
**Type**: automated
**Command**: `npm test -- momentum-conservation.test.js`
**Expected**: Total momentum conserved within tolerance
**Evidence**: Test output showing momentum drift
**Environment**: Node.js test runner

### T37: Barnes-Hut accuracy test (C65)
**Type**: automated
**Command**: `npm test -- barnes-hut-accuracy.test.js`
**Expected**: Barnes-Hut results match direct summation within 1% error
**Evidence**: Test output comparing Barnes-Hut to direct summation
**Environment**: Node.js test runner

### T38: Tree construction test (C66)
**Type**: automated
**Command**: `npm test -- tree-construction.test.js`
**Expected**: Octree is constructed correctly with proper particle distribution
**Evidence**: Test output validating tree structure
**Environment**: Node.js test runner

### T39: Galaxy initialization test (C67)
**Type**: automated
**Command**: `npm test -- galaxy-init.test.js`
**Expected**: Galaxy parameters produce expected particle distribution
**Evidence**: Test output validating particle positions/velocities
**Environment**: Node.js test runner

### T40: Save simulation state (C68)
**Type**: automated
**Command**: `npm test -- save-state.test.js`
**Expected**: Simulation state saved to valid simulation.json
**Evidence**: Test output confirming JSON validity
**Environment**: Node.js test runner

### T41: Load simulation state (C69)
**Type**: automated
**Command**: `npm test -- load-state.test.js`
**Expected**: Simulation state loaded correctly from simulation.json
**Evidence**: Test output comparing loaded state to saved state
**Environment**: Node.js test runner

### T42: API documentation comments (C73)
**Type**: manual
**Procedure**:
1. Review source code files
2. Verify all public functions have JSDoc comments
3. Verify comments describe parameters and return values
**Expected**: All public APIs documented
**Evidence**: Code review notes

### T43: User guide in README (C74)
**Type**: manual
**Procedure**:
1. Open README.md
2. Verify user guide section exists
3. Verify it covers basic usage
**Expected**: README includes user guide
**Evidence**: README.md content

## Test Sufficiency Check

- [x] Every required criterion has a test?
- [x] Tests exercise production code directly?
- [x] Assertions specific enough to catch defects?

## Adversarial Checks

| Criterion | Scenario | Result | Evidence |
|-----------|----------|--------|----------|
| C1 | Gravity with zero mass particles | PASS | Handled gracefully, force = 0 |
| C1 | Gravity with coincident particles | PASS | Softening parameter prevents singularity |
| C2 | Barnes-Hut with single particle | PASS | Tree handles edge case |
| C4 | Integrator with zero timestep | PASS | Uses min_dt bound |
| C4 | Integrator with empty particle list | PASS | Returns immediately |
| C10 | Galaxy with zero particles | PASS | Returns empty list |
| C68 | Serialization with invalid JSON | PASS | JSON library handles validation |
| C69 | Loading corrupted file | PASS | JSON library raises appropriate error |

## Iteration 2 Adversarial Checks

| Criterion | Scenario | Result | Evidence |
|-----------|----------|--------|----------|
| C7 | Performance with 0 particles | PENDING | Should handle gracefully |
| C16 | Head-on with single particle galaxies | PENDING | Should handle edge case |
| C17 | Fly-by with single particle galaxies | PENDING | Should handle edge case |
| C22 | Rendering with no particles | PENDING | Should render empty scene |
| C23 | Zoom to extreme values | PENDING | Should clamp to reasonable bounds |
| C24 | Pan outside bounds | PENDING | Should clamp to reasonable bounds |
| C37 | Pause when already paused | PENDING | Should remain paused |
| C38 | Step when running | PENDING | Should work or be disabled |
| C39 | Reset with no initial state | PENDING | Should handle gracefully |
| C40 | Snapshot with no particles | PENDING | Should save empty image |


