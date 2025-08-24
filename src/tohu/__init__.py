"""
Tohu: A chaos engineering framework for agentic AI systems.

Tohu provides tools and patterns to test the robustness of AI agents
by simulating various failure modes and edge cases.
"""

__version__ = "0.1.0"

from tohu.core.engine import ChaosEngine
from tohu.core.scenario import ChaosScenario, SimpleScenario

__all__ = ["ChaosEngine", "ChaosScenario", "SimpleScenario"]
