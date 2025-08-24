"""
Security testing scenarios for Tohu.

This package contains scenarios that test the security aspects
of AI agents, including resistance to attacks and manipulation.
"""

from tohu.scenarios.security.prompt_injection import PromptInjectionScenario
from tohu.scenarios.security.data_poisoning import DataPoisoningScenario

__all__ = [
    "PromptInjectionScenario",
    "DataPoisoningScenario"
]
