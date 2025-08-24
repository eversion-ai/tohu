"""
Oscillating Conversation Messages Chaos Scenario.

This scenario creates repetitive, non-productive loops between agents
or between an agent and a tool to test cycle detection and breaking.
"""

import random
import time
import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union, Set

from tohu.core.scenario import ChaosScenario

logger = logging.getLogger(__name__)


@dataclass
class OscillatingConversationScenario(ChaosScenario):
    """
    Creates repetitive conversation loops to test cycle detection.

    This scenario induces non-productive conversation cycles where agents
    or tools provide repetitive, ambiguous responses, testing the system's
    ability to detect and break out of cycles.
    """

    oscillation_probability: float = 0.5
    """Probability of triggering oscillating behavior (0.0 to 1.0)"""

    max_oscillations: int = 5
    """Maximum number of oscillations before test fails"""

    oscillation_types: List[str] = None
    """Types of oscillations to create"""

    detection_timeout: float = 10.0
    """Time to wait for cycle detection (seconds)"""

    def __post_init__(self):
        if self.oscillation_types is None:
            self.oscillation_types = [
                'clarification_loop',
                'confirmation_loop',
                'ambiguous_response_loop',
                'question_answering_loop',
                'decision_defer_loop',
                'validation_loop'
            ]

    def run(self, target: Any) -> Dict[str, Any]:
        """Apply oscillating conversation chaos to the target."""
        logger.info(f"Starting OscillatingConversationScenario with {self.oscillation_probability*100}% oscillation rate")

        observations = []
        oscillations_triggered = 0
        cycles_detected = 0
        cycle_breaks = 0
        original_methods = {}
        message_history = []

        try:
            # Intercept conversation methods
            conversation_methods = [
                'generate_reply', 'send_message', 'receive_message', 'respond',
                'process_message', 'handle_input', 'reply_to', 'answer',
                'ask_question', 'request_clarification', 'provide_feedback'
            ]

            for method_name in conversation_methods:
                if hasattr(target, method_name):
                    original_method = getattr(target, method_name)
                    original_methods[method_name] = original_method

                    def create_oscillating_method(orig_method, method_name):
                        def oscillating_method(*args, **kwargs):
                            nonlocal oscillations_triggered, cycles_detected, cycle_breaks

                            # Record the message/interaction
                            message_content = self._extract_message_content(args, kwargs)
                            message_history.append({
                                'method': method_name,
                                'content': message_content,
                                'timestamp': time.time()
                            })

                            # Check for existing cycles
                            cycle_detected = self._detect_cycle(message_history)
                            if cycle_detected:
                                cycles_detected += 1
                                observations.append(f"Detected cycle in {method_name}")

                                # Test if agent can break the cycle
                                break_success = self._test_cycle_breaking(target, method_name)
                                if break_success:
                                    cycle_breaks += 1
                                    observations.append(f"Successfully broke cycle in {method_name}")
                                else:
                                    observations.append(f"Failed to break cycle in {method_name}")

                            # Trigger oscillating behavior
                            if random.random() < self.oscillation_probability:
                                oscillations_triggered += 1
                                oscillation_type = random.choice(self.oscillation_types)

                                logger.warning(f"🔥 CHAOS: Triggering {oscillation_type} in {method_name}")
                                observations.append(f"Triggered {oscillation_type} in {method_name}")

                                # Apply specific oscillation pattern
                                return self._apply_oscillation(
                                    orig_method, oscillation_type, args, kwargs, message_content
                                )

                            return orig_method(*args, **kwargs)

                        return oscillating_method

                    setattr(target, method_name, create_oscillating_method(original_method, method_name))
                    logger.debug(f"Intercepted {method_name} for oscillation testing")

            # Test multi-agent oscillations if applicable
            self._test_multi_agent_oscillations(target, observations)

            # Test tool-agent oscillations
            self._test_tool_oscillations(target, observations)

            # Test cycle detection mechanisms
            self._test_cycle_detection_mechanisms(target, observations)

            # Evaluate results
            cycle_detection_rate = cycles_detected / max(oscillations_triggered, 1)
            cycle_break_rate = cycle_breaks / max(cycles_detected, 1)

            success = (
                oscillations_triggered > 0 and
                cycle_detection_rate >= 0.5 and  # Detect at least 50% of cycles
                cycle_break_rate >= 0.6          # Break at least 60% of detected cycles
            )

            if oscillations_triggered == 0:
                observations.append("No conversation methods found to create oscillations")
                success = False

            result = {
                'success': success,
                'observations': observations,
                'oscillations_triggered': oscillations_triggered,
                'cycles_detected': cycles_detected,
                'cycle_breaks': cycle_breaks,
                'cycle_detection_rate': cycle_detection_rate,
                'cycle_break_rate': cycle_break_rate,
                'scenario': 'OscillatingConversationScenario'
            }

            logger.info(f"OscillatingConversationScenario completed: {result}")
            return result

        except Exception as e:
            logger.error(f"OscillatingConversationScenario failed: {e}")
            return {
                'success': False,
                'observations': [f"Scenario execution failed: {str(e)}"],
                'error': str(e),
                'scenario': 'OscillatingConversationScenario'
            }

        finally:
            # Restore original methods
            for method_name, original_method in original_methods.items():
                if hasattr(target, method_name):
                    setattr(target, method_name, original_method)
                    logger.debug(f"Restored original {method_name}")

    def _extract_message_content(self, args: tuple, kwargs: dict) -> str:
        """Extract message content from method arguments."""
        # Try to find message content in various forms
        content_candidates = []

        # Check positional arguments
        for arg in args:
            if isinstance(arg, str) and len(arg.strip()) > 0:
                content_candidates.append(arg.strip())

        # Check keyword arguments
        content_keys = ['message', 'content', 'text', 'prompt', 'input', 'query']
        for key in content_keys:
            if key in kwargs and isinstance(kwargs[key], str):
                content_candidates.append(kwargs[key].strip())

        # Return the first non-empty content or a placeholder
        for content in content_candidates:
            if content and len(content) > 0:
                return content[:100]  # Truncate for comparison

        return "unknown_content"

    def _detect_cycle(self, message_history: List[Dict], lookback: int = 6) -> bool:
        """Detect if there's a cycle in recent message history."""
        if len(message_history) < 4:  # Need at least 4 messages for a cycle
            return False

        # Look at recent messages
        recent_messages = message_history[-lookback:]
        content_sequence = [msg['content'] for msg in recent_messages]

        # Check for repeating patterns
        for pattern_length in range(2, len(content_sequence) // 2 + 1):
            for start_idx in range(len(content_sequence) - pattern_length * 2 + 1):
                pattern = content_sequence[start_idx:start_idx + pattern_length]
                next_pattern = content_sequence[start_idx + pattern_length:start_idx + pattern_length * 2]

                if pattern == next_pattern and len(pattern) > 0:
                    return True

        # Check for exact repetitions
        content_counts = {}
        for content in content_sequence[-4:]:  # Last 4 messages
            content_counts[content] = content_counts.get(content, 0) + 1
            if content_counts[content] >= 3:  # Same message 3+ times
                return True

        return False

    def _apply_oscillation(self, original_method, oscillation_type: str, args: tuple, kwargs: dict, message_content: str):
        """Apply specific oscillation pattern."""

        try:
            if oscillation_type == 'clarification_loop':
                return self._create_clarification_loop(original_method, args, kwargs, message_content)
            elif oscillation_type == 'confirmation_loop':
                return self._create_confirmation_loop(original_method, args, kwargs, message_content)
            elif oscillation_type == 'ambiguous_response_loop':
                return self._create_ambiguous_response_loop(original_method, args, kwargs, message_content)
            elif oscillation_type == 'question_answering_loop':
                return self._create_question_answering_loop(original_method, args, kwargs, message_content)
            elif oscillation_type == 'decision_defer_loop':
                return self._create_decision_defer_loop(original_method, args, kwargs, message_content)
            elif oscillation_type == 'validation_loop':
                return self._create_validation_loop(original_method, args, kwargs, message_content)
            else:
                return original_method(*args, **kwargs)

        except Exception as e:
            logger.warning(f"Oscillation application failed: {e}")
            return original_method(*args, **kwargs)

    def _create_clarification_loop(self, original_method, args, kwargs, message_content):
        """Create a clarification request loop."""
        clarification_responses = [
            "Could you clarify what you mean?",
            "I'm not sure I understand. Can you elaborate?",
            "Can you provide more details about that?",
            "What specifically are you referring to?",
            "I need more information to help you."
        ]
        return random.choice(clarification_responses)

    def _create_confirmation_loop(self, original_method, args, kwargs, message_content):
        """Create a confirmation request loop."""
        confirmation_responses = [
            "Just to confirm, are you asking about...?",
            "Let me make sure I understand correctly...",
            "Can you confirm that you want me to...?",
            "To be clear, you're asking me to...?",
            "Just verifying - you need help with...?"
        ]
        return random.choice(confirmation_responses)

    def _create_ambiguous_response_loop(self, original_method, args, kwargs, message_content):
        """Create ambiguous responses that prompt more questions."""
        ambiguous_responses = [
            "It depends on what you're looking for.",
            "There are several ways to approach this.",
            "The answer varies depending on the context.",
            "It's complicated and depends on many factors.",
            "That's an interesting question with multiple aspects."
        ]
        return random.choice(ambiguous_responses)

    def _create_question_answering_loop(self, original_method, args, kwargs, message_content):
        """Create a loop where questions are answered with questions."""
        question_responses = [
            "What made you ask that question?",
            "How would you like me to answer that?",
            "What's the context for this question?",
            "Are you looking for a specific type of answer?",
            "What would be most helpful for you to know?"
        ]
        return random.choice(question_responses)

    def _create_decision_defer_loop(self, original_method, args, kwargs, message_content):
        """Create a loop where decisions are constantly deferred."""
        defer_responses = [
            "I think we should consider this more carefully.",
            "Maybe we should explore other options first.",
            "Let's think about this from a different angle.",
            "Perhaps we need more information before deciding.",
            "I suggest we take more time to evaluate this."
        ]
        return random.choice(defer_responses)

    def _create_validation_loop(self, original_method, args, kwargs, message_content):
        """Create a validation request loop."""
        validation_responses = [
            "Can you double-check that information?",
            "Are you sure about that?",
            "Can you verify that's correct?",
            "I want to make sure we have the right information.",
            "Let me confirm those details are accurate."
        ]
        return random.choice(validation_responses)

    def _test_cycle_breaking(self, target: Any, method_name: str) -> bool:
        """Test if the agent can break out of cycles."""
        # Check if agent has cycle-breaking mechanisms
        break_methods = [
            'break_cycle', 'escape_loop', 'change_topic', 'reset_conversation',
            'escalate', 'try_different_approach', 'abort_conversation'
        ]

        for break_method in break_methods:
            if hasattr(target, break_method):
                try:
                    method = getattr(target, break_method)
                    result = method()
                    if result:  # Successful break attempt
                        return True
                except Exception as e:
                    logger.debug(f"Cycle breaking method {break_method} failed: {e}")

        # Check if agent has conversation state reset
        if hasattr(target, 'reset_state') or hasattr(target, 'clear_history'):
            try:
                reset_method = getattr(target, 'reset_state', None) or getattr(target, 'clear_history')
                reset_method()
                return True
            except Exception as e:
                logger.debug(f"State reset failed: {e}")

        return False

    def _test_multi_agent_oscillations(self, target: Any, observations: List[str]):
        """Test for multi-agent oscillation patterns."""
        if hasattr(target, 'agents') or hasattr(target, 'other_agents'):
            agents_attr = 'agents' if hasattr(target, 'agents') else 'other_agents'
            observations.append(f"Found multi-agent setup: {agents_attr}")

            # Check for multi-agent cycle detection
            multi_agent_detection_methods = [
                'detect_group_cycles', 'monitor_group_conversation',
                'check_multi_agent_loops', 'group_cycle_detection'
            ]

            for method_name in multi_agent_detection_methods:
                if hasattr(target, method_name):
                    observations.append(f"Agent has multi-agent cycle detection: {method_name}")

    def _test_tool_oscillations(self, target: Any, observations: List[str]):
        """Test for tool-agent oscillation patterns."""
        tool_attrs = ['tools', 'available_tools', 'tool_set', 'functions']

        for attr_name in tool_attrs:
            if hasattr(target, attr_name):
                observations.append(f"Found tool integration: {attr_name}")

                # Check for tool interaction monitoring
                if hasattr(target, 'monitor_tool_interactions'):
                    observations.append("Agent monitors tool interactions")
                else:
                    observations.append("Agent lacks tool interaction monitoring")

    def _test_cycle_detection_mechanisms(self, target: Any, observations: List[str]):
        """Test the agent's cycle detection capabilities."""
        detection_methods = [
            'detect_cycles', 'check_for_loops', 'monitor_patterns',
            'conversation_analysis', 'pattern_detection'
        ]

        detection_found = False
        for method_name in detection_methods:
            if hasattr(target, method_name):
                detection_found = True
                observations.append(f"Agent has cycle detection: {method_name}")

                # Test the detection method
                try:
                    method = getattr(target, method_name)
                    test_result = method()
                    observations.append(f"Cycle detection test result: {test_result}")
                except Exception as e:
                    observations.append(f"Cycle detection method {method_name} failed: {e}")

        if not detection_found:
            observations.append("Agent lacks explicit cycle detection mechanisms")

        # Check for conversation history tracking
        history_attrs = ['conversation_history', 'message_history', 'interaction_log']
        for attr_name in history_attrs:
            if hasattr(target, attr_name):
                observations.append(f"Agent tracks conversation: {attr_name}")
                break
        else:
            observations.append("Agent does not track conversation history")
