"""
Infrastructure testing scenarios for Tohu.

This package contains scenarios that test the reliability and
robustness of the infrastructure supporting AI agents.
"""

from tohu.scenarios.infrastructure.tool_llm_failures import ToolLLMFailureScenario
from tohu.scenarios.infrastructure.model_degradation import ModelDegradationScenario
from tohu.scenarios.infrastructure.corrupted_state import CorruptedStateScenario
from tohu.scenarios.infrastructure.resource_exhaustion import ResourceExhaustionScenario
from tohu.scenarios.infrastructure.wrong_context_memory import WrongContextMemoryScenario
from tohu.scenarios.infrastructure.high_latency import HighLatencyScenario

__all__ = [
    "ToolLLMFailureScenario",
    "ModelDegradationScenario",
    "CorruptedStateScenario",
    "ResourceExhaustionScenario",
    "WrongContextMemoryScenario",
    "HighLatencyScenario"
]
