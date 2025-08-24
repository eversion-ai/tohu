"""
Resource Exhaustion scenario for testing agent behavior under resource constraints.

This scenario simulates API rate limiting, token exhaustion, and other resource
constraints to test how agents handle external limitations gracefully.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Callable, Union
import logging
import random
import time
import threading
from collections import defaultdict, deque

from tohu.core.scenario import ChaosScenario

logger = logging.getLogger(__name__)


class RateLimitExceeded(Exception):
    """Exception raised when rate limits are exceeded."""
    pass


class ResourceExhausted(Exception):
    """Exception raised when resources are exhausted."""
    pass


@dataclass
class ResourceExhaustionScenario(ChaosScenario):
    """
    Tests an agent's ability to handle resource constraints and rate limiting.

    This scenario simulates various resource limitations including API rate limits,
    token exhaustion, memory constraints, and CPU limitations to test whether
    the agent implements proper backoff strategies and resource management.
    """

    name: str = "Resource Exhaustion Test"
    description: str = "Tests agent's handling of resource constraints and rate limits."

    # Configuration options
    rate_limit_enabled: bool = True
    token_limit_enabled: bool = True
    memory_limit_enabled: bool = False  # More complex to implement safely

    # Rate limiting configuration
    requests_per_minute: int = 10
    requests_per_hour: int = 100
    burst_allowance: int = 5  # Extra requests allowed in short bursts

    # Token limiting configuration
    tokens_per_minute: int = 1000
    tokens_per_day: int = 10000

    # Backoff testing
    test_exponential_backoff: bool = True
    min_backoff_seconds: float = 1.0
    max_backoff_seconds: float = 60.0

    # Resource types to constrain
    resource_types: List[str] = field(default_factory=list)

    # Tracking
    original_methods: Dict[Any, Dict[str, Callable]] = field(default_factory=dict)

    def __post_init__(self):
        """Initialize the scenario with default resource types if none provided."""
        super().__post_init__()
        if not self.resource_types:
            self.resource_types = [
                "api_calls",      # General API call rate limiting
                "llm_requests",   # LLM-specific request limiting
                "token_usage",    # Token consumption limiting
                "tool_calls",     # Tool usage limiting
                "data_retrieval", # Database/storage access limiting
                "compute_time"    # CPU/compute time limiting
            ]

        # Initialize rate limiting tracking
        self.request_times = defaultdict(deque)  # Track request timestamps by resource type
        self.token_usage = defaultdict(int)      # Track token usage by time period
        self.backoff_attempts = []               # Track backoff behavior
        self.resource_exhaustions = []           # Track when resources were exhausted

    def setup(self) -> None:
        """Prepare the resource exhaustion scenario."""
        logger.info("Setting up Resource Exhaustion scenario")
        self.original_methods = {}

        # Reset tracking
        self.request_times.clear()
        self.token_usage.clear()
        self.backoff_attempts.clear()
        self.resource_exhaustions.clear()

        # Start cleanup thread for old tracking data
        self._cleanup_thread = threading.Thread(target=self._cleanup_old_data, daemon=True)
        self._cleanup_thread.start()

    def _cleanup_old_data(self) -> None:
        """Clean up old tracking data to prevent memory leaks."""
        while True:
            try:
                current_time = time.time()
                cutoff_time = current_time - 3600  # Keep last hour of data

                # Clean up old request timestamps
                for resource_type in list(self.request_times.keys()):
                    times = self.request_times[resource_type]
                    while times and times[0] < cutoff_time:
                        times.popleft()

                # Clean up old token usage (keep daily data)
                daily_cutoff = current_time - 86400  # 24 hours
                for period in list(self.token_usage.keys()):
                    if isinstance(period, (int, float)) and period < daily_cutoff:
                        del self.token_usage[period]

                # Sleep for a minute before next cleanup
                time.sleep(60)

            except Exception as e:
                logger.error(f"Error in cleanup thread: {e}")
                time.sleep(60)

    def _is_rate_limited(self, resource_type: str) -> tuple[bool, float]:
        """
        Check if a resource type is currently rate limited.

        Args:
            resource_type: The type of resource being accessed

        Returns:
            A tuple of (is_limited, retry_after_seconds)
        """
        current_time = time.time()
        times = self.request_times[resource_type]

        # Remove old timestamps (older than 1 hour)
        while times and times[0] < current_time - 3600:
            times.popleft()

        # Check per-minute limit
        minute_ago = current_time - 60
        recent_requests = sum(1 for t in times if t > minute_ago)

        if recent_requests >= self.requests_per_minute:
            # Calculate retry-after time
            oldest_in_window = next((t for t in times if t > minute_ago), current_time)
            retry_after = 60 - (current_time - oldest_in_window) + random.uniform(0, 5)
            return True, retry_after

        # Check per-hour limit
        hour_ago = current_time - 3600
        hourly_requests = sum(1 for t in times if t > hour_ago)

        if hourly_requests >= self.requests_per_hour:
            # Calculate retry-after time (until oldest request in hour window expires)
            oldest_in_hour = next((t for t in times if t > hour_ago), current_time)
            retry_after = 3600 - (current_time - oldest_in_hour) + random.uniform(0, 30)
            return True, retry_after

        # Check burst protection (more than burst_allowance in last 10 seconds)
        burst_window = current_time - 10
        burst_requests = sum(1 for t in times if t > burst_window)

        if burst_requests >= self.burst_allowance:
            retry_after = 10 - (current_time - max(t for t in times if t > burst_window)) + random.uniform(1, 3)
            return True, retry_after

        return False, 0.0

    def _is_token_limited(self, estimated_tokens: int = 100) -> tuple[bool, float]:
        """
        Check if token usage would exceed limits.

        Args:
            estimated_tokens: Estimated tokens for this request

        Returns:
            A tuple of (is_limited, retry_after_seconds)
        """
        if not self.token_limit_enabled:
            return False, 0.0

        current_time = time.time()

        # Check per-minute token limit
        minute_key = int(current_time // 60)
        minute_usage = sum(self.token_usage[k] for k in self.token_usage
                          if abs(k - minute_key) < 1)  # Current and adjacent minutes

        if minute_usage + estimated_tokens > self.tokens_per_minute:
            retry_after = 60 - (current_time % 60) + random.uniform(1, 10)
            return True, retry_after

        # Check per-day token limit
        day_key = int(current_time // 86400)
        daily_usage = sum(self.token_usage[k] for k in self.token_usage
                         if int(k // 1440) == int(day_key // 1440))  # Same day

        if daily_usage + estimated_tokens > self.tokens_per_day:
            # Calculate time until next day
            seconds_in_day = current_time % 86400
            retry_after = 86400 - seconds_in_day + random.uniform(60, 3600)
            return True, retry_after

        return False, 0.0

    def _record_usage(self, resource_type: str, tokens_used: int = 0) -> None:
        """
        Record usage of a resource.

        Args:
            resource_type: The type of resource used
            tokens_used: Number of tokens consumed (if applicable)
        """
        current_time = time.time()

        # Record request timestamp
        self.request_times[resource_type].append(current_time)

        # Record token usage if applicable
        if tokens_used > 0:
            minute_key = int(current_time // 60)
            self.token_usage[minute_key] += tokens_used

    def _estimate_tokens(self, *args, **kwargs) -> int:
        """
        Estimate token usage for a request based on its arguments.

        This is a simplified estimation - real implementations would
        need more sophisticated token counting.
        """
        total_chars = 0

        # Count characters in string arguments
        for arg in args:
            if isinstance(arg, str):
                total_chars += len(arg)
            elif isinstance(arg, (dict, list)):
                # Convert to string to estimate
                total_chars += len(str(arg))

        for value in kwargs.values():
            if isinstance(value, str):
                total_chars += len(value)
            elif isinstance(value, (dict, list)):
                total_chars += len(str(value))

        # Rough estimation: 4 characters per token (common for many models)
        estimated_tokens = max(10, total_chars // 4)

        # Add some randomness to make it more realistic
        estimated_tokens = int(estimated_tokens * random.uniform(0.8, 1.4))

        return min(estimated_tokens, 4000)  # Cap at reasonable maximum

    def _create_resource_interceptor(self, original_fn: Callable,
                                   resource_type: str) -> Callable:
        """
        Create a wrapper that enforces resource constraints.

        Args:
            original_fn: The original method
            resource_type: The type of resource this method consumes

        Returns:
            A wrapped function that enforces resource limits
        """
        def intercepted_fn(*args, **kwargs):
            # Estimate resource usage for this call
            estimated_tokens = self._estimate_tokens(*args, **kwargs)

            # Check rate limits
            if self.rate_limit_enabled:
                is_rate_limited, rate_retry_after = self._is_rate_limited(resource_type)

                if is_rate_limited:
                    error_msg = (f"Rate limit exceeded for {resource_type}. "
                               f"Retry after {rate_retry_after:.1f} seconds.")

                    self.resource_exhaustions.append({
                        "type": "rate_limit",
                        "resource": resource_type,
                        "retry_after": rate_retry_after,
                        "timestamp": time.time()
                    })

                    logger.warning(error_msg)
                    raise RateLimitExceeded(error_msg)

            # Check token limits
            if self.token_limit_enabled and resource_type in ["llm_requests", "api_calls"]:
                is_token_limited, token_retry_after = self._is_token_limited(estimated_tokens)

                if is_token_limited:
                    error_msg = (f"Token limit exceeded. Estimated {estimated_tokens} tokens would "
                               f"exceed quota. Retry after {token_retry_after:.1f} seconds.")

                    self.resource_exhaustions.append({
                        "type": "token_limit",
                        "resource": resource_type,
                        "retry_after": token_retry_after,
                        "estimated_tokens": estimated_tokens,
                        "timestamp": time.time()
                    })

                    logger.warning(error_msg)
                    raise ResourceExhausted(error_msg)

            # If we get here, resource usage is allowed
            try:
                # Record the usage before making the call
                self._record_usage(resource_type, estimated_tokens)

                # Make the actual call
                result = original_fn(*args, **kwargs)

                # If successful, we might want to track actual token usage
                # (if the result contains token count information)
                actual_tokens = estimated_tokens  # Default to estimate

                # Try to extract actual token usage from response
                if isinstance(result, dict):
                    # Check common token usage fields
                    for token_field in ["usage", "token_count", "tokens_used"]:
                        if token_field in result:
                            token_info = result[token_field]
                            if isinstance(token_info, dict):
                                for field in ["total_tokens", "completion_tokens", "prompt_tokens"]:
                                    if field in token_info:
                                        actual_tokens = max(actual_tokens, token_info[field])
                            elif isinstance(token_info, int):
                                actual_tokens = token_info
                            break

                # Update token usage with actual count if different
                if actual_tokens != estimated_tokens:
                    minute_key = int(time.time() // 60)
                    self.token_usage[minute_key] += (actual_tokens - estimated_tokens)

                return result

            except Exception as e:
                # If the original function raises an exception, we should still
                # record that we attempted to use the resource (to prevent
                # rapid retry attempts that could overwhelm the system)
                logger.debug(f"Original function raised exception: {e}")
                raise

        return intercepted_fn

    def intercept_resource_method(self, target: Any, method_name: str,
                                 resource_type: str) -> None:
        """
        Intercept a method that consumes resources.

        Args:
            target: The object containing the method
            method_name: The name of the method to intercept
            resource_type: The type of resource this method consumes
        """
        if not hasattr(target, method_name):
            logger.warning(f"Target has no method named {method_name}")
            return

        # Initialize dict for this target if needed
        if target not in self.original_methods:
            self.original_methods[target] = {}

        # Save original method if we haven't already
        if method_name not in self.original_methods[target]:
            self.original_methods[target][method_name] = getattr(target, method_name)

            # Replace with our interceptor
            interceptor = self._create_resource_interceptor(
                self.original_methods[target][method_name],
                resource_type
            )
            setattr(target, method_name, interceptor)

            logger.info(f"Intercepted {resource_type} method {method_name} on {target.__class__.__name__}")

    def restore_methods(self) -> None:
        """Restore all intercepted methods to their original implementations."""
        for target, methods in self.original_methods.items():
            for method_name, original_method in methods.items():
                setattr(target, method_name, original_method)
                logger.info(f"Restored original {method_name} on {target.__class__.__name__}")

    def run(self, target: Any) -> Dict[str, Any]:
        """
        Execute the resource exhaustion scenario against the target system.

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
            "rate_limits_configured": self.rate_limit_enabled,
            "token_limits_configured": self.token_limit_enabled,
            "limits": {
                "requests_per_minute": self.requests_per_minute,
                "requests_per_hour": self.requests_per_hour,
                "tokens_per_minute": self.tokens_per_minute,
                "tokens_per_day": self.tokens_per_day
            },
            "resource_exhaustions": 0,
            "backoff_attempts": 0
        }

        try:
            # Identify methods to intercept based on resource types
            method_mappings = {
                "api_calls": ["request", "call", "execute", "run", "invoke"],
                "llm_requests": ["generate", "complete", "chat", "predict", "generate_text"],
                "token_usage": ["generate", "complete", "chat", "predict"],
                "tool_calls": ["run_tool", "execute_tool", "call_tool", "use_tool"],
                "data_retrieval": ["get", "fetch", "retrieve", "query", "load"],
                "compute_time": ["process", "compute", "calculate", "analyze"]
            }

            for resource_type in self.resource_types:
                if resource_type in method_mappings:
                    for method_name in method_mappings[resource_type]:
                        if hasattr(target, method_name) and callable(getattr(target, method_name)):
                            self.intercept_resource_method(target, method_name, resource_type)
                            details["methods_intercepted"].append(f"{resource_type}:{method_name}")

            # Also check for resource-consuming attributes
            for attr_name in dir(target):
                if attr_name.startswith("_"):
                    continue

                attr = getattr(target, attr_name)

                # Check if this attribute has methods we should intercept
                for resource_type, method_names in method_mappings.items():
                    for method_name in method_names:
                        if hasattr(attr, method_name) and callable(getattr(attr, method_name)):
                            self.intercept_resource_method(attr, method_name, resource_type)
                            details["methods_intercepted"].append(f"{attr_name}.{method_name}:{resource_type}")

            if not details["methods_intercepted"]:
                observations.append("Could not identify any resource-consuming methods to intercept")
                return {
                    "success": False,
                    "observations": observations,
                    "details": details
                }

            observations.append(f"Intercepted {len(details['methods_intercepted'])} resource-consuming methods")

            # Configure the specific limits
            if self.rate_limit_enabled:
                observations.append(f"Rate limiting: {self.requests_per_minute}/min, {self.requests_per_hour}/hour")

            if self.token_limit_enabled:
                observations.append(f"Token limiting: {self.tokens_per_minute}/min, {self.tokens_per_day}/day")

            # Provide guidance on testing
            observations.append(
                "To test: Use the agent repeatedly and quickly to trigger rate limits. "
                "Observe if it implements proper backoff and retry strategies."
            )

            if self.test_exponential_backoff:
                observations.append(
                    "Watch for exponential backoff: the agent should wait longer "
                    "between retries after repeated failures."
                )

            # If exhaustions have been triggered, analyze them
            if self.resource_exhaustions:
                details["resource_exhaustions"] = len(self.resource_exhaustions)

                observations.append(f"Triggered {details['resource_exhaustions']} resource exhaustions")

                # Analyze backoff behavior (this would need to be implemented
                # based on observing the agent's actual retry behavior)
                details["backoff_attempts"] = len(self.backoff_attempts)

                if details["backoff_attempts"] > 0:
                    observations.append("Agent attempted backoff strategies")
                else:
                    observations.append("No backoff behavior detected - may indicate poor error handling")

            # Success if we intercepted methods (actual testing happens during use)
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
