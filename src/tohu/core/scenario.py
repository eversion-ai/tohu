"""
Core scenario classes for Tohu chaos testing.

This module defines the base ChaosScenario class that all scenarios
should inherit from, as well as a simple example scenario.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union


@dataclass
class ChaosScenario(ABC):
    """
    Abstract base class for all chaos scenarios.

    A chaos scenario defines a specific test case or failure mode
    to be applied to an AI agent or system to test its robustness.

    Attributes:
        name: Human-readable name for the scenario
        description: Detailed description of what the scenario tests
        config: Configuration parameters for the scenario
    """

    name: str = field(default="")
    description: str = field(default="")
    config: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Set default name and description if not provided."""
        if not self.name:
            self.name = self.__class__.__name__
        if not self.description:
            self.description = self.__doc__ or "No description provided."

    @abstractmethod
    def run(self, target: Any) -> Dict[str, Any]:
        """
        Execute the scenario against the target system.

        Args:
            target: The target system or agent to test

        Returns:
            A dictionary containing the results and observations
        """
        pass

    def setup(self) -> None:
        """
        Perform any necessary setup before running the scenario.

        This method can be overridden by subclasses to perform
        initialization steps before the scenario runs.
        """
        pass

    def teardown(self) -> None:
        """
        Perform any necessary cleanup after running the scenario.

        This method can be overridden by subclasses to perform
        cleanup steps after the scenario runs.
        """
        pass


@dataclass
class SimpleScenario(ChaosScenario):
    """
    A simple example scenario that can be used as a template.

    This scenario demonstrates the basic structure of a chaos test
    and can be used as a starting point for developing custom scenarios.
    """

    name: str = "Simple Example Scenario"
    description: str = "A basic scenario that serves as an example template."
    expected_response: Optional[str] = None

    def run(self, target: Any) -> Dict[str, Any]:
        """
        Execute a simple test against the target.

        This implementation simply sends a test prompt to the
        target and validates the response.

        Args:
            target: The target system or agent to test

        Returns:
            A dictionary containing test results
        """
        self.setup()

        # This is a placeholder implementation
        # In a real scenario, you would:
        # 1. Apply some form of "chaos" to the target
        # 2. Observe how it responds
        # 3. Record and return the results

        results = {
            "success": True,  # Placeholder
            "observations": [
                "This is a placeholder observation."
            ],
            "details": {
                "scenario_type": self.__class__.__name__,
                "config": self.config,
                # Add more detailed results here
            }
        }

        self.teardown()
        return results


# Example of a more specific scenario (not fully implemented)
@dataclass
class NetworkLatencyScenario(ChaosScenario):
    """
    Simulates network latency when an AI agent makes external API calls.

    This scenario intercepts network requests and adds artificial delay
    to test how the agent handles slow responses.
    """

    name: str = "Network Latency Test"
    description: str = "Tests how an agent handles delayed API responses."
    latency_ms: int = 2000  # Default 2-second delay

    def run(self, target: Any) -> Dict[str, Any]:
        """
        Execute the network latency scenario.

        Args:
            target: The target system or agent to test

        Returns:
            A dictionary containing test results
        """
        self.setup()

        # TODO: Implement actual latency injection
        # This would involve:
        # 1. Hooking into the target's network layer
        # 2. Adding delays to responses
        # 3. Observing how the agent handles the delays

        results = {
            "success": True,  # Placeholder
            "observations": [
                f"Applied {self.latency_ms}ms latency to network requests",
                "This is a placeholder - actual implementation needed"
            ],
            "details": {
                "scenario_type": self.__class__.__name__,
                "config": {
                    "latency_ms": self.latency_ms,
                    **self.config
                }
            }
        }

        self.teardown()
        return results
