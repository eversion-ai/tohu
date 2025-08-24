"""
Multi-agent testing scenarios for Tohu.

This package contains scenarios that test the interactions
between multiple agents in a system.
"""

from tohu.scenarios.multiagent.conflicting_instructions import ConflictingInstructionsScenario
from tohu.scenarios.multiagent.oscillating_conversations import OscillatingConversationScenario

__all__ = [
    "ConflictingInstructionsScenario",
    "OscillatingConversationScenario"
]
