"""
Agent behavior testing scenarios for Tohu.

This package contains scenarios that test how agents behave under
various challenging conditions related to their core behavior.
"""

from tohu.scenarios.agent_behavior.rogue_agent import RogueAgentScenario
from tohu.scenarios.agent_behavior.stupid_selectors import StupidSelectorsScenario
from tohu.scenarios.agent_behavior.abrupt_conversations import AbruptConversationsScenario
from tohu.scenarios.agent_behavior.wrong_termination import WrongTerminationScenario

__all__ = [
    "RogueAgentScenario",
    "StupidSelectorsScenario",
    "AbruptConversationsScenario",
    "WrongTerminationScenario"
]
