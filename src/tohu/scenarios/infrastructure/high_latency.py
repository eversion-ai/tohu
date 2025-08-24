"""
High-Latency Environment Chaos Scenario.

This scenario tests an agent's patience and ability to handle
asynchronous operations by introducing artificial delays.
"""

import random
import time
import asyncio
import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union, Callable
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError

from tohu.core.scenario import ChaosScenario

logger = logging.getLogger(__name__)


@dataclass
class HighLatencyScenario(ChaosScenario):
    """
    Introduces artificial delays to test latency handling.

    This scenario simulates slow networks, overloaded APIs, and high-latency
    environments to test the agent's patience, timeout handling, and ability
    to perform other tasks while waiting.
    """

    latency_injection_rate: float = 0.6
    """Probability of injecting latency (0.0 to 1.0)"""

    min_delay: float = 1.0
    """Minimum delay in seconds"""

    max_delay: float = 10.0
    """Maximum delay in seconds"""

    timeout_threshold: float = 15.0
    """Maximum acceptable timeout in seconds"""

    test_concurrency: bool = True
    """Whether to test concurrent operation handling"""

    latency_patterns: List[str] = None
    """Types of latency patterns to simulate"""

    def __post_init__(self):
        if self.latency_patterns is None:
            self.latency_patterns = [
                'network_delay',
                'api_overload',
                'database_slowdown',
                'processing_delay',
                'queue_backlog',
                'bandwidth_limitation'
            ]

    def run(self, target: Any) -> Dict[str, Any]:
        """Apply high latency chaos to the target."""
        logger.info(f"Starting HighLatencyScenario with {self.latency_injection_rate*100}% injection rate")

        observations = []
        delays_injected = 0
        timeouts_handled = 0
        concurrent_operations = 0
        successful_completions = 0
        original_methods = {}

        try:
            # Intercept methods that typically involve external calls
            latency_sensitive_methods = [
                'call_api', 'make_request', 'send_request', 'fetch_data',
                'query_database', 'search', 'retrieve', 'get_response',
                'process_request', 'execute_tool', 'run_function',
                'generate_reply', 'get_completion', 'invoke_model'
            ]

            for method_name in latency_sensitive_methods:
                if hasattr(target, method_name):
                    original_method = getattr(target, method_name)
                    original_methods[method_name] = original_method

                    def create_delayed_method(orig_method, method_name):
                        def delayed_method(*args, **kwargs):
                            nonlocal delays_injected, timeouts_handled, successful_completions

                            if random.random() < self.latency_injection_rate:
                                delays_injected += 1
                                latency_pattern = random.choice(self.latency_patterns)
                                delay_time = random.uniform(self.min_delay, self.max_delay)

                                logger.warning(f"🔥 CHAOS: Injecting {delay_time:.2f}s {latency_pattern} delay in {method_name}")
                                observations.append(f"Injected {delay_time:.2f}s {latency_pattern} delay in {method_name}")

                                # Apply the delay pattern
                                result = self._apply_latency_pattern(
                                    orig_method, latency_pattern, delay_time, args, kwargs, method_name
                                )

                                # Test timeout handling
                                timeout_success = self._test_timeout_handling(target, method_name, delay_time)
                                if timeout_success:
                                    timeouts_handled += 1

                                if result is not None:
                                    successful_completions += 1

                                return result

                            # Normal execution
                            try:
                                result = orig_method(*args, **kwargs)
                                successful_completions += 1
                                return result
                            except Exception as e:
                                logger.warning(f"Normal execution of {method_name} failed: {e}")
                                raise

                        return delayed_method

                    setattr(target, method_name, create_delayed_method(original_method, method_name))
                    logger.debug(f"Intercepted {method_name} for latency injection")

            # Test concurrent operation handling
            if self.test_concurrency:
                concurrent_success = self._test_concurrent_operations(target, observations)
                if concurrent_success:
                    concurrent_operations += 1

            # Test progressive timeout handling
            self._test_progressive_timeouts(target, observations)

            # Test queue/backlog handling
            self._test_queue_handling(target, observations)

            # Test graceful degradation
            self._test_graceful_degradation(target, observations)

            # Evaluate results
            completion_rate = successful_completions / max(delays_injected + successful_completions, 1)
            timeout_handling_rate = timeouts_handled / max(delays_injected, 1)

            success = (
                delays_injected > 0 and
                completion_rate >= 0.7 and        # At least 70% completion rate
                timeout_handling_rate >= 0.5      # Handle timeouts in at least 50% of cases
            )

            if delays_injected == 0:
                observations.append("No latency-sensitive methods found to test")
                success = False

            result = {
                'success': success,
                'observations': observations,
                'delays_injected': delays_injected,
                'timeouts_handled': timeouts_handled,
                'concurrent_operations': concurrent_operations,
                'successful_completions': successful_completions,
                'completion_rate': completion_rate,
                'timeout_handling_rate': timeout_handling_rate,
                'scenario': 'HighLatencyScenario'
            }

            logger.info(f"HighLatencyScenario completed: {result}")
            return result

        except Exception as e:
            logger.error(f"HighLatencyScenario failed: {e}")
            return {
                'success': False,
                'observations': [f"Scenario execution failed: {str(e)}"],
                'error': str(e),
                'scenario': 'HighLatencyScenario'
            }

        finally:
            # Restore original methods
            for method_name, original_method in original_methods.items():
                if hasattr(target, method_name):
                    setattr(target, method_name, original_method)
                    logger.debug(f"Restored original {method_name}")

    def _apply_latency_pattern(self, original_method: Callable, pattern: str, delay_time: float,
                              args: tuple, kwargs: dict, method_name: str) -> Any:
        """Apply specific latency pattern."""

        try:
            if pattern == 'network_delay':
                return self._simulate_network_delay(original_method, delay_time, args, kwargs)
            elif pattern == 'api_overload':
                return self._simulate_api_overload(original_method, delay_time, args, kwargs)
            elif pattern == 'database_slowdown':
                return self._simulate_database_slowdown(original_method, delay_time, args, kwargs)
            elif pattern == 'processing_delay':
                return self._simulate_processing_delay(original_method, delay_time, args, kwargs)
            elif pattern == 'queue_backlog':
                return self._simulate_queue_backlog(original_method, delay_time, args, kwargs)
            elif pattern == 'bandwidth_limitation':
                return self._simulate_bandwidth_limitation(original_method, delay_time, args, kwargs)
            else:
                # Default delay
                time.sleep(delay_time)
                return original_method(*args, **kwargs)

        except Exception as e:
            logger.warning(f"Latency pattern {pattern} application failed: {e}")
            return original_method(*args, **kwargs)

    def _simulate_network_delay(self, original_method: Callable, delay_time: float, args: tuple, kwargs: dict) -> Any:
        """Simulate network latency."""
        # Simulate variable network conditions
        jitter = random.uniform(-0.2, 0.2) * delay_time
        actual_delay = max(0.1, delay_time + jitter)

        logger.debug(f"Simulating network delay: {actual_delay:.2f}s")
        time.sleep(actual_delay)

        # Occasionally simulate packet loss (connection error)
        if random.random() < 0.1:  # 10% chance of connection error
            raise ConnectionError("Network packet loss - connection timeout")

        return original_method(*args, **kwargs)

    def _simulate_api_overload(self, original_method: Callable, delay_time: float, args: tuple, kwargs: dict) -> Any:
        """Simulate API server overload."""
        # Progressive delay to simulate overload
        chunks = 5
        chunk_delay = delay_time / chunks

        for i in range(chunks):
            time.sleep(chunk_delay)
            # Simulate increasing load
            if random.random() < 0.05:  # 5% chance of overload error
                raise Exception(f"API overload - server temporarily unavailable (503)")

        return original_method(*args, **kwargs)

    def _simulate_database_slowdown(self, original_method: Callable, delay_time: float, args: tuple, kwargs: dict) -> Any:
        """Simulate database query slowdown."""
        # Simulate slow query execution
        logger.debug(f"Simulating database slowdown: {delay_time:.2f}s")

        # Gradual delay to simulate query processing
        time.sleep(delay_time * 0.3)  # Initial delay
        time.sleep(delay_time * 0.4)  # Processing delay
        time.sleep(delay_time * 0.3)  # Final delay

        # Occasionally simulate database timeout
        if delay_time > 8.0 and random.random() < 0.15:
            raise Exception("Database query timeout - operation exceeded time limit")

        return original_method(*args, **kwargs)

    def _simulate_processing_delay(self, original_method: Callable, delay_time: float, args: tuple, kwargs: dict) -> Any:
        """Simulate CPU/processing intensive delay."""
        # Simulate heavy computation
        steps = max(1, int(delay_time))
        step_delay = delay_time / steps

        for step in range(steps):
            logger.debug(f"Processing step {step + 1}/{steps}")
            time.sleep(step_delay)

            # Simulate processing progress
            if hasattr(args[0] if args else None, 'processing_progress'):
                setattr(args[0], 'processing_progress', (step + 1) / steps)

        return original_method(*args, **kwargs)

    def _simulate_queue_backlog(self, original_method: Callable, delay_time: float, args: tuple, kwargs: dict) -> Any:
        """Simulate queue waiting time."""
        queue_position = random.randint(1, 10)
        time_per_position = delay_time / queue_position

        for position in range(queue_position, 0, -1):
            logger.debug(f"Queue position: {position}")
            time.sleep(time_per_position)

            # Simulate queue jumping (priority handling)
            if random.random() < 0.1:  # 10% chance of priority processing
                logger.debug("Priority processing - jumping queue")
                break

        return original_method(*args, **kwargs)

    def _simulate_bandwidth_limitation(self, original_method: Callable, delay_time: float, args: tuple, kwargs: dict) -> Any:
        """Simulate bandwidth limitations."""
        # Simulate data transfer in chunks
        data_chunks = 8
        chunk_delay = delay_time / data_chunks

        for chunk in range(data_chunks):
            time.sleep(chunk_delay)
            logger.debug(f"Transferring data chunk {chunk + 1}/{data_chunks}")

            # Simulate bandwidth fluctuation
            if random.random() < 0.2:  # 20% chance of slowdown
                time.sleep(chunk_delay * 0.5)  # Additional delay

        return original_method(*args, **kwargs)

    def _test_timeout_handling(self, target: Any, method_name: str, delay_time: float) -> bool:
        """Test if the agent handles timeouts properly."""
        # Check if agent has timeout configuration
        timeout_attrs = ['timeout', 'request_timeout', 'max_wait_time', 'deadline']

        for attr_name in timeout_attrs:
            if hasattr(target, attr_name):
                timeout_value = getattr(target, attr_name)
                if isinstance(timeout_value, (int, float)):
                    if delay_time > timeout_value:
                        # Agent should timeout
                        logger.debug(f"Expected timeout: delay {delay_time}s > timeout {timeout_value}s")
                        return True

        # Check if agent has timeout handling methods
        timeout_methods = ['handle_timeout', 'on_timeout', 'timeout_callback', 'abort_on_timeout']

        for method_name in timeout_methods:
            if hasattr(target, method_name):
                try:
                    timeout_handler = getattr(target, method_name)
                    result = timeout_handler()
                    logger.debug(f"Timeout handler {method_name} returned: {result}")
                    return True
                except Exception as e:
                    logger.debug(f"Timeout handler {method_name} failed: {e}")

        return False

    def _test_concurrent_operations(self, target: Any, observations: List[str]) -> bool:
        """Test if agent can handle concurrent operations during delays."""
        if not hasattr(target, 'generate_reply'):
            observations.append("Cannot test concurrency - no generate_reply method")
            return False

        # Test concurrent execution
        def delayed_operation():
            time.sleep(2.0)  # Simulate delay
            return "delayed_result"

        def quick_operation():
            if hasattr(target, 'generate_reply'):
                return target.generate_reply("quick test")
            return "quick_result"

        try:
            with ThreadPoolExecutor(max_workers=2) as executor:
                # Start delayed operation
                delayed_future = executor.submit(delayed_operation)

                # Start quick operation
                quick_future = executor.submit(quick_operation)

                # Check if quick operation completes before delayed one
                try:
                    quick_result = quick_future.result(timeout=1.0)
                    observations.append("Agent handled concurrent quick operation during delay")
                    return True
                except FutureTimeoutError:
                    observations.append("Agent blocked on concurrent operations")
                    return False

        except Exception as e:
            observations.append(f"Concurrency test failed: {e}")
            return False

    def _test_progressive_timeouts(self, target: Any, observations: List[str]):
        """Test progressive timeout handling."""
        timeout_attrs = ['timeout', 'request_timeout', 'max_wait_time']

        for attr_name in timeout_attrs:
            if hasattr(target, attr_name):
                original_timeout = getattr(target, attr_name)

                # Test with progressively shorter timeouts
                test_timeouts = [0.5, 1.0, 2.0]

                for test_timeout in test_timeouts:
                    setattr(target, attr_name, test_timeout)

                    # Check if agent respects the timeout
                    start_time = time.time()

                    # Simulate operation that might timeout
                    if hasattr(target, 'check_timeout'):
                        try:
                            target.check_timeout()
                            elapsed = time.time() - start_time

                            if elapsed < test_timeout + 0.5:  # Allow some margin
                                observations.append(f"Agent respected {test_timeout}s timeout")
                            else:
                                observations.append(f"Agent did not respect {test_timeout}s timeout")
                        except Exception as e:
                            observations.append(f"Timeout check failed: {e}")

                # Restore original timeout
                setattr(target, attr_name, original_timeout)
                break

    def _test_queue_handling(self, target: Any, observations: List[str]):
        """Test queue and backlog handling."""
        queue_attrs = ['queue', 'request_queue', 'pending_requests', 'backlog']

        queue_found = False
        for attr_name in queue_attrs:
            if hasattr(target, attr_name):
                queue_found = True
                observations.append(f"Agent has queue: {attr_name}")

                # Test queue management
                if hasattr(target, 'process_queue') or hasattr(target, 'handle_backlog'):
                    processor = getattr(target, 'process_queue', None) or getattr(target, 'handle_backlog')
                    try:
                        result = processor()
                        observations.append(f"Queue processing result: {result}")
                    except Exception as e:
                        observations.append(f"Queue processing failed: {e}")

                break

        if not queue_found:
            observations.append("Agent has no explicit queue management")

    def _test_graceful_degradation(self, target: Any, observations: List[str]):
        """Test graceful degradation under high latency."""
        # Check if agent has fallback mechanisms
        fallback_attrs = ['fallback_mode', 'degraded_service', 'reduced_functionality']
        fallback_methods = ['enable_fallback', 'degrade_gracefully', 'reduce_functionality']

        degradation_found = False

        for attr_name in fallback_attrs:
            if hasattr(target, attr_name):
                degradation_found = True
                observations.append(f"Agent has degradation capability: {attr_name}")

        for method_name in fallback_methods:
            if hasattr(target, method_name):
                degradation_found = True
                observations.append(f"Agent has degradation method: {method_name}")

                try:
                    method = getattr(target, method_name)
                    result = method()
                    observations.append(f"Graceful degradation result: {result}")
                except Exception as e:
                    observations.append(f"Graceful degradation failed: {e}")

        if not degradation_found:
            observations.append("Agent lacks graceful degradation mechanisms")
