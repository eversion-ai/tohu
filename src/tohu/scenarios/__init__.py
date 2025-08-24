"""
Built-in chaos testing scenarios for the Tohu framework.

This package contains ready-to-use scenarios for testing
different aspects of AI agent robustness.
"""

# Import scenarios for automatic discovery
from tohu.scenarios.hallucination import HallucinationScenario

# Import category-specific scenarios
from tohu.scenarios.agent_behavior import (
    RogueAgentScenario,
    StupidSelectorsScenario,
    AbruptConversationsScenario,
    WrongTerminationScenario
)
from tohu.scenarios.infrastructure import (
    ToolLLMFailureScenario,
    ModelDegradationScenario,
    CorruptedStateScenario,
    ResourceExhaustionScenario,
    WrongContextMemoryScenario,
    HighLatencyScenario
)
from tohu.scenarios.security import (
    PromptInjectionScenario,
    DataPoisoningScenario
)
from tohu.scenarios.multiagent import (
    ConflictingInstructionsScenario,
    OscillatingConversationScenario
)

# Export available scenarios
__all__ = [
    # General scenarios
    "HallucinationScenario",

    # Agent behavior scenarios
    "RogueAgentScenario",
    "StupidSelectorsScenario",
    "AbruptConversationsScenario",
    "WrongTerminationScenario",

    # Infrastructure scenarios
    "ToolLLMFailureScenario",
    "ModelDegradationScenario",
    "CorruptedStateScenario",
    "ResourceExhaustionScenario",
    "WrongContextMemoryScenario",
    "HighLatencyScenario",

    # Security scenarios
    "PromptInjectionScenario",
    "DataPoisoningScenario",

    # Multi-agent scenarios
    "ConflictingInstructionsScenario",
    "OscillatingConversationScenario",
]
