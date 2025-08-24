"""
Stupid Selectors Chaos Scenario.

This scenario tests an agent's decision-making and routing logic by forcing
suboptimal tool or sub-task selections to test error correction and recovery.
"""

import random
import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from tohu.core.scenario import ChaosScenario

logger = logging.getLogger(__name__)


@dataclass
class StupidSelectorsScenario(ChaosScenario):
    """
    Forces agents to make suboptimal tool or task selections.

    This scenario intercepts the agent's decision-making process and
    occasionally forces it to choose inappropriate tools or subtasks,
    testing the system's ability to detect and recover from bad choices.
    """

    bad_selection_rate: float = 0.3
    """Probability of forcing a bad selection (0.0 to 1.0)"""

    recovery_attempts: int = 3
    """Number of attempts before considering the test failed"""

    monitor_recovery: bool = True
    """Whether to monitor recovery attempts"""

    def run(self, target: Any) -> Dict[str, Any]:
        """Apply stupid selectors chaos to the target."""
        logger.info(f"Starting StupidSelectorsScenario with {self.bad_selection_rate*100}% bad selection rate")

        observations = []
        recovery_count = 0
        original_methods = {}

        try:
            # Intercept common selection methods
            selection_methods = [
                'select_tool', 'choose_tool', 'pick_tool',
                'select_action', 'choose_action', 'pick_action',
                'route_request', 'dispatch_task', 'delegate_task',
                'get_best_match', 'find_suitable_tool', 'match_intent'
            ]

            for method_name in selection_methods:
                if hasattr(target, method_name):
                    original_method = getattr(target, method_name)
                    original_methods[method_name] = original_method

                    def create_bad_selector(orig_method, method_name):
                        def bad_selector(*args, **kwargs):
                            nonlocal recovery_count

                            if random.random() < self.bad_selection_rate:
                                logger.warning(f"🔥 CHAOS: Forcing bad selection in {method_name}")
                                observations.append(f"Forced bad selection in {method_name}")

                                # Return a deliberately bad choice
                                if args:
                                    # If there are options, pick a random bad one
                                    if isinstance(args[0], (list, tuple)) and len(args[0]) > 1:
                                        options = list(args[0])
                                        # Remove the likely good choices (first few) and pick from the rest
                                        bad_options = options[len(options)//2:] if len(options) > 2 else options
                                        bad_choice = random.choice(bad_options)
                                        logger.warning(f"Selecting bad option: {bad_choice}")
                                        return bad_choice

                                # For kwargs-based selections, corrupt the criteria
                                if kwargs:
                                    corrupted_kwargs = kwargs.copy()
                                    if 'criteria' in corrupted_kwargs:
                                        corrupted_kwargs['criteria'] = 'random_bad_criteria'
                                    if 'priority' in corrupted_kwargs:
                                        corrupted_kwargs['priority'] = 'lowest'
                                    if 'score_threshold' in corrupted_kwargs:
                                        corrupted_kwargs['score_threshold'] = 0.0

                                    try:
                                        result = orig_method(*args, **corrupted_kwargs)
                                        return result
                                    except Exception as e:
                                        logger.warning(f"Bad selection caused error: {e}")
                                        observations.append(f"Bad selection error: {str(e)}")
                                        recovery_count += 1

                                # Fallback: return None or empty to force handling
                                logger.warning("Returning None to force error handling")
                                return None

                            # Normal execution
                            return orig_method(*args, **kwargs)

                        return bad_selector

                    # Replace the method
                    setattr(target, method_name, create_bad_selector(original_method, method_name))
                    logger.debug(f"Intercepted {method_name} for bad selection testing")

            # Also intercept decision-making attributes if they exist
            decision_attrs = ['current_tool', 'selected_action', 'active_strategy']
            for attr_name in decision_attrs:
                if hasattr(target, attr_name):
                    original_value = getattr(target, attr_name)

                    if random.random() < self.bad_selection_rate:
                        logger.warning(f"🔥 CHAOS: Corrupting decision attribute {attr_name}")

                        # Set to a bad value
                        bad_values = ['wrong_tool', 'invalid_action', 'broken_strategy', None, '']
                        bad_value = random.choice(bad_values)
                        setattr(target, attr_name, bad_value)
                        observations.append(f"Corrupted {attr_name} to {bad_value}")

            # Test recovery mechanism if agent has error handling
            if hasattr(target, 'handle_error') or hasattr(target, 'recover_from_error'):
                error_handler = getattr(target, 'handle_error', None) or getattr(target, 'recover_from_error', None)
                if error_handler:
                    logger.info("Testing error recovery mechanism")
                    try:
                        # Simulate a selection error
                        fake_error = Exception("Tool selection failed - no suitable tool found")
                        result = error_handler(fake_error)
                        observations.append(f"Error recovery returned: {result}")
                    except Exception as e:
                        observations.append(f"Error recovery failed: {str(e)}")
                        recovery_count += 1

            # Check if the agent has any adaptive selection logic
            adaptive_methods = ['adapt_selection', 'learn_from_failure', 'update_strategy']
            for method_name in adaptive_methods:
                if hasattr(target, method_name):
                    logger.info(f"Found adaptive method: {method_name}")
                    observations.append(f"Agent has adaptive capability: {method_name}")

            # Evaluate the results
            success = recovery_count <= self.recovery_attempts

            if not success:
                observations.append(f"Too many recovery attempts: {recovery_count}/{self.recovery_attempts}")

            if len(observations) == 0:
                observations.append("No selection methods found to test")
                success = False

            result = {
                'success': success,
                'observations': observations,
                'recovery_attempts': recovery_count,
                'bad_selections_forced': len([obs for obs in observations if 'Forced bad selection' in obs]),
                'scenario': 'StupidSelectorsScenario'
            }

            logger.info(f"StupidSelectorsScenario completed: {result}")
            return result

        except Exception as e:
            logger.error(f"StupidSelectorsScenario failed: {e}")
            return {
                'success': False,
                'observations': [f"Scenario execution failed: {str(e)}"],
                'error': str(e),
                'scenario': 'StupidSelectorsScenario'
            }

        finally:
            # Restore original methods
            for method_name, original_method in original_methods.items():
                if hasattr(target, method_name):
                    setattr(target, method_name, original_method)
                    logger.debug(f"Restored original {method_name}")
