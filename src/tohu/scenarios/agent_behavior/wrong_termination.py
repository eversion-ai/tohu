"""
Wrong Output Criteria or Termination Chaos Scenario.

This scenario tests an agent's goal-completion logic by providing
impossible, ambiguous, or incorrect termination conditions.
"""

import random
import time
import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union, Callable

from tohu.core.scenario import ChaosScenario

logger = logging.getLogger(__name__)


@dataclass
class WrongTerminationScenario(ChaosScenario):
    """
    Modifies termination conditions to test goal-completion logic.

    This scenario tests how agents handle impossible, ambiguous, or incorrect
    success criteria, and whether they can recognize failure conditions
    and avoid infinite loops.
    """

    corruption_rate: float = 0.4
    """Probability of corrupting termination criteria (0.0 to 1.0)"""

    corruption_types: List[str] = None
    """Types of termination corruption to apply"""

    timeout_threshold: float = 10.0
    """Maximum time to wait before considering a test failed (seconds)"""

    monitor_loops: bool = True
    """Whether to monitor for infinite loops"""

    def __post_init__(self):
        if self.corruption_types is None:
            self.corruption_types = [
                'impossible_criteria',
                'ambiguous_criteria',
                'premature_termination',
                'never_terminating',
                'contradictory_goals',
                'invalid_success_metrics'
            ]

    def run(self, target: Any) -> Dict[str, Any]:
        """Apply wrong termination chaos to the target."""
        logger.info(f"Starting WrongTerminationScenario with {self.corruption_rate*100}% corruption rate")

        observations = []
        corruptions_applied = 0
        loop_detections = 0
        timeout_recoveries = 0
        original_methods = {}
        original_attributes = {}

        try:
            # Intercept termination and goal-checking methods
            termination_methods = [
                'is_done', 'is_complete', 'should_terminate', 'check_completion',
                'evaluate_success', 'check_goal', 'is_finished', 'has_succeeded',
                'meets_criteria', 'task_complete', 'goal_achieved'
            ]

            for method_name in termination_methods:
                if hasattr(target, method_name):
                    original_method = getattr(target, method_name)
                    original_methods[method_name] = original_method

                    def create_corrupted_termination(orig_method, method_name):
                        def corrupted_termination(*args, **kwargs):
                            nonlocal corruptions_applied, loop_detections, timeout_recoveries

                            if random.random() < self.corruption_rate:
                                corruptions_applied += 1
                                corruption_type = random.choice(self.corruption_types)

                                logger.warning(f"🔥 CHAOS: Corrupting {method_name} with {corruption_type}")
                                observations.append(f"Applied {corruption_type} to {method_name}")

                                # Apply specific corruption
                                return self._apply_termination_corruption(
                                    orig_method, corruption_type, args, kwargs, method_name
                                )

                            return orig_method(*args, **kwargs)

                        return corrupted_termination

                    setattr(target, method_name, create_corrupted_termination(original_method, method_name))
                    logger.debug(f"Intercepted {method_name} for termination corruption")

            # Corrupt termination-related attributes
            self._corrupt_termination_attributes(target, observations, original_attributes)

            # Test loop detection and recovery
            if self.monitor_loops:
                self._test_loop_detection(target, observations)

            # Test timeout handling
            timeout_success = self._test_timeout_handling(target, observations)
            if timeout_success:
                timeout_recoveries += 1

            # Test goal recognition
            self._test_goal_recognition(target, observations)

            # Evaluate results
            success = (
                corruptions_applied > 0 and
                timeout_recoveries > 0 and
                not self._detected_infinite_loop(target)
            )

            if corruptions_applied == 0:
                observations.append("No termination methods found to corrupt")
                success = False

            result = {
                'success': success,
                'observations': observations,
                'corruptions_applied': corruptions_applied,
                'loop_detections': loop_detections,
                'timeout_recoveries': timeout_recoveries,
                'scenario': 'WrongTerminationScenario'
            }

            logger.info(f"WrongTerminationScenario completed: {result}")
            return result

        except Exception as e:
            logger.error(f"WrongTerminationScenario failed: {e}")
            return {
                'success': False,
                'observations': [f"Scenario execution failed: {str(e)}"],
                'error': str(e),
                'scenario': 'WrongTerminationScenario'
            }

        finally:
            # Restore original methods and attributes
            for method_name, original_method in original_methods.items():
                if hasattr(target, method_name):
                    setattr(target, method_name, original_method)
                    logger.debug(f"Restored original {method_name}")

            for attr_name, original_value in original_attributes.items():
                if hasattr(target, attr_name):
                    setattr(target, attr_name, original_value)
                    logger.debug(f"Restored original {attr_name}")

    def _apply_termination_corruption(self, original_method: Callable, corruption_type: str,
                                    args: tuple, kwargs: dict, method_name: str) -> Any:
        """Apply specific termination corruption."""

        try:
            if corruption_type == 'impossible_criteria':
                # Always return False (never complete)
                logger.warning("Returning impossible termination criteria (never complete)")
                return False

            elif corruption_type == 'ambiguous_criteria':
                # Return random boolean
                result = random.choice([True, False])
                logger.warning(f"Returning ambiguous criteria: {result}")
                return result

            elif corruption_type == 'premature_termination':
                # Always return True (immediately complete)
                logger.warning("Returning premature termination (immediately complete)")
                return True

            elif corruption_type == 'never_terminating':
                # Return False and introduce delay to simulate infinite processing
                logger.warning("Simulating never-terminating condition")
                time.sleep(0.5)  # Small delay to simulate processing
                return False

            elif corruption_type == 'contradictory_goals':
                # Return opposite of what would be expected
                try:
                    original_result = original_method(*args, **kwargs)
                    contradictory_result = not original_result
                    logger.warning(f"Returning contradictory result: {contradictory_result} (was {original_result})")
                    return contradictory_result
                except:
                    return random.choice([True, False])

            elif corruption_type == 'invalid_success_metrics':
                # Return invalid types or values
                invalid_returns = [None, -1, "invalid", [], {}, float('inf')]
                invalid_result = random.choice(invalid_returns)
                logger.warning(f"Returning invalid success metric: {invalid_result}")
                return invalid_result

            else:
                return original_method(*args, **kwargs)

        except Exception as e:
            logger.warning(f"Termination corruption failed: {e}")
            return False

    def _corrupt_termination_attributes(self, target: Any, observations: List[str], original_attributes: Dict[str, Any]):
        """Corrupt termination-related attributes."""
        termination_attrs = [
            'success_criteria', 'goal', 'target_state', 'completion_threshold',
            'max_iterations', 'timeout', 'success_metric', 'done_condition',
            'stop_condition', 'termination_rule', 'exit_criteria'
        ]

        for attr_name in termination_attrs:
            if hasattr(target, attr_name):
                original_value = getattr(target, attr_name)
                original_attributes[attr_name] = original_value

                if random.random() < self.corruption_rate:
                    corruption_type = random.choice(self.corruption_types)

                    if corruption_type == 'impossible_criteria':
                        # Set impossible values
                        if attr_name == 'completion_threshold':
                            setattr(target, attr_name, float('inf'))
                        elif attr_name == 'max_iterations':
                            setattr(target, attr_name, -1)
                        elif attr_name == 'success_metric':
                            setattr(target, attr_name, "impossible_metric")
                        else:
                            setattr(target, attr_name, None)

                        observations.append(f"Set impossible {attr_name}")

                    elif corruption_type == 'contradictory_goals':
                        # Set contradictory values
                        contradictory_values = {
                            'success_criteria': 'failure_criteria',
                            'goal': 'anti_goal',
                            'target_state': 'opposite_state',
                            'completion_threshold': 0 if isinstance(original_value, (int, float)) and original_value > 0 else 1
                        }

                        new_value = contradictory_values.get(attr_name, "contradictory_value")
                        setattr(target, attr_name, new_value)
                        observations.append(f"Set contradictory {attr_name} to {new_value}")

    def _test_loop_detection(self, target: Any, observations: List[str]):
        """Test if the agent can detect infinite loops."""
        # Check if agent has loop detection mechanisms
        loop_detection_methods = [
            'detect_loop', 'check_for_cycles', 'monitor_progress',
            'track_states', 'cycle_detection', 'progress_monitor'
        ]

        for method_name in loop_detection_methods:
            if hasattr(target, method_name):
                observations.append(f"Agent has loop detection: {method_name}")
                try:
                    method = getattr(target, method_name)
                    # Test the detection method
                    result = method()
                    observations.append(f"Loop detection result: {result}")
                except Exception as e:
                    observations.append(f"Loop detection method {method_name} failed: {e}")

        # Check for state tracking attributes
        state_tracking_attrs = ['state_history', 'previous_states', 'action_history', 'decision_log']
        for attr_name in state_tracking_attrs:
            if hasattr(target, attr_name):
                observations.append(f"Agent tracks state: {attr_name}")

    def _test_timeout_handling(self, target: Any, observations: List[str]) -> bool:
        """Test if the agent handles timeouts properly."""
        timeout_attrs = ['timeout', 'max_time', 'time_limit', 'deadline']

        for attr_name in timeout_attrs:
            if hasattr(target, attr_name):
                original_timeout = getattr(target, attr_name)

                # Set a very short timeout
                setattr(target, attr_name, 0.1)
                observations.append(f"Set short timeout for {attr_name}")

                # Test if agent respects timeout
                start_time = time.time()

                # Check if agent has timeout checking
                if hasattr(target, 'check_timeout'):
                    try:
                        timeout_result = target.check_timeout()
                        elapsed = time.time() - start_time

                        if elapsed < 1.0:  # Should timeout quickly
                            observations.append("Agent properly handled timeout")
                            setattr(target, attr_name, original_timeout)  # Restore
                            return True
                        else:
                            observations.append("Agent did not respect timeout")
                    except Exception as e:
                        observations.append(f"Timeout check failed: {e}")

                # Restore original timeout
                setattr(target, attr_name, original_timeout)

        return False

    def _test_goal_recognition(self, target: Any, observations: List[str]):
        """Test if the agent can recognize valid vs invalid goals."""
        goal_attrs = ['goal', 'objective', 'target', 'mission']

        for attr_name in goal_attrs:
            if hasattr(target, attr_name):
                original_goal = getattr(target, attr_name)

                # Test with clearly invalid goal
                invalid_goals = [None, "", "impossible_goal", -1, [], {}]
                invalid_goal = random.choice(invalid_goals)

                setattr(target, attr_name, invalid_goal)
                observations.append(f"Set invalid goal: {invalid_goal}")

                # Check if agent validates goals
                if hasattr(target, 'validate_goal') or hasattr(target, 'check_goal_validity'):
                    validator = getattr(target, 'validate_goal', None) or getattr(target, 'check_goal_validity')
                    try:
                        is_valid = validator()
                        if not is_valid:
                            observations.append("Agent correctly identified invalid goal")
                        else:
                            observations.append("Agent failed to identify invalid goal")
                    except Exception as e:
                        observations.append(f"Goal validation failed: {e}")

                # Restore original goal
                setattr(target, attr_name, original_goal)

    def _detected_infinite_loop(self, target: Any) -> bool:
        """Check if an infinite loop was detected."""
        # Look for signs of infinite loops
        loop_indicators = ['loop_count', 'iteration_count', 'cycle_detected', 'stuck']

        for indicator in loop_indicators:
            if hasattr(target, indicator):
                value = getattr(target, indicator)
                if isinstance(value, bool) and value:
                    return True
                elif isinstance(value, (int, float)) and value > 100:  # Arbitrary high threshold
                    return True

        return False
