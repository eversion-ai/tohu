"""
Tests for the core ChaosEngine class.
"""

import pytest
from tohu.core import ChaosEngine, SimpleScenario


def test_chaos_engine_initialization():
    """Test that the engine initializes properly."""
    engine = ChaosEngine()
    assert isinstance(engine, ChaosEngine)
    # Should have at least the built-in scenarios
    assert len(engine.scenarios) > 0
    assert "SimpleScenario" in engine.scenarios


def test_register_scenario():
    """Test that custom scenarios can be registered."""
    # Create a custom scenario for testing
    class CustomScenario(SimpleScenario):
        name = "Custom Test Scenario"

    engine = ChaosEngine()
    initial_count = len(engine.scenarios)

    # Register the custom scenario
    engine.register_scenario(CustomScenario)

    # Check that it was added
    assert len(engine.scenarios) == initial_count + 1
    assert "CustomScenario" in engine.scenarios

    # Check that we can retrieve it
    scenario_class = engine.scenarios["CustomScenario"]
    assert scenario_class == CustomScenario


def test_run_scenario():
    """Test running a basic scenario."""
    engine = ChaosEngine()

    # Run the simple scenario
    results = engine.run_scenario("SimpleScenario")

    # Check the results structure
    assert "scenario" in results
    assert "success" in results
    assert "observations" in results
    assert "details" in results

    # The simple scenario should succeed by default
    assert results["success"] is True


def test_list_scenarios():
    """Test listing available scenarios."""
    engine = ChaosEngine()
    scenarios = engine.list_scenarios()

    # Should return a list
    assert isinstance(scenarios, list)

    # Should include at least the built-in scenarios
    assert "SimpleScenario" in scenarios
    assert "NetworkLatencyScenario" in scenarios
