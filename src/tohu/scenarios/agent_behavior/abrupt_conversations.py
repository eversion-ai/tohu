"""
Abrupt Conversations Chaos Scenario.

This scenario tests state management, persistence, and recovery by
simulating connection drops and conversation interruptions.
"""

import random
import time
import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from tohu.core.scenario import ChaosScenario

logger = logging.getLogger(__name__)


@dataclass
class AbruptConversationsScenario(ChaosScenario):
    """
    Simulates sudden conversation interruptions and connection drops.

    This scenario tests an agent's ability to handle interrupted conversations,
    maintain state across disconnections, and resume tasks after interruptions.
    """

    interruption_rate: float = 0.4
    """Probability of interrupting a conversation (0.0 to 1.0)"""

    interruption_types: List[str] = None
    """Types of interruptions to simulate"""

    recovery_timeout: float = 5.0
    """Maximum time to wait for recovery (seconds)"""

    test_persistence: bool = True
    """Whether to test state persistence across interruptions"""

    def __post_init__(self):
        if self.interruption_types is None:
            self.interruption_types = [
                'connection_lost',
                'timeout',
                'user_disconnect',
                'system_restart',
                'network_error',
                'session_expired'
            ]

    def run(self, target: Any) -> Dict[str, Any]:
        """Apply abrupt conversation chaos to the target."""
        logger.info(f"Starting AbruptConversationsScenario with {self.interruption_rate*100}% interruption rate")

        observations = []
        interruptions_triggered = 0
        successful_recoveries = 0
        original_methods = {}
        stored_state = {}

        try:
            # Intercept conversation methods
            conversation_methods = [
                'generate_reply', 'send_message', 'receive_message',
                'process_input', 'handle_message', 'respond_to',
                'continue_conversation', 'chat', 'talk'
            ]

            for method_name in conversation_methods:
                if hasattr(target, method_name):
                    original_method = getattr(target, method_name)
                    original_methods[method_name] = original_method

                    def create_interrupted_method(orig_method, method_name):
                        def interrupted_method(*args, **kwargs):
                            nonlocal interruptions_triggered, successful_recoveries

                            # Store state before potential interruption
                            if self.test_persistence:
                                current_state = self._capture_agent_state(target)
                                stored_state[f'before_{method_name}'] = current_state

                            if random.random() < self.interruption_rate:
                                interruptions_triggered += 1
                                interruption_type = random.choice(self.interruption_types)

                                logger.warning(f"🔥 CHAOS: Interrupting {method_name} with {interruption_type}")
                                observations.append(f"Interrupted {method_name} with {interruption_type}")

                                # Simulate different types of interruptions
                                if interruption_type == 'connection_lost':
                                    self._simulate_connection_loss(target)
                                elif interruption_type == 'timeout':
                                    self._simulate_timeout(target)
                                elif interruption_type == 'user_disconnect':
                                    self._simulate_user_disconnect(target)
                                elif interruption_type == 'system_restart':
                                    self._simulate_system_restart(target)
                                elif interruption_type == 'network_error':
                                    self._simulate_network_error(target)
                                elif interruption_type == 'session_expired':
                                    self._simulate_session_expiry(target)

                                # Test recovery
                                recovery_success = self._test_recovery(target, method_name, args, kwargs, orig_method)
                                if recovery_success:
                                    successful_recoveries += 1
                                    observations.append(f"Successfully recovered from {interruption_type}")
                                else:
                                    observations.append(f"Failed to recover from {interruption_type}")

                                # Validate state consistency after recovery
                                if self.test_persistence and f'before_{method_name}' in stored_state:
                                    state_consistent = self._validate_state_consistency(
                                        target, stored_state[f'before_{method_name}']
                                    )
                                    if state_consistent:
                                        observations.append("State consistency maintained after interruption")
                                    else:
                                        observations.append("State consistency lost after interruption")

                                # After interruption handling, try to continue normally
                                try:
                                    return orig_method(*args, **kwargs)
                                except Exception as e:
                                    logger.warning(f"Method failed after interruption: {e}")
                                    observations.append(f"Post-interruption execution failed: {str(e)}")
                                    raise

                            # Normal execution
                            return orig_method(*args, **kwargs)

                        return interrupted_method

                    # Replace the method
                    setattr(target, method_name, create_interrupted_method(original_method, method_name))
                    logger.debug(f"Intercepted {method_name} for interruption testing")

            # Test conversation state management
            if hasattr(target, 'conversation_state') or hasattr(target, 'chat_history'):
                self._test_conversation_state_handling(target, observations)

            # Test session management
            if hasattr(target, 'session') or hasattr(target, 'session_id'):
                self._test_session_management(target, observations)

            # Evaluate results
            recovery_rate = successful_recoveries / max(interruptions_triggered, 1)
            success = recovery_rate >= 0.7 and interruptions_triggered > 0  # At least 70% recovery rate

            if interruptions_triggered == 0:
                observations.append("No conversation methods found to interrupt")
                success = False

            result = {
                'success': success,
                'observations': observations,
                'interruptions_triggered': interruptions_triggered,
                'successful_recoveries': successful_recoveries,
                'recovery_rate': recovery_rate,
                'scenario': 'AbruptConversationsScenario'
            }

            logger.info(f"AbruptConversationsScenario completed: {result}")
            return result

        except Exception as e:
            logger.error(f"AbruptConversationsScenario failed: {e}")
            return {
                'success': False,
                'observations': [f"Scenario execution failed: {str(e)}"],
                'error': str(e),
                'scenario': 'AbruptConversationsScenario'
            }

        finally:
            # Restore original methods
            for method_name, original_method in original_methods.items():
                if hasattr(target, method_name):
                    setattr(target, method_name, original_method)
                    logger.debug(f"Restored original {method_name}")

    def _capture_agent_state(self, target: Any) -> Dict[str, Any]:
        """Capture the current state of the agent."""
        state = {}

        # Common state attributes to capture
        state_attrs = [
            'conversation_state', 'chat_history', 'session_id', 'context',
            'memory', 'current_task', 'active_tools', 'user_preferences',
            'conversation_id', 'turn_count', 'last_message', 'pending_actions'
        ]

        for attr in state_attrs:
            if hasattr(target, attr):
                try:
                    value = getattr(target, attr)
                    state[attr] = str(value)  # Convert to string for comparison
                except Exception as e:
                    state[attr] = f"<error: {e}>"

        return state

    def _validate_state_consistency(self, target: Any, original_state: Dict[str, Any]) -> bool:
        """Check if the agent's state is consistent after interruption."""
        current_state = self._capture_agent_state(target)

        # Check critical state attributes
        critical_attrs = ['conversation_id', 'session_id', 'current_task']

        for attr in critical_attrs:
            if attr in original_state and attr in current_state:
                if original_state[attr] != current_state[attr]:
                    logger.warning(f"State inconsistency in {attr}: {original_state[attr]} -> {current_state[attr]}")
                    return False

        return True

    def _simulate_connection_loss(self, target: Any):
        """Simulate a connection loss."""
        if hasattr(target, 'connection') or hasattr(target, 'client'):
            # Temporarily disable connection
            connection_attr = 'connection' if hasattr(target, 'connection') else 'client'
            original_connection = getattr(target, connection_attr)
            setattr(target, connection_attr, None)
            time.sleep(0.5)  # Brief disconnection
            setattr(target, connection_attr, original_connection)

    def _simulate_timeout(self, target: Any):
        """Simulate a timeout."""
        # Add artificial delay
        time.sleep(self.recovery_timeout * 0.3)
        if hasattr(target, 'last_activity'):
            setattr(target, 'last_activity', time.time() - self.recovery_timeout - 1)

    def _simulate_user_disconnect(self, target: Any):
        """Simulate user disconnection."""
        if hasattr(target, 'user_connected'):
            setattr(target, 'user_connected', False)
            time.sleep(0.2)
            setattr(target, 'user_connected', True)

    def _simulate_system_restart(self, target: Any):
        """Simulate system restart."""
        # Clear temporary state
        temp_attrs = ['temp_data', 'cache', 'buffer', 'pending_messages']
        for attr in temp_attrs:
            if hasattr(target, attr):
                original_value = getattr(target, attr)
                setattr(target, attr, None)
                time.sleep(0.1)
                setattr(target, attr, original_value)

    def _simulate_network_error(self, target: Any):
        """Simulate network error."""
        if hasattr(target, 'network_status'):
            setattr(target, 'network_status', 'error')
            time.sleep(0.3)
            setattr(target, 'network_status', 'connected')

    def _simulate_session_expiry(self, target: Any):
        """Simulate session expiry."""
        if hasattr(target, 'session_expires_at'):
            # Set expiry to past time
            setattr(target, 'session_expires_at', time.time() - 1)
            time.sleep(0.1)
            # Restore future expiry
            setattr(target, 'session_expires_at', time.time() + 3600)

    def _test_recovery(self, target: Any, method_name: str, args: tuple, kwargs: dict, original_method) -> bool:
        """Test if the agent can recover from interruption."""
        try:
            # Wait a bit to simulate recovery time
            time.sleep(0.5)

            # Check if agent has recovery methods
            recovery_methods = ['recover', 'reconnect', 'resume', 'restore_state']
            for recovery_method in recovery_methods:
                if hasattr(target, recovery_method):
                    logger.info(f"Attempting recovery using {recovery_method}")
                    try:
                        getattr(target, recovery_method)()
                        return True
                    except Exception as e:
                        logger.warning(f"Recovery method {recovery_method} failed: {e}")

            # If no specific recovery method, test if normal operation resumes
            try:
                # Try a simple operation to test recovery
                if hasattr(target, 'generate_reply'):
                    test_result = target.generate_reply("test recovery")
                    return test_result is not None
                elif hasattr(target, 'status'):
                    return target.status != 'error'
                else:
                    return True  # Assume recovery if no clear way to test
            except Exception as e:
                logger.warning(f"Recovery test failed: {e}")
                return False

        except Exception as e:
            logger.error(f"Recovery testing failed: {e}")
            return False

    def _test_conversation_state_handling(self, target: Any, observations: List[str]):
        """Test how the agent handles conversation state during interruptions."""
        state_attr = 'conversation_state' if hasattr(target, 'conversation_state') else 'chat_history'

        if hasattr(target, state_attr):
            original_state = getattr(target, state_attr)

            # Simulate state corruption
            setattr(target, state_attr, None)
            observations.append("Simulated conversation state loss")

            # Check if agent detects and handles the loss
            time.sleep(0.2)
            current_state = getattr(target, state_attr)

            if current_state is not None:
                observations.append("Agent recovered conversation state")
            else:
                observations.append("Agent did not recover conversation state")

            # Restore original state
            setattr(target, state_attr, original_state)

    def _test_session_management(self, target: Any, observations: List[str]):
        """Test session management during interruptions."""
        session_attr = 'session' if hasattr(target, 'session') else 'session_id'

        if hasattr(target, session_attr):
            original_session = getattr(target, session_attr)

            # Simulate session invalidation
            setattr(target, session_attr, None)
            observations.append("Simulated session invalidation")

            # Check if agent creates new session or recovers old one
            time.sleep(0.2)
            current_session = getattr(target, session_attr)

            if current_session is not None:
                observations.append("Agent handled session recovery")
            else:
                observations.append("Agent did not handle session recovery")

            # Restore original session
            setattr(target, session_attr, original_session)
