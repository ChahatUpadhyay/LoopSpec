"""Unit tests for latency simulation."""

import pytest
from simulation.latency import LatencySimulator, LatencyProfile


def test_network_delay():
    """Test T18: Network Delay Simulation"""
    sim = LatencySimulator(seed=42)
    profile = LatencyProfile(network_delay_ms=10.0)
    sim.set_profile("agent1", profile)
    
    submission_time = 0.0
    adjusted_time = sim.apply_network_delay("agent1", submission_time)
    
    # Should be delayed by approximately 10ms
    assert adjusted_time >= submission_time + 0.005  # Allow for stochastic variation
    assert adjusted_time <= submission_time + 0.020


def test_execution_delay():
    """Test T19: Execution Delay Simulation"""
    sim = LatencySimulator(seed=42)
    profile = LatencyProfile(execution_delay_ms=5.0)
    sim.set_profile("agent1", profile)
    
    receipt_time = 0.0
    adjusted_time = sim.apply_execution_delay("agent1", receipt_time)
    
    # Should be delayed by approximately 5ms
    assert adjusted_time >= receipt_time + 0.002
    assert adjusted_time <= receipt_time + 0.010


def test_cancellation_delay():
    """Test T20: Cancellation Delay Simulation"""
    sim = LatencySimulator(seed=42)
    profile = LatencyProfile(cancellation_delay_ms=3.0)
    sim.set_profile("agent1", profile)
    
    submission_time = 0.0
    adjusted_time = sim.apply_cancellation_delay("agent1", submission_time)
    
    # Should be delayed by approximately 3ms
    assert adjusted_time >= submission_time + 0.001
    assert adjusted_time <= submission_time + 0.008


def test_latency_model():
    """Test T35: Latency Model Works"""
    sim = LatencySimulator(seed=42)
    
    # With significant latency
    profile = LatencyProfile(network_delay_ms=50.0, execution_delay_ms=25.0)
    sim.set_profile("agent1", profile)
    
    submission_time = 0.0
    with_latency = sim.apply_network_delay("agent1", submission_time)
    with_latency = sim.apply_execution_delay("agent1", with_latency)
    
    # Without latency (default profile)
    no_latency = sim.apply_network_delay("agent2", submission_time)
    no_latency = sim.apply_execution_delay("agent2", no_latency)
    
    # With latency should be slower (allowing for stochastic variation)
    assert with_latency > no_latency + 0.01  # At least 10ms difference
