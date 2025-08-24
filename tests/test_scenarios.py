"""
Tests for the core ChaosScenario classes.
"""

import pytest
from tohu.core import ChaosScenario, SimpleScenario
from tohu.scenarios import HallucinationScenario


def test_scenario_initialization():
    """Test that scenarios initialize with proper defaults."""
    scenario = SimpleScenario()

    # Check that name and description are set
    assert scenario.name == "Simple Example Scenario"
    assert "basic scenario" in scenario.description.lower()

    # Check empty config
    assert isinstance(scenario.config, dict)
    assert len(scenario.config) == 0


def test_custom_scenario_values():
    """Test that custom values are properly set."""
    custom_name = "My Custom Scenario"
    custom_description = "This is a custom test scenario"
    custom_config = {"param1": "value1", "param2": 42}

    scenario = SimpleScenario(
        name=custom_name,
        description=custom_description,
        config=custom_config
    )

    assert scenario.name == custom_name
    assert scenario.description == custom_description
    assert scenario.config == custom_config


def test_hallucination_scenario():
    """Test the hallucination scenario initialization."""
    scenario = HallucinationScenario()

    # Should have default test cases
    assert len(scenario.test_cases) > 0

    # Each test case should have the required fields
    for case in scenario.test_cases:
        assert "question" in case
        assert "misleading_context" in case
        assert "ground_truth" in case


def test_scenario_run_interface():
    """Test that scenarios follow the correct interface for results."""
    scenario = SimpleScenario()
    # We pass None as the target for this test
    results = scenario.run(None)

    # Check the basic structure of the results
    assert isinstance(results, dict)
    assert "success" in results
    assert "observations" in results
    assert "details" in results

    # Check the observations format
    assert isinstance(results["observations"], list)

    # Check the details format
    assert isinstance(results["details"], dict)
    assert "scenario_type" in results["details"]
    assert results["details"]["scenario_type"] == "SimpleScenario"
