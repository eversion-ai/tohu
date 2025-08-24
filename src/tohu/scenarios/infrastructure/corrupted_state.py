"""
Corrupted State and Memory scenario for testing agent resilience to data corruption.

This scenario intentionally corrupts or deletes parts of an agent's persisted state
to test how well it can detect and recover from data corruption.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Callable, Union
import logging
import random
import json
import copy

from tohu.core.scenario import ChaosScenario

logger = logging.getLogger(__name__)


@dataclass
class CorruptedStateScenario(ChaosScenario):
    """
    Tests an agent's resilience to corrupted or missing state/memory data.

    This scenario simulates data corruption in the agent's persistent state,
    such as conversation history, memory banks, or cached data. It tests
    whether the agent can detect inconsistencies and attempt recovery.
    """

    name: str = "Corrupted State and Memory Test"
    description: str = "Tests agent's resilience to data corruption in persistent state."

    # Configuration options
    corruption_probability: float = 0.3  # Probability of corrupting state access
    corruption_types: List[str] = field(default_factory=list)
    partial_corruption: bool = True  # Whether to corrupt only parts vs. entire state
    recovery_testing: bool = True  # Whether to test recovery mechanisms

    # State tracking
    original_methods: Dict[Any, Dict[str, Callable]] = field(default_factory=dict)
    corruptions_applied: List[Dict[str, Any]] = field(default_factory=list)

    def __post_init__(self):
        """Initialize the scenario with default corruption types if none provided."""
        super().__post_init__()
        if not self.corruption_types:
            self.corruption_types = [
                "missing_data",        # Delete parts of the state
                "invalid_json",        # Corrupt JSON structure
                "wrong_types",         # Change data types unexpectedly
                "inconsistent_refs",   # Break references between data
                "truncated_data",      # Cut off data mid-stream
                "duplicate_entries",   # Add duplicate or conflicting entries
                "timestamp_corruption", # Corrupt timestamps/ordering
                "encoding_errors",     # Introduce encoding issues
                "schema_violations",   # Violate expected data schema
                "partial_writes"       # Simulate incomplete write operations
            ]

    def setup(self) -> None:
        """Prepare the corrupted state scenario."""
        logger.info("Setting up Corrupted State scenario")
        self.original_methods = {}
        self.corruptions_applied = []

    def _corrupt_data(self, data: Any, corruption_type: str) -> Any:
        """
        Apply a specific type of corruption to data.

        Args:
            data: The original data to corrupt
            corruption_type: The type of corruption to apply

        Returns:
            The corrupted data
        """
        if data is None:
            return data

        corrupted = copy.deepcopy(data)

        if corruption_type == "missing_data":
            # Delete random parts of the data
            if isinstance(corrupted, dict):
                if corrupted:  # Only if dict is not empty
                    keys_to_remove = random.sample(
                        list(corrupted.keys()),
                        max(1, len(corrupted) // 3)
                    )
                    for key in keys_to_remove:
                        del corrupted[key]
            elif isinstance(corrupted, list):
                if corrupted:  # Only if list is not empty
                    indices_to_remove = sorted(
                        random.sample(range(len(corrupted)),
                                    max(1, len(corrupted) // 3)),
                        reverse=True
                    )
                    for idx in indices_to_remove:
                        del corrupted[idx]
            elif isinstance(corrupted, str):
                if len(corrupted) > 10:
                    # Remove random chunks
                    chunk_size = len(corrupted) // 4
                    start = random.randint(0, len(corrupted) - chunk_size)
                    corrupted = corrupted[:start] + corrupted[start + chunk_size:]

        elif corruption_type == "invalid_json":
            # If it's a string that looks like JSON, corrupt it
            if isinstance(corrupted, str):
                try:
                    # Try to parse as JSON to see if it's JSON-like
                    json.loads(corrupted)
                    # If successful, corrupt the JSON
                    corrupted = corrupted.replace('"', "'").replace("{", "[").replace("}", "]")
                except (json.JSONDecodeError, ValueError):
                    # Not JSON, corrupt as regular string
                    corrupted = corrupted.replace(" ", "}{").replace(",", "}{")
            elif isinstance(corrupted, (dict, list)):
                # Convert to JSON string and then corrupt it
                json_str = json.dumps(corrupted)
                corrupted = json_str.replace('"', "'").replace("{", "[")

        elif corruption_type == "wrong_types":
            # Change data types unexpectedly
            if isinstance(corrupted, dict):
                for key, value in list(corrupted.items()):
                    if isinstance(value, str) and value.isdigit():
                        corrupted[key] = int(value)  # String to int
                    elif isinstance(value, int):
                        corrupted[key] = str(value)  # Int to string
                    elif isinstance(value, bool):
                        corrupted[key] = int(value)  # Bool to int
                    elif isinstance(value, list) and len(value) == 1:
                        corrupted[key] = value[0]  # List to single item
            elif isinstance(corrupted, list):
                # Convert list to dict with indices as keys
                corrupted = {str(i): item for i, item in enumerate(corrupted)}
            elif isinstance(corrupted, str):
                # Try to convert string to number if possible
                try:
                    corrupted = float(corrupted)
                except ValueError:
                    # If not a number, convert to list of characters
                    corrupted = list(corrupted)

        elif corruption_type == "inconsistent_refs":
            # Break references between data (for structured data)
            if isinstance(corrupted, dict):
                # Look for ID-like fields and corrupt them
                for key, value in corrupted.items():
                    if ("id" in key.lower() or "ref" in key.lower()) and isinstance(value, str):
                        # Corrupt the ID
                        corrupted[key] = value + "_CORRUPTED"
                    elif isinstance(value, dict):
                        # Recursively corrupt nested objects
                        corrupted[key] = self._corrupt_data(value, corruption_type)

        elif corruption_type == "truncated_data":
            # Cut off data as if a write operation was interrupted
            if isinstance(corrupted, str):
                if len(corrupted) > 20:
                    truncate_point = random.randint(10, len(corrupted) - 10)
                    corrupted = corrupted[:truncate_point]
            elif isinstance(corrupted, list):
                if len(corrupted) > 3:
                    truncate_point = random.randint(1, len(corrupted) - 1)
                    corrupted = corrupted[:truncate_point]
            elif isinstance(corrupted, dict):
                # Remove random keys as if write was interrupted
                keys = list(corrupted.keys())
                if len(keys) > 2:
                    keep_count = random.randint(1, len(keys) - 1)
                    keys_to_keep = random.sample(keys, keep_count)
                    corrupted = {k: v for k, v in corrupted.items() if k in keys_to_keep}

        elif corruption_type == "duplicate_entries":
            # Add duplicate or conflicting entries
            if isinstance(corrupted, list):
                if corrupted:
                    # Duplicate some existing items
                    items_to_duplicate = random.sample(corrupted, min(2, len(corrupted)))
                    corrupted.extend(items_to_duplicate)
            elif isinstance(corrupted, dict):
                # Add conflicting keys
                for key in list(corrupted.keys())[:2]:  # Only first 2 keys
                    corrupted[key + "_duplicate"] = corrupted[key]
                    # Also add a conflicting value
                    if isinstance(corrupted[key], str):
                        corrupted[key + "_conflict"] = "CONFLICTING_" + corrupted[key]

        elif corruption_type == "timestamp_corruption":
            # Corrupt timestamp-like data
            if isinstance(corrupted, dict):
                timestamp_keys = ["timestamp", "created_at", "updated_at", "time", "date"]
                for key, value in corrupted.items():
                    if any(ts_key in key.lower() for ts_key in timestamp_keys):
                        if isinstance(value, (int, float)):
                            # Corrupt numeric timestamp
                            corrupted[key] = value + random.randint(-1000000, 1000000)
                        elif isinstance(value, str):
                            # Corrupt string timestamp
                            corrupted[key] = "INVALID_DATE_" + value

        elif corruption_type == "encoding_errors":
            # Introduce encoding-like errors
            if isinstance(corrupted, str):
                # Replace some characters with encoding error markers
                chars = list(corrupted)
                for i in random.sample(range(len(chars)), min(3, len(chars))):
                    chars[i] = "�"  # Unicode replacement character
                corrupted = "".join(chars)
            elif isinstance(corrupted, dict):
                # Corrupt string values in the dict
                for key, value in corrupted.items():
                    if isinstance(value, str) and len(value) > 5:
                        chars = list(value)
                        for i in random.sample(range(len(chars)), min(2, len(chars))):
                            chars[i] = "�"
                        corrupted[key] = "".join(chars)

        elif corruption_type == "schema_violations":
            # Violate expected data schema
            if isinstance(corrupted, dict):
                # Add unexpected fields
                corrupted["__CORRUPTED_FIELD__"] = "UNEXPECTED_DATA"
                corrupted["__INVALID_KEY__"] = {"nested": "corruption"}

                # Remove required-looking fields
                required_looking_keys = [k for k in corrupted.keys()
                                       if any(req in k.lower() for req in ["id", "name", "type"])]
                if required_looking_keys:
                    key_to_remove = random.choice(required_looking_keys)
                    del corrupted[key_to_remove]

        elif corruption_type == "partial_writes":
            # Simulate incomplete write operations
            if isinstance(corrupted, dict):
                # Add incomplete nested structures
                corrupted["__INCOMPLETE__"] = {"partial": True, "data": None}
                # Leave some values as None unexpectedly
                for key in random.sample(list(corrupted.keys()), min(2, len(corrupted))):
                    if not key.startswith("__"):  # Don't overwrite our marker
                        corrupted[key] = None

        return corrupted

    def _create_state_interceptor(self, original_fn: Callable, method_name: str) -> Callable:
        """
        Create a wrapper around state access methods that occasionally corrupts data.

        Args:
            original_fn: The original method
            method_name: The name of the method being intercepted

        Returns:
            A wrapped function that may return corrupted state
        """
        def intercepted_fn(*args, **kwargs):
            # Call the original method first
            result = original_fn(*args, **kwargs)

            # Decide whether to corrupt this access
            if random.random() < self.corruption_probability:
                # Choose a corruption type
                corruption_type = random.choice(self.corruption_types)

                # Apply corruption
                if self.partial_corruption and isinstance(result, (dict, list)) and result:
                    # Only corrupt part of the data
                    if isinstance(result, dict):
                        # Corrupt a random subset of keys
                        keys_to_corrupt = random.sample(
                            list(result.keys()),
                            max(1, len(result) // 3)
                        )
                        corrupted_result = copy.deepcopy(result)
                        for key in keys_to_corrupt:
                            corrupted_result[key] = self._corrupt_data(result[key], corruption_type)
                    else:  # list
                        # Corrupt a random subset of items
                        indices_to_corrupt = random.sample(
                            range(len(result)),
                            max(1, len(result) // 3)
                        )
                        corrupted_result = copy.deepcopy(result)
                        for idx in indices_to_corrupt:
                            corrupted_result[idx] = self._corrupt_data(result[idx], corruption_type)
                else:
                    # Corrupt the entire result
                    corrupted_result = self._corrupt_data(result, corruption_type)

                # Log the corruption
                corruption_record = {
                    "method": method_name,
                    "corruption_type": corruption_type,
                    "original_type": type(result).__name__,
                    "corrupted_type": type(corrupted_result).__name__,
                    "partial": self.partial_corruption and isinstance(result, (dict, list))
                }

                self.corruptions_applied.append(corruption_record)
                logger.info(f"Applied {corruption_type} corruption to {method_name}")

                return corrupted_result

            # No corruption
            return result

        return intercepted_fn

    def intercept_state_method(self, target: Any, method_name: str) -> None:
        """
        Intercept a state access method on the target.

        Args:
            target: The object containing the method
            method_name: The name of the method to intercept
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
            interceptor = self._create_state_interceptor(
                self.original_methods[target][method_name],
                method_name
            )
            setattr(target, method_name, interceptor)

            logger.info(f"Intercepted state method {method_name} on {target.__class__.__name__}")

    def restore_methods(self) -> None:
        """Restore all intercepted methods to their original implementations."""
        for target, methods in self.original_methods.items():
            for method_name, original_method in methods.items():
                setattr(target, method_name, original_method)
                logger.info(f"Restored original {method_name} on {target.__class__.__name__}")

    def run(self, target: Any) -> Dict[str, Any]:
        """
        Execute the corrupted state scenario against the target system.

        Args:
            target: The target agent or system to test

        Returns:
            A dictionary containing test results and observations
        """
        self.setup()

        # Reset tracking for this run
        self.corruptions_applied = []

        # Record observations
        observations = []
        success = False
        details = {
            "scenario_type": self.__class__.__name__,
            "methods_intercepted": [],
            "corruptions_applied": 0,
            "corruption_types_used": set(),
            "recovery_detected": False,
            "errors_handled": 0,
            "corruption_details": []
        }

        try:
            # Identify state/memory access methods to intercept
            # These vary by framework but commonly include:
            state_methods = [
                # Memory/state retrieval
                "get_memory", "load_state", "get_conversation_history",
                "retrieve_memory", "get_context", "load_context",

                # Cache access
                "get_cache", "load_cache", "retrieve_cached",

                # Database/storage access
                "get_data", "load_data", "fetch_data", "query",

                # Generic getters that might access persistent state
                "get", "load", "fetch", "retrieve"
            ]

            for method_name in state_methods:
                if hasattr(target, method_name) and callable(getattr(target, method_name)):
                    self.intercept_state_method(target, method_name)
                    details["methods_intercepted"].append(method_name)

            # Also check for state-like attributes that might have methods
            for attr_name in dir(target):
                if attr_name.startswith("_"):
                    continue

                # Look for attributes that suggest state/memory storage
                state_indicators = ["memory", "state", "context", "history", "cache", "store"]
                if any(indicator in attr_name.lower() for indicator in state_indicators):
                    attr = getattr(target, attr_name)

                    # Check if this attribute has methods we can intercept
                    for method_name in state_methods:
                        if hasattr(attr, method_name) and callable(getattr(attr, method_name)):
                            self.intercept_state_method(attr, method_name)
                            details["methods_intercepted"].append(f"{attr_name}.{method_name}")

            if not details["methods_intercepted"]:
                observations.append("Could not identify any state/memory access methods to intercept")
                observations.append("The agent may not use detectable persistent state mechanisms")
                return {
                    "success": False,
                    "observations": observations,
                    "details": details
                }

            observations.append(f"Intercepted {len(details['methods_intercepted'])} state access methods")

            # Provide guidance on testing
            observations.append(
                "To test: Use the agent normally and this scenario will automatically "
                "corrupt state access. Observe how the agent handles the corruption."
            )

            if self.recovery_testing:
                observations.append(
                    "Watch for signs of recovery: error handling, state validation, "
                    "fallback mechanisms, or attempts to reconstruct missing data."
                )

            # If corruptions have been applied during setup, analyze them
            if self.corruptions_applied:
                details["corruptions_applied"] = len(self.corruptions_applied)
                details["corruption_types_used"] = set(c["corruption_type"] for c in self.corruptions_applied)
                details["corruption_details"] = self.corruptions_applied

                observations.append(f"Applied {details['corruptions_applied']} corruptions during testing")
                observations.append(f"Corruption types used: {', '.join(details['corruption_types_used'])}")

                # Basic success if we were able to intercept and apply corruptions
                success = True
            else:
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
