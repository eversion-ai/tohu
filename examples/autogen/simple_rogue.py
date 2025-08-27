"""
Simplified Rogue Agent Chaos Testing for AutoGen

This module provides a clean, minimal interface for adding rogue agent testing
to any AutoGen implementation with just a decorator.
"""

import random
import logging
from functools import wraps
from typing import Dict, Any, Optional, List

# Configure logging
logger = logging.getLogger(__name__)

class SimpleRogueAgent:
    """Minimal rogue agent implementation"""

    def __init__(self, chaos_probability: float = 0.3):
        self.chaos_probability = chaos_probability
        self.is_active = False
        self.deviation_count = 0

    def should_activate(self) -> bool:
        """Simple probability check for activation"""
        return random.random() < self.chaos_probability

    def corrupt_task(self, original_task: str) -> str:
        """Apply simple task corruption"""
        if not self.should_activate():
            return original_task

        self.is_active = True
        self.deviation_count += 1

        # Import rogue prompts
        from rogue_prompts import get_random_rogue_task
        corrupted_task = get_random_rogue_task(original_task)

        logger.warning(f"🔥 ROGUE: Task corrupted (attempt #{self.deviation_count})")
        return corrupted_task

    def corrupt_system_message(self, original_message: str) -> str:
        """Apply simple system message corruption"""
        if not self.should_activate():
            return original_message

        self.is_active = True

        # Import rogue prompts
        from rogue_prompts import get_random_rogue_system_message
        corrupted_message = get_random_rogue_system_message()

        logger.warning(f"🔥 ROGUE: System message corrupted")
        return corrupted_message

    def corrupt_tool_response(self, tool_name: str, normal_response: str) -> str:
        """Apply simple tool response corruption"""
        if not self.should_activate():
            return normal_response

        self.is_active = True

        # Import rogue prompts
        from rogue_prompts import get_random_rogue_tool_response
        corrupted_response = get_random_rogue_tool_response(tool_name, normal_response)

        logger.warning(f"🔥 ROGUE: Tool '{tool_name}' corrupted")
        return corrupted_response

    def get_status(self) -> Dict[str, Any]:
        """Get simple status"""
        return {
            "active": self.is_active,
            "deviations": self.deviation_count,
            "probability": self.chaos_probability
        }

# Global instance
_rogue_agent: Optional[SimpleRogueAgent] = None

def rogue_chaos(probability: float = 0.3):
    """
    Simple decorator to add rogue agent chaos to any AutoGen function.

    Usage:
        @rogue_chaos(probability=0.3)
        async def my_agent_function():
            # your AutoGen code here
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            global _rogue_agent
            _rogue_agent = SimpleRogueAgent(chaos_probability=probability)

            logger.info(f"🔥 CHAOS: Rogue agent active (probability: {probability})")

            try:
                result = await func(*args, **kwargs)

                # Simple status log
                status = _rogue_agent.get_status()
                if status["active"]:
                    logger.warning(f"🔥 ROGUE: {status['deviations']} deviations detected")
                else:
                    logger.info("✅ NORMAL: No rogue behavior this run")

                return result

            except Exception as e:
                logger.error(f"🔥 ERROR: Execution failed: {e}")
                raise

        return wrapper
    return decorator

def get_rogue_agent() -> Optional[SimpleRogueAgent]:
    """Get the current rogue agent instance"""
    return _rogue_agent

def is_rogue_active() -> bool:
    """Check if rogue agent is currently active"""
    return _rogue_agent is not None and _rogue_agent.is_active

# Simple helper functions for easy integration
def maybe_corrupt_task(task: str) -> str:
    """Helper: Maybe corrupt a task"""
    if _rogue_agent:
        return _rogue_agent.corrupt_task(task)
    return task

def maybe_corrupt_system_message(message: str) -> str:
    """Helper: Maybe corrupt a system message"""
    if _rogue_agent:
        return _rogue_agent.corrupt_system_message(message)
    return message

def maybe_corrupt_tool_response(tool_name: str, response: str) -> str:
    """Helper: Maybe corrupt a tool response"""
    if _rogue_agent:
        return _rogue_agent.corrupt_tool_response(tool_name, response)
    return response
