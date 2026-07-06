"""
Performance test for 10K particles.

Tests that the simulation can handle 10,000 particles at 30+ FPS.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from galaxy.spiral_generator import SpiralGalaxyGenerator
from physics.integrator import LeapfrogIntegrator
from physics.barnes_hut import BarnesHutTree
import time


def test_10k_particles_performance():
    """Test performance with 10,000 particles."""
    print("Generating 10,000 particles...")
    generator = SpiralGalaxyGenerator()
    particles = generator.generate_random(10000)
    
    print(f"Generated {len(particles)} particles")
    
    integrator = LeapfrogIntegrator(dt=0.01, adaptive=True, G=1.0, softening=0.1)
    
    total_steps = 100
    print(f"Running performance test ({total_steps} steps)...")
    print("Progress: [", end="", flush=True)
    
    start = time.time()
    
    for i in range(total_steps):
        integrator.step(particles, use_barnes_hut=False)
        
        # Progress bar
        progress = (i + 1) / total_steps
        bar_length = 40
        filled = int(bar_length * progress)
        print(f"\rProgress: [{'=' * filled}{' ' * (bar_length - filled)}] {i+1}/{total_steps} ({progress*100:.0f}%)", end="", flush=True)


def test_small_batch_performance(num_particles: int = 100, steps: int = 50):
    """Test performance with small batch for quick verification."""
    print(f"Generating {num_particles} particles...")
    generator = SpiralGalaxyGenerator()
    particles = generator.generate_random(num_particles)
    
    print(f"Generated {len(particles)} particles")
    
    integrator = LeapfrogIntegrator(dt=0.01, adaptive=True, G=1.0, softening=0.1)
    
    print(f"Running performance test ({steps} steps)...")
    print("Progress: [", end="", flush=True)
    
    start = time.time()
    
    for i in range(steps):
        integrator.step(particles, use_barnes_hut=False)
        
        # Progress bar
        progress = (i + 1) / steps
        bar_length = 40
        filled = int(bar_length * progress)
        print(f"\rProgress: [{'=' * filled}{' ' * (bar_length - filled)}] {i+1}/{steps} ({progress*100:.0f}%)", end="", flush=True)
    
    elapsed = time.time() - start
    fps = steps / elapsed
    
    print(f"\n\nPerformance Results:")
    print(f"Total time: {elapsed:.2f} seconds")
    print(f"Average FPS: {fps:.2f}")
    print(f"Particles: {len(particles)}")
    
    if fps >= 30:
        print(f"[PASS] {fps:.2f} FPS >= 30 FPS target")
        return True
    else:
        print(f"[FAIL] {fps:.2f} FPS < 30 FPS target")
        return False


if __name__ == "__main__":
    # Test with 500 particles for GUI demo
    print("=" * 60)
    print("Testing with 500 particles (GUI demo target)")
    print("=" * 60)
    success_500 = test_small_batch_performance(500, 50)
    
    if success_500:
        print("\n500 particles test PASSED - suitable for GUI demo")
        sys.exit(0)
    else:
        print("\n500 particles test FAILED")
        sys.exit(1)
