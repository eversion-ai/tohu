"""
Wrong Context and Memory Management Chaos Scenario.

This scenario tests an agent's focus and memory management by overloading
context with irrelevant information or simulating memory leaks.
"""

import random
import time
import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from tohu.core.scenario import ChaosScenario

logger = logging.getLogger(__name__)


@dataclass
class WrongContextMemoryScenario(ChaosScenario):
    """
    Tests context window management and memory handling.

    This scenario overloads context with irrelevant information,
    simulates memory leaks, and tests the agent's ability to maintain
    focus and manage long-term operational stability.
    """

    context_pollution_rate: float = 0.4
    """Probability of polluting context (0.0 to 1.0)"""

    memory_corruption_rate: float = 0.3
    """Probability of corrupting memory (0.0 to 1.0)"""

    saturation_level: float = 0.8
    """Context saturation level before considering overloaded (0.0 to 1.0)"""

    simulate_memory_leaks: bool = True
    """Whether to simulate memory leak conditions"""

    max_irrelevant_content: int = 1000
    """Maximum amount of irrelevant content to inject (in characters)"""

    def run(self, target: Any) -> Dict[str, Any]:
        """Apply wrong context and memory chaos to the target."""
        logger.info(f"Starting WrongContextMemoryScenario")

        observations = []
        context_pollutions = 0
        memory_corruptions = 0
        leak_simulations = 0
        cleanup_successes = 0
        original_methods = {}
        original_attributes = {}

        try:
            # Intercept context management methods
            context_methods = [
                'get_context', 'set_context', 'update_context', 'add_to_context',
                'clear_context', 'manage_context', 'context_window', 'load_context'
            ]

            for method_name in context_methods:
                if hasattr(target, method_name):
                    original_method = getattr(target, method_name)
                    original_methods[method_name] = original_method

                    def create_polluted_context_method(orig_method, method_name):
                        def polluted_context_method(*args, **kwargs):
                            nonlocal context_pollutions

                            if random.random() < self.context_pollution_rate:
                                context_pollutions += 1

                                logger.warning(f"🔥 CHAOS: Polluting context in {method_name}")
                                observations.append(f"Applied context pollution to {method_name}")

                                # Get original context
                                try:
                                    original_result = orig_method(*args, **kwargs)
                                except Exception as e:
                                    logger.warning(f"Original context method failed: {e}")
                                    return None

                                # Apply context pollution
                                polluted_result = self._pollute_context(original_result)
                                return polluted_result

                            return orig_method(*args, **kwargs)

                        return polluted_context_method

                    setattr(target, method_name, create_polluted_context_method(original_method, method_name))
                    logger.debug(f"Intercepted {method_name} for context pollution")

            # Intercept memory management methods
            memory_methods = [
                'remember', 'forget', 'recall', 'store_memory', 'retrieve_memory',
                'update_memory', 'clear_memory', 'memory_cleanup', 'save_state'
            ]

            for method_name in memory_methods:
                if hasattr(target, method_name):
                    original_method = getattr(target, method_name)
                    original_methods[method_name] = original_method

                    def create_corrupted_memory_method(orig_method, method_name):
                        def corrupted_memory_method(*args, **kwargs):
                            nonlocal memory_corruptions

                            if random.random() < self.memory_corruption_rate:
                                memory_corruptions += 1

                                logger.warning(f"🔥 CHAOS: Corrupting memory in {method_name}")
                                observations.append(f"Applied memory corruption to {method_name}")

                                # Apply memory corruption
                                return self._corrupt_memory_operation(orig_method, args, kwargs)

                            return orig_method(*args, **kwargs)

                        return corrupted_memory_method

                    setattr(target, method_name, create_corrupted_memory_method(original_method, method_name))
                    logger.debug(f"Intercepted {method_name} for memory corruption")

            # Corrupt context and memory attributes
            self._corrupt_context_attributes(target, observations, original_attributes)
            self._corrupt_memory_attributes(target, observations, original_attributes)

            # Simulate memory leaks
            if self.simulate_memory_leaks:
                leak_success = self._simulate_memory_leaks(target, observations)
                if leak_success:
                    leak_simulations += 1

            # Test context overflow handling
            self._test_context_overflow(target, observations)

            # Test memory cleanup mechanisms
            cleanup_success = self._test_memory_cleanup(target, observations)
            if cleanup_success:
                cleanup_successes += 1

            # Test focus maintenance
            self._test_focus_maintenance(target, observations)

            # Evaluate results
            total_corruptions = context_pollutions + memory_corruptions + leak_simulations
            success = (
                total_corruptions > 0 and
                cleanup_successes > 0 and
                self._check_stability(target, observations)
            )

            if total_corruptions == 0:
                observations.append("No context or memory methods found to corrupt")
                success = False

            result = {
                'success': success,
                'observations': observations,
                'context_pollutions': context_pollutions,
                'memory_corruptions': memory_corruptions,
                'leak_simulations': leak_simulations,
                'cleanup_successes': cleanup_successes,
                'total_corruptions': total_corruptions,
                'scenario': 'WrongContextMemoryScenario'
            }

            logger.info(f"WrongContextMemoryScenario completed: {result}")
            return result

        except Exception as e:
            logger.error(f"WrongContextMemoryScenario failed: {e}")
            return {
                'success': False,
                'observations': [f"Scenario execution failed: {str(e)}"],
                'error': str(e),
                'scenario': 'WrongContextMemoryScenario'
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

    def _pollute_context(self, original_context: Any) -> Any:
        """Pollute context with irrelevant information."""
        if original_context is None:
            return self._generate_irrelevant_context()

        irrelevant_content = self._generate_irrelevant_context()

        # Handle different context types
        if isinstance(original_context, str):
            # Inject irrelevant text
            return f"{irrelevant_content}\\n\\n{original_context}\\n\\n{irrelevant_content}"

        elif isinstance(original_context, list):
            # Add irrelevant items
            irrelevant_items = self._generate_irrelevant_list_items()
            return irrelevant_items + original_context + irrelevant_items

        elif isinstance(original_context, dict):
            # Add irrelevant key-value pairs
            polluted_context = original_context.copy()
            irrelevant_dict = self._generate_irrelevant_dict()
            polluted_context.update(irrelevant_dict)
            return polluted_context

        else:
            # Unknown type, return with irrelevant wrapper
            return {
                'original': original_context,
                'irrelevant_data': self._generate_irrelevant_context(),
                'noise': self._generate_noise_data()
            }

    def _generate_irrelevant_context(self) -> str:
        """Generate irrelevant context content."""
        irrelevant_topics = [
            "The weather patterns in Antarctica during the summer months show interesting variations.",
            "Medieval cooking techniques involved the use of various herbs and spices that are now rare.",
            "The migration patterns of arctic terns cover distances of over 44,000 miles annually.",
            "Ancient Roman architecture demonstrates sophisticated understanding of engineering principles.",
            "The lifecycle of butterflies involves four distinct stages: egg, larva, pupa, and adult.",
            "Deep sea creatures have evolved unique adaptations to survive in extreme pressure environments.",
            "The history of paper manufacturing dates back to ancient China around 100 BCE.",
            "Musical instruments from different cultures show remarkable diversity in design and sound.",
            "Geological formations in mountain ranges provide insights into Earth's tectonic history.",
            "The development of written languages evolved independently in various civilizations."
        ]

        num_topics = random.randint(2, 5)
        selected_topics = random.sample(irrelevant_topics, min(num_topics, len(irrelevant_topics)))

        irrelevant_text = " ".join(selected_topics)

        # Truncate to max length
        if len(irrelevant_text) > self.max_irrelevant_content:
            irrelevant_text = irrelevant_text[:self.max_irrelevant_content] + "..."

        return irrelevant_text

    def _generate_irrelevant_list_items(self) -> List[str]:
        """Generate irrelevant list items."""
        irrelevant_items = [
            "banana recipe instructions",
            "17th century poetry analysis",
            "quantum physics equations",
            "gardening tips for roses",
            "historical facts about Vikings",
            "cooking temperature guidelines",
            "astronomy observation notes",
            "art history timeline",
            "geology field study data",
            "marine biology specimens"
        ]

        num_items = random.randint(3, 7)
        return random.sample(irrelevant_items, min(num_items, len(irrelevant_items)))

    def _generate_irrelevant_dict(self) -> Dict[str, Any]:
        """Generate irrelevant dictionary data."""
        return {
            'random_fact_1': "Octopuses have three hearts and blue blood",
            'random_fact_2': "A group of flamingos is called a flamboyance",
            'random_fact_3': "Honey never spoils or goes bad",
            'irrelevant_number': random.randint(1, 10000),
            'noise_data': ['x'] * random.randint(50, 200),
            'timestamp': time.time(),
            'random_string': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=100))
        }

    def _generate_noise_data(self) -> str:
        """Generate pure noise data."""
        noise_chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-=[]{}|;:,.<>?'
        noise_length = random.randint(100, 500)
        return ''.join(random.choices(noise_chars, k=noise_length))

    def _corrupt_memory_operation(self, original_method, args: tuple, kwargs: dict) -> Any:
        """Corrupt a memory operation."""
        corruption_strategies = [
            'return_wrong_data',
            'return_outdated_data',
            'return_corrupted_data',
            'return_empty',
            'cause_error'
        ]

        strategy = random.choice(corruption_strategies)

        try:
            if strategy == 'return_wrong_data':
                # Return completely unrelated data
                wrong_data = {
                    'wrong_key': 'wrong_value',
                    'corrupted': True,
                    'actual_data': 'this is not the data you are looking for'
                }
                return wrong_data

            elif strategy == 'return_outdated_data':
                # Return data with old timestamp
                outdated_data = {
                    'data': 'this data is from last week',
                    'timestamp': time.time() - 604800,  # 1 week ago
                    'outdated': True
                }
                return outdated_data

            elif strategy == 'return_corrupted_data':
                # Return partially corrupted data
                try:
                    original_result = original_method(*args, **kwargs)
                    if isinstance(original_result, dict):
                        corrupted = original_result.copy()
                        # Corrupt some values
                        for key in list(corrupted.keys())[:2]:
                            corrupted[key] = "CORRUPTED_DATA"
                        return corrupted
                    elif isinstance(original_result, str):
                        return "CORRUPTED: " + original_result[:50] + "...CORRUPTED"
                    else:
                        return f"CORRUPTED_MEMORY_DATA_{random.randint(1000, 9999)}"
                except:
                    return "CORRUPTED_MEMORY_DATA"

            elif strategy == 'return_empty':
                return None

            elif strategy == 'cause_error':
                raise Exception("Memory corruption error - data unavailable")

            else:
                return original_method(*args, **kwargs)

        except Exception as e:
            logger.warning(f"Memory corruption failed: {e}")
            return original_method(*args, **kwargs)

    def _corrupt_context_attributes(self, target: Any, observations: List[str], original_attributes: Dict[str, Any]):
        """Corrupt context-related attributes."""
        context_attrs = [
            'context', 'context_window', 'current_context', 'context_buffer',
            'prompt_context', 'conversation_context', 'working_context'
        ]

        for attr_name in context_attrs:
            if hasattr(target, attr_name):
                original_value = getattr(target, attr_name)
                original_attributes[attr_name] = original_value

                if random.random() < self.context_pollution_rate:
                    corrupted_context = self._pollute_context(original_value)
                    setattr(target, attr_name, corrupted_context)
                    observations.append(f"Corrupted context attribute: {attr_name}")

    def _corrupt_memory_attributes(self, target: Any, observations: List[str], original_attributes: Dict[str, Any]):
        """Corrupt memory-related attributes."""
        memory_attrs = [
            'memory', 'short_term_memory', 'long_term_memory', 'working_memory',
            'episodic_memory', 'semantic_memory', 'memory_buffer', 'memory_store'
        ]

        for attr_name in memory_attrs:
            if hasattr(target, attr_name):
                original_value = getattr(target, attr_name)
                original_attributes[attr_name] = original_value

                if random.random() < self.memory_corruption_rate:
                    # Corrupt memory content
                    if isinstance(original_value, dict):
                        corrupted_memory = original_value.copy()
                        corrupted_memory['corrupted_data'] = self._generate_noise_data()
                        corrupted_memory['memory_leak'] = ['leaked_data'] * 100
                    elif isinstance(original_value, list):
                        corrupted_memory = original_value + ['corrupted_entry'] * 50
                    else:
                        corrupted_memory = f"CORRUPTED_MEMORY: {original_value}"

                    setattr(target, attr_name, corrupted_memory)
                    observations.append(f"Corrupted memory attribute: {attr_name}")

    def _simulate_memory_leaks(self, target: Any, observations: List[str]) -> bool:
        """Simulate memory leak conditions."""
        # Create memory leak by adding large amounts of data
        leak_attrs = ['temp_storage', 'cache', 'buffer', 'accumulated_data']

        leak_created = False
        for attr_name in leak_attrs:
            if hasattr(target, attr_name) or random.random() < 0.5:
                # Create or expand existing attribute with large data
                large_data = ['memory_leak_data'] * 1000  # Simulate accumulated data

                if hasattr(target, attr_name):
                    existing_data = getattr(target, attr_name)
                    if isinstance(existing_data, list):
                        setattr(target, attr_name, existing_data + large_data)
                    else:
                        setattr(target, attr_name, large_data)
                else:
                    setattr(target, attr_name, large_data)

                observations.append(f"Simulated memory leak in {attr_name}")
                leak_created = True
                break

        return leak_created

    def _test_context_overflow(self, target: Any, observations: List[str]):
        """Test handling of context overflow."""
        context_attrs = ['context', 'context_window', 'prompt_context']

        for attr_name in context_attrs:
            if hasattr(target, attr_name):
                # Try to overflow context
                overflow_content = "OVERFLOW_DATA " * 500  # Large amount of data
                original_context = getattr(target, attr_name)

                if isinstance(original_context, str):
                    overflowed_context = original_context + overflow_content
                elif isinstance(original_context, list):
                    overflowed_context = original_context + ['OVERFLOW'] * 200
                else:
                    overflowed_context = overflow_content

                setattr(target, attr_name, overflowed_context)
                observations.append(f"Applied context overflow to {attr_name}")

                # Check if agent handles overflow
                if hasattr(target, 'handle_context_overflow') or hasattr(target, 'truncate_context'):
                    handler = getattr(target, 'handle_context_overflow', None) or getattr(target, 'truncate_context')
                    try:
                        handler()
                        observations.append(f"Agent handled context overflow in {attr_name}")
                    except Exception as e:
                        observations.append(f"Context overflow handling failed: {e}")

                break

    def _test_memory_cleanup(self, target: Any, observations: List[str]) -> bool:
        """Test memory cleanup mechanisms."""
        cleanup_methods = [
            'cleanup_memory', 'clear_cache', 'garbage_collect', 'free_memory',
            'compact_memory', 'optimize_memory', 'memory_management'
        ]

        for method_name in cleanup_methods:
            if hasattr(target, method_name):
                try:
                    cleanup_method = getattr(target, method_name)
                    cleanup_method()
                    observations.append(f"Successfully called cleanup method: {method_name}")
                    return True
                except Exception as e:
                    observations.append(f"Cleanup method {method_name} failed: {e}")

        observations.append("No memory cleanup mechanisms found")
        return False

    def _test_focus_maintenance(self, target: Any, observations: List[str]):
        """Test if agent maintains focus despite context pollution."""
        # Check if agent has focus-related attributes or methods
        focus_attrs = ['current_task', 'primary_goal', 'focus', 'objective']
        focus_methods = ['maintain_focus', 'refocus', 'check_focus', 'stay_on_task']

        focus_found = False
        for attr_name in focus_attrs:
            if hasattr(target, attr_name):
                focus_found = True
                observations.append(f"Agent tracks focus: {attr_name}")

        for method_name in focus_methods:
            if hasattr(target, method_name):
                focus_found = True
                observations.append(f"Agent has focus method: {method_name}")
                try:
                    method = getattr(target, method_name)
                    result = method()
                    observations.append(f"Focus method result: {result}")
                except Exception as e:
                    observations.append(f"Focus method {method_name} failed: {e}")

        if not focus_found:
            observations.append("Agent lacks explicit focus maintenance mechanisms")

    def _check_stability(self, target: Any, observations: List[str]) -> bool:
        """Check if the agent maintains stability after corruptions."""
        # Test basic operations to see if agent still functions
        try:
            # Check if agent can still perform basic operations
            if hasattr(target, 'status'):
                status = target.status
                if status and 'error' not in str(status).lower():
                    observations.append("Agent maintains stable status")
                    return True

            # Check if agent responds to simple queries
            if hasattr(target, 'generate_reply'):
                try:
                    response = target.generate_reply("test stability")
                    if response:
                        observations.append("Agent maintains response capability")
                        return True
                except Exception as e:
                    observations.append(f"Stability test failed: {e}")

            observations.append("Agent stability uncertain")
            return False

        except Exception as e:
            observations.append(f"Stability check failed: {e}")
            return False
