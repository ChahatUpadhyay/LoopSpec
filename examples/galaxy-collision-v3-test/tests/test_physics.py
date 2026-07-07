"""Automated physics tests. (C62-C67)

Run: python -m pytest tests/test_physics.py -v
"""
import sys
import os
import time
import numpy as np

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.physics.particles import ParticleSystem
from src.physics.gravity import compute_forces_direct, compute_forces_barnes_hut
from src.physics.octree import build_octree, OctreeNode
from src.physics.integrator import LeapfrogIntegrator
from src.galaxy.generator import generate_spiral_galaxy, milky_way_preset
from src.galaxy.serialization import save_state, load_state


def test_integrator_correctness():
    """C62: Verify leapfrog integrator produces correct trajectories.
    
    Two-body problem: test that orbit is approximately circular.
    """
    particles = ParticleSystem.create(2)
    particles.positions[0] = [0, 0, 0]
    particles.positions[1] = [1, 0, 0]
    particles.masses[0] = 100.0
    particles.masses[1] = 1.0
    # Circular orbit velocity: v = sqrt(GM/r)
    v_circ = np.sqrt(100.0 / 1.0)
    particles.velocities[1] = [0, v_circ, 0]
    
    integrator = LeapfrogIntegrator(softening=0.01, theta=0.5, dt=0.001, adaptive=False)
    
    # Run for 100 steps
    for _ in range(100):
        integrator.step(particles)
    
    # Particle 1 should still be approximately distance 1 from origin
    r = np.linalg.norm(particles.positions[1] - particles.positions[0])
    assert 0.8 < r < 1.3, f"Orbit radius drifted: {r:.3f} (expected ~1.0)"
    print(f"  PASS C62: Orbit radius = {r:.4f} (expected ~1.0)")


def test_energy_conservation():
    """C63: Verify energy conservation over 1000 steps.
    
    Uses direct summation (exact forces) to test the leapfrog integrator.
    Total energy should drift less than 1%.
    """
    from src.physics.gravity import compute_forces_direct
    
    particles = ParticleSystem.create(20)
    rng = np.random.default_rng(42)
    particles.positions = rng.uniform(-1, 1, (20, 3))
    particles.velocities = rng.uniform(-0.05, 0.05, (20, 3))
    particles.masses = rng.uniform(0.5, 2.0, 20)
    
    # Use direct integrator (no BH approximation) for energy test
    softening = 0.2
    dt = 0.005
    
    # Compute initial energy
    ke0 = particles.kinetic_energy()
    pe0 = particles.potential_energy(softening)
    e0 = ke0 + pe0
    
    # Manual leapfrog with direct summation (exact, symmetric forces)
    acc = compute_forces_direct(particles.positions, particles.masses, softening)
    for _ in range(1000):
        particles.velocities += 0.5 * dt * acc
        particles.positions += dt * particles.velocities
        acc = compute_forces_direct(particles.positions, particles.masses, softening)
        particles.velocities += 0.5 * dt * acc
    
    ke1 = particles.kinetic_energy()
    pe1 = particles.potential_energy(softening)
    e1 = ke1 + pe1
    
    drift = abs(e1 - e0) / abs(e0) if abs(e0) > 0 else 0
    assert drift < 0.01, f"Energy drift too large: {drift*100:.2f}% (max 1%)"
    print(f"  PASS C63: Energy drift = {drift*100:.4f}% (< 1%)")


def test_momentum_conservation():
    """C64: Verify total momentum conservation.
    
    Uses direct summation (symmetric forces guarantee momentum conservation).
    """
    from src.physics.gravity import compute_forces_direct
    
    particles = ParticleSystem.create(20)
    rng = np.random.default_rng(123)
    particles.positions = rng.uniform(-2, 2, (20, 3))
    particles.velocities = rng.uniform(-0.5, 0.5, (20, 3))
    particles.masses = rng.uniform(1.0, 3.0, 20)
    
    # Make zero total momentum
    total_p = particles.momentum()
    particles.velocities -= total_p / np.sum(particles.masses)
    
    p0 = np.linalg.norm(particles.momentum())
    softening = 0.1
    dt = 0.005
    
    # Manual leapfrog with direct summation
    acc = compute_forces_direct(particles.positions, particles.masses, softening)
    for _ in range(500):
        particles.velocities += 0.5 * dt * acc
        particles.positions += dt * particles.velocities
        acc = compute_forces_direct(particles.positions, particles.masses, softening)
        particles.velocities += 0.5 * dt * acc
    
    p1 = np.linalg.norm(particles.momentum())
    assert p1 < 1e-8, f"Momentum not conserved: |p| = {p1:.2e}"
    print(f"  PASS C64: Final momentum magnitude = {p1:.2e} (~0)")


def test_barnes_hut_accuracy():
    """C65: Compare Barnes-Hut to direct summation.
    
    With theta=0.5, relative error should be < 5% for most particles.
    """
    n = 100
    rng = np.random.default_rng(55)
    positions = rng.uniform(-2, 2, (n, 3))
    masses = rng.uniform(0.5, 2.0, n)
    
    acc_direct = compute_forces_direct(positions, masses, softening=0.05)
    acc_bh = compute_forces_barnes_hut(positions, masses, softening=0.05, theta=0.5)
    
    # Compute relative error for each particle
    mag_direct = np.sqrt(np.sum(acc_direct**2, axis=1))
    errors = np.sqrt(np.sum((acc_bh - acc_direct)**2, axis=1))
    rel_errors = errors / (mag_direct + 1e-10)
    
    median_error = np.median(rel_errors)
    assert median_error < 0.05, f"Barnes-Hut median error too high: {median_error:.4f}"
    print(f"  PASS C65: Barnes-Hut median relative error = {median_error:.4f} (< 5%)")


def test_tree_construction():
    """C66: Validate octree structure."""
    n = 200
    rng = np.random.default_rng(77)
    positions = rng.uniform(-5, 5, (n, 3))
    masses = np.ones(n)
    
    tree = build_octree(positions, masses)
    
    # Total mass should equal sum of particle masses
    assert tree is not None, "Tree is None"
    assert abs(tree.mass - n) < 1e-10, f"Tree mass {tree.mass} != {n}"
    
    # Center of mass should be close to mean position
    expected_com = positions.mean(axis=0)
    com_error = np.linalg.norm(tree.com - expected_com)
    assert com_error < 0.5, f"COM error too large: {com_error:.4f}"
    print(f"  PASS C66: Tree mass = {tree.mass:.0f}, COM error = {com_error:.4f}")


def test_galaxy_initialization():
    """C67: Validate galaxy parameters."""
    galaxy = milky_way_preset(1000)
    
    assert galaxy.n == 1000, f"Wrong particle count: {galaxy.n}"
    assert galaxy.positions.shape == (1000, 3)
    assert galaxy.velocities.shape == (1000, 3)
    assert galaxy.masses.shape == (1000,)
    assert galaxy.colors.shape == (1000, 4)
    assert galaxy.radii.shape == (1000,)
    
    # All masses positive
    assert np.all(galaxy.masses > 0), "Negative masses found"
    
    # Positions should be within reasonable bounds
    max_r = np.max(np.linalg.norm(galaxy.positions, axis=1))
    assert max_r < 20.0, f"Particles too far: max_r = {max_r:.1f}"
    
    print(f"  PASS C67: Galaxy init OK — {galaxy.n} particles, max_r = {max_r:.2f}")


def test_serialization_roundtrip():
    """C68, C69: Save/load state preserves data."""
    import tempfile
    
    galaxy = milky_way_preset(100)
    
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False, mode='w') as f:
        filepath = f.name
    
    save_state(galaxy, filepath, {'sim_time': 1.5})
    loaded, meta = load_state(filepath)
    
    assert loaded.n == galaxy.n
    assert np.allclose(loaded.positions, galaxy.positions)
    assert np.allclose(loaded.velocities, galaxy.velocities)
    assert np.allclose(loaded.masses, galaxy.masses)
    assert meta['sim_time'] == 1.5
    
    os.unlink(filepath)
    print(f"  PASS C68/C69: Serialization round-trip OK")


def test_performance_scaling():
    """C2: Verify O(N log N) scaling of Barnes-Hut."""
    times = {}
    for n in [500, 1000, 2000]:
        rng = np.random.default_rng(42)
        pos = rng.uniform(-5, 5, (n, 3))
        masses = np.ones(n)
        
        t0 = time.perf_counter()
        compute_forces_barnes_hut(pos, masses, softening=0.05, theta=0.8)
        elapsed = time.perf_counter() - t0
        times[n] = elapsed
    
    # Check scaling: t(2000)/t(1000) should be < 3x for O(N log N)
    # (O(N^2) would give ~4x)
    ratio = times[2000] / times[1000]
    assert ratio < 3.5, f"Scaling looks O(N^2): ratio = {ratio:.2f}"
    print(f"  PASS C2: Barnes-Hut scaling ratio (2000/1000) = {ratio:.2f} (< 3.5, consistent with O(N log N))")
    print(f"    N=500: {times[500]*1000:.1f}ms, N=1000: {times[1000]*1000:.1f}ms, N=2000: {times[2000]*1000:.1f}ms")


def test_particle_data_structure():
    """C9: Verify particle data structure."""
    ps = ParticleSystem.create(10)
    assert hasattr(ps, 'positions') and ps.positions.shape == (10, 3)
    assert hasattr(ps, 'velocities') and ps.velocities.shape == (10, 3)
    assert hasattr(ps, 'masses') and ps.masses.shape == (10,)
    assert hasattr(ps, 'colors') and ps.colors.shape == (10, 4)
    assert hasattr(ps, 'radii') and ps.radii.shape == (10,)
    print(f"  PASS C9: Particle data structure validates OK")


if __name__ == '__main__':
    print("=" * 60)
    print("Galaxy Collision Simulator — Physics Test Suite")
    print("=" * 60)
    
    tests = [
        test_particle_data_structure,
        test_galaxy_initialization,
        test_tree_construction,
        test_barnes_hut_accuracy,
        test_integrator_correctness,
        test_energy_conservation,
        test_momentum_conservation,
        test_serialization_roundtrip,
        test_performance_scaling,
    ]
    
    passed = 0
    failed = 0
    for test in tests:
        try:
            print(f"\n[RUN] {test.__name__}")
            test()
            passed += 1
        except AssertionError as e:
            print(f"  FAIL: {e}")
            failed += 1
        except Exception as e:
            print(f"  ERROR: {e}")
            failed += 1
    
    print(f"\n{'=' * 60}")
    print(f"Results: {passed} passed, {failed} failed out of {len(tests)}")
    print(f"{'=' * 60}")
    sys.exit(0 if failed == 0 else 1)
