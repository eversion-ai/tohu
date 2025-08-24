"""
Tool and LLM Call Failures scenario for testing agent error handling.

This scenario simulates failures in the agent's primary interfaces to the world
and its "brain", testing for resilience against API errors and unexpected responses.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Callable, Union, Tuple
import logging
import random
import time
import traceback

from tohu.core.scenario import ChaosScenario

logger = logging.getLogger(__name__)


class ToolCallError(Exception):
    """Exception raised to simulate tool call failures."""
    pass


class LLMCallError(Exception):
    """Exception raised to simulate LLM API failures."""
    pass


@dataclass
class ToolLLMFailureScenario(ChaosScenario):
    """
    Tests an agent's ability to handle failures in tool calls and LLM API requests.

    This scenario intercepts calls to tools and LLM APIs, deliberately inducing
    failures, timeouts, and unexpected responses to test the agent's error
    handling and recovery mechanisms.
    """

    name: str = "Tool and LLM Call Failure Test"
    description: str = "Tests agent's resilience to tool and LLM API failures."

    # Configuration options
    tool_failure_rate: float = 0.3  # Probability of a tool call failing
    llm_failure_rate: float = 0.2  # Probability of an LLM call failing
    unexpected_response_rate: float = 0.25  # Probability of returning unexpected data
    timeout_rate: float = 0.15  # Probability of a timeout
    max_consecutive_failures: int = 3  # Maximum consecutive failures before recovery

    # Tracking state
    intercepted_methods: Dict[str, Callable] = field(default_factory=dict)
    consecutive_failures: Dict[str, int] = field(default_factory=dict)

    # Failure types
    failure_types: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Initialize the scenario with default failure types if none provided."""
        super().__post_init__()
        if not self.failure_types:
            self.failure_types = [
                "exception",           # Raise an exception
                "timeout",             # Simulate a timeout
                "empty_response",      # Return empty or null data
                "malformed_response",  # Return malformed/corrupt data
                "wrong_type",          # Return data of unexpected type
                "rate_limit",          # Simulate rate limiting
                "auth_error",          # Simulate authentication failure
            ]

    def setup(self) -> None:
        """Prepare the tool/LLM failure scenario."""
        logger.info("Setting up Tool/LLM Failure scenario")
        self.intercepted_methods.clear()
        self.consecutive_failures.clear()

    def _should_induce_failure(self, method_name: str, is_llm_call: bool = False) -> Tuple[bool, str]:
        """
        Determine if a failure should be induced for this call.

        Args:
            method_name: The name of the intercepted method
            is_llm_call: Whether this is an LLM API call (vs. a tool call)

        Returns:
            A tuple of (should_fail, failure_type)
        """
        # Track consecutive failures
        if method_name not in self.consecutive_failures:
            self.consecutive_failures[method_name] = 0

        # If we've hit the max consecutive failures, allow a success
        if self.consecutive_failures[method_name] >= self.max_consecutive_failures:
            self.consecutive_failures[method_name] = 0
            return False, ""

        # Determine failure probability based on call type
        failure_prob = self.llm_failure_rate if is_llm_call else self.tool_failure_rate

        # Check if we should induce a failure
        if random.random() < failure_prob:
            # Choose a failure type
            failure_type = random.choice(self.failure_types)

            # Increment consecutive failures
            self.consecutive_failures[method_name] += 1

            return True, failure_type

        # No failure
        self.consecutive_failures[method_name] = 0
        return False, ""

    def _create_interceptor(self, method_name: str, original_fn: Callable,
                          is_llm_call: bool = False) -> Callable:
        """
        Create a wrapper around a method that occasionally induces failures.

        Args:
            method_name: The name of the intercepted method
            original_fn: The original method
            is_llm_call: Whether this is an LLM API call (vs. a tool call)

        Returns:
            A wrapped function that may fail deliberately
        """
        def intercepted_fn(*args, **kwargs):
            # Decide whether to induce a failure
            should_fail, failure_type = self._should_induce_failure(method_name, is_llm_call)

            if should_fail:
                logger.info(f"Inducing {failure_type} in {method_name}")

                # Implement different failure types
                if failure_type == "exception":
                    error_cls = LLMCallError if is_llm_call else ToolCallError
                    raise error_cls(f"Simulated {failure_type} in {method_name}")

                elif failure_type == "timeout":
                    # Simulate a long delay, then either return or raise timeout
                    time.sleep(2.0)  # Simulate delay
                    if random.random() < 0.5:
                        raise TimeoutError(f"Simulated timeout in {method_name}")
                    # Otherwise continue with empty response
                    failure_type = "empty_response"

                # Handle other failure types that return unexpected data
                if failure_type == "empty_response":
                    # Return an empty or null response
                    if is_llm_call:
                        return {"content": "", "role": "assistant"}
                    return None

                elif failure_type == "malformed_response":
                    # Return malformed or corrupt data
                    if is_llm_call:
                        return {"content": "{{mal%formed&&JSON*(@#)}", "role": "assistant"}
                    return {"error": "malformed_data", "data": "{]invalid[}"}

                elif failure_type == "wrong_type":
                    # Return data of unexpected type
                    if is_llm_call:
                        return "This is just a string instead of the expected object"
                    return 12345  # Return a number instead of expected object

                elif failure_type == "rate_limit":
                    # Simulate rate limiting
                    raise Exception("Rate limit exceeded. Try again in 60 seconds.")

                elif failure_type == "auth_error":
                    # Simulate authentication failure
                    raise Exception("Authentication failed. Invalid API key or token.")

            # If no failure or unhandled failure type, call the original function
            try:
                result = original_fn(*args, **kwargs)

                # Potentially modify the successful response to be unexpected
                if random.random() < self.unexpected_response_rate:
                    logger.info(f"Modifying successful response from {method_name}")

                    # This is highly dependent on the expected return format
                    # Here's a simplified version that works with common patterns
                    if isinstance(result, dict):
                        if "content" in result:  # Common for LLM responses
                            # Add some gibberish to the content
                            result["content"] += " [UNEXPECTED_DATA: %$#@^&*()]"
                        elif "result" in result:  # Common for tool calls
                            # Replace some of the result with unexpected data
                            if isinstance(result["result"], str):
                                result["result"] = result["result"][:10] + " [TRUNCATED]"

                return result

            except Exception as e:
                # Log any unexpected errors in the original function
                logger.error(f"Unexpected error in original {method_name}: {str(e)}")
                logger.debug(traceback.format_exc())
                raise

        return intercepted_fn

    def intercept_method(self, target: Any, method_name: str, is_llm_call: bool = False) -> None:
        """
        Intercept a method on the target to induce failures.

        Args:
            target: The object containing the method
            method_name: The name of the method to intercept
            is_llm_call: Whether this is an LLM API call (vs. a tool call)
        """
        if not hasattr(target, method_name):
            logger.warning(f"Target has no method named {method_name}")
            return

        # Save original method if we haven't already
        if (target, method_name) not in self.intercepted_methods:
            original_fn = getattr(target, method_name)
            self.intercepted_methods[(target, method_name)] = original_fn

            # Replace with our interceptor
            interceptor = self._create_interceptor(method_name, original_fn, is_llm_call)
            setattr(target, method_name, interceptor)

            logger.info(f"Intercepted method {method_name} on {target.__class__.__name__}")

    def restore_methods(self) -> None:
        """Restore all intercepted methods to their original implementations."""
        for (target, method_name), original_fn in self.intercepted_methods.items():
            setattr(target, method_name, original_fn)
            logger.info(f"Restored original {method_name} on {target.__class__.__name__}")

        self.intercepted_methods.clear()

    def run(self, target: Any) -> Dict[str, Any]:
        """
        Execute the tool/LLM failure scenario against the target system.

        Args:
            target: The target agent or system to test

        Returns:
            A dictionary containing test results and observations
        """
        self.setup()

        # Record observations
        observations = []
        success = False
        details = {
            "scenario_type": self.__class__.__name__,
            "methods_intercepted": [],
            "failure_counts": {},
            "recovery_attempts": 0,
            "successful_recoveries": 0,
            "unhandled_failures": 0
        }

        try:
            # Identify methods to intercept based on common patterns
            # This is highly dependent on the agent framework being used

            # For LLM calls (looking for common method names across frameworks)
            llm_methods = ["generate", "complete", "chat", "predict", "generate_text"]
            for method_name in llm_methods:
                if hasattr(target, method_name) and callable(getattr(target, method_name)):
                    self.intercept_method(target, method_name, is_llm_call=True)
                    details["methods_intercepted"].append(f"llm:{method_name}")

            # For tool calls (looking for common method names across frameworks)
            tool_methods = ["run_tool", "execute_tool", "call_tool", "invoke"]
            for method_name in tool_methods:
                if hasattr(target, method_name) and callable(getattr(target, method_name)):
                    self.intercept_method(target, method_name, is_llm_call=False)
                    details["methods_intercepted"].append(f"tool:{method_name}")

            # If no methods were intercepted, try to find any callable methods
            if not details["methods_intercepted"]:
                for attr_name in dir(target):
                    if (attr_name.startswith("_") or not callable(getattr(target, attr_name))):
                        continue

                    # Assume any method with "call", "run", or "execute" might be relevant
                    if any(keyword in attr_name.lower() for keyword in ["call", "run", "execute", "invoke"]):
                        self.intercept_method(target, attr_name, is_llm_call=False)
                        details["methods_intercepted"].append(f"auto:{attr_name}")

            if not details["methods_intercepted"]:
                observations.append("Could not identify any methods to intercept")
                return {
                    "success": False,
                    "observations": observations,
                    "details": details
                }

            observations.append(f"Intercepted {len(details['methods_intercepted'])} methods")

            # Run a simulation of tasks that exercise the intercepted methods
            # In a real test, this would involve actual task execution
            # For now, we'll just analyze what we've intercepted

            # Check if we were able to intercept key functionality
            if any(m.startswith("llm:") for m in details["methods_intercepted"]):
                observations.append("Successfully intercepted LLM call methods")
            else:
                observations.append("Warning: Could not identify LLM call methods")

            if any(m.startswith("tool:") for m in details["methods_intercepted"]):
                observations.append("Successfully intercepted tool call methods")
            else:
                observations.append("Warning: Could not identify tool call methods")

            # Evaluate the agent's error handling capabilities
            # Since we can't actually run tasks here, we'll provide guidance
            observations.append(
                "To fully test, run a series of tasks with this scenario active "
                "and observe how the agent handles the induced failures"
            )

            # For now, success is based on whether we could intercept methods
            success = len(details["methods_intercepted"]) > 0

        finally:
            # Always restore the original methods
            self.restore_methods()
            observations.append("Restored all intercepted methods")

        self.teardown()

        return {
            "success": success,
            "observations": observations,
            "details": details
        }
