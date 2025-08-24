"""
Model Degradation scenario for testing agent performance with less capable models.

This scenario tests how well an agent can handle degraded model capabilities,
simulating what happens when a less capable model is used as a fallback.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Callable, Union
import logging
import random
import re

from tohu.core.scenario import ChaosScenario

logger = logging.getLogger(__name__)


@dataclass
class ModelDegradationScenario(ChaosScenario):
    """
    Tests an agent's ability to function with degraded model capabilities.

    This scenario simulates what happens when an agent must fall back to a less
    capable model, either due to service disruptions, cost optimization, or
    other factors. It tests whether the agent can still achieve its goals,
    perhaps less efficiently or with reduced quality.
    """

    name: str = "Model Degradation Test"
    description: str = "Tests agent's resilience to reduced model capabilities."

    # Configuration options
    degradation_level: float = 0.5  # 0.0 = no degradation, 1.0 = severe degradation
    degradation_types: List[str] = field(default_factory=list)
    degradation_consistency: float = 0.8  # How consistent the degradation is (vs. random)
    apply_to_system_messages: bool = False  # Whether to degrade system messages

    # Original methods and tracking
    original_methods: Dict[Any, Dict[str, Callable]] = field(default_factory=dict)

    def __post_init__(self):
        """Initialize the scenario with default degradation types if none provided."""
        super().__post_init__()
        if not self.degradation_types:
            self.degradation_types = [
                "truncate_response",     # Cut off responses early
                "reduce_reasoning",      # Remove step-by-step reasoning
                "introduce_mistakes",    # Add factual or logical errors
                "simplify_language",     # Use simpler vocabulary and grammar
                "reduce_creativity",     # Make responses more formulaic
                "ignore_nuance",         # Miss subtle aspects of the prompt
                "forget_context",        # Forget parts of the conversation history
                "misunderstand_intent"   # Misinterpret what the user is asking for
            ]

    def setup(self) -> None:
        """Prepare the model degradation scenario."""
        logger.info("Setting up Model Degradation scenario")
        self.original_methods = {}

    def _degrade_text(self, text: str, is_system_message: bool = False) -> str:
        """
        Apply degradation effects to text output from the model.

        Args:
            text: The original text to degrade
            is_system_message: Whether this is a system message

        Returns:
            The degraded text
        """
        # Don't degrade system messages unless configured to do so
        if is_system_message and not self.apply_to_system_messages:
            return text

        # Apply degradation based on level and consistency
        if random.random() > self.degradation_consistency:
            # Occasionally skip degradation for variance
            return text

        # Choose degradation types to apply based on level
        num_degradations = max(1, int(len(self.degradation_types) * self.degradation_level))
        degradations_to_apply = random.sample(self.degradation_types, num_degradations)

        degraded_text = text

        for degradation_type in degradations_to_apply:
            if degradation_type == "truncate_response":
                # Cut off the response early
                max_length = int(len(degraded_text) * (1.0 - self.degradation_level * 0.7))
                if max_length < len(degraded_text):
                    degraded_text = degraded_text[:max_length] + "..."

            elif degradation_type == "reduce_reasoning":
                # Remove step-by-step reasoning and explanations
                # Look for common reasoning patterns and remove them
                patterns = [
                    r"Let me think about this step by step:.*?(?=\n\n|\Z)",
                    r"Here's my reasoning:.*?(?=\n\n|\Z)",
                    r"To solve this, I'll:.*?(?=\n\n|\Z)",
                    r"Let's break this down:.*?(?=\n\n|\Z)"
                ]

                for pattern in patterns:
                    degraded_text = re.sub(pattern, "I'll solve this directly:", degraded_text,
                                        flags=re.DOTALL)

            elif degradation_type == "introduce_mistakes":
                # Add factual or logical errors
                # This is simplified - a real implementation would be more sophisticated
                if "correct" in degraded_text.lower():
                    degraded_text = degraded_text.replace("correct", "incorrect")
                if "true" in degraded_text.lower():
                    degraded_text = degraded_text.replace("true", "false")

                # Randomly change some numbers if present
                def replace_number(match):
                    num = int(match.group(0))
                    return str(num + random.randint(1, 5))

                degraded_text = re.sub(r'\b\d+\b', replace_number, degraded_text)

            elif degradation_type == "simplify_language":
                # Use simpler vocabulary and grammar
                # Replace sophisticated words with simpler alternatives
                replacements = {
                    "utilize": "use",
                    "implement": "do",
                    "consideration": "thought",
                    "subsequently": "then",
                    "furthermore": "also",
                    "nevertheless": "but",
                    "approximately": "about",
                    "sufficient": "enough",
                    "demonstrate": "show",
                    "terminate": "end"
                }

                for word, replacement in replacements.items():
                    degraded_text = re.sub(fr'\b{word}\b', replacement, degraded_text,
                                        flags=re.IGNORECASE)

                # Shorten sentences
                degraded_text = re.sub(r'([.!?]) (However|Furthermore|Nevertheless|Additionally|Consequently)',
                                    r'\1 But', degraded_text)

            elif degradation_type == "reduce_creativity":
                # Make responses more formulaic and less varied
                # Simplify lists and examples
                degraded_text = re.sub(r'For example:.*?(?=\n\n|\Z)',
                                    "For example: it works like that.",
                                    degraded_text, flags=re.DOTALL)

                # Replace creative expressions with basic ones
                degraded_text = re.sub(r'(?i)a (fascinating|intriguing|compelling) (aspect|point|feature)',
                                    r'an important thing', degraded_text)

            elif degradation_type == "ignore_nuance":
                # Miss subtle aspects of the prompt or context
                # Look for qualifiers and remove them
                degraded_text = re.sub(r'(?i)(somewhat|partially|occasionally|potentially|arguably)',
                                    '', degraded_text)

                # Remove "on one hand / on the other hand" patterns
                degraded_text = re.sub(r'(?i)on (the )?one hand.*?on the other hand',
                                    'simply put', degraded_text, flags=re.DOTALL)

            elif degradation_type == "forget_context":
                # Simulate forgetting parts of the conversation
                # Add phrases that indicate memory issues
                context_loss_phrases = [
                    "As mentioned earlier (though I don't recall the specifics)...",
                    "Without referring back to our previous discussion...",
                    "Setting aside what we discussed before...",
                    "To address your question directly (without considering our history)..."
                ]

                # Insert a context loss phrase at a paragraph break
                if "\n\n" in degraded_text and random.random() < 0.7:
                    parts = degraded_text.split("\n\n", 1)
                    degraded_text = parts[0] + "\n\n" + random.choice(context_loss_phrases) + "\n\n" + parts[1]

            elif degradation_type == "misunderstand_intent":
                # Misinterpret what the user is asking for
                intent_confusion_phrases = [
                    "If you're asking about X (though you might have meant Y)...",
                    "I'll assume you want to know about...",
                    "Your question is probably about...",
                    "I think what you're really asking is..."
                ]

                # Add a misunderstanding phrase near the beginning
                first_para_end = degraded_text.find("\n\n")
                if first_para_end > 0:
                    insert_pos = min(100, first_para_end)
                    degraded_text = degraded_text[:insert_pos] + "\n\n" + random.choice(intent_confusion_phrases) + "\n\n" + degraded_text[insert_pos:]

        return degraded_text

    def _create_degraded_method(self, original_fn: Callable) -> Callable:
        """
        Create a wrapper around the model's generation method that degrades outputs.

        Args:
            original_fn: The original method

        Returns:
            A wrapped function that produces degraded outputs
        """
        def degraded_method(*args, **kwargs):
            # Call the original method
            result = original_fn(*args, **kwargs)

            # Degrade the result based on its type and structure
            # This is framework-specific and would need to be adapted
            # Here's a general implementation that handles common patterns

            # Handle dictionary response (common in many frameworks)
            if isinstance(result, dict):
                # OpenAI-like format with 'content' field
                if "content" in result and isinstance(result["content"], str):
                    result["content"] = self._degrade_text(
                        result["content"],
                        is_system_message=(result.get("role") == "system")
                    )

                # LangChain-like format with 'text' field
                elif "text" in result and isinstance(result["text"], str):
                    result["text"] = self._degrade_text(result["text"])

                # Handle nested structures
                elif "output" in result and isinstance(result["output"], dict):
                    if "text" in result["output"] and isinstance(result["output"]["text"], str):
                        result["output"]["text"] = self._degrade_text(result["output"]["text"])

            # Handle string response
            elif isinstance(result, str):
                result = self._degrade_text(result)

            # Handle list response (e.g., multiple generations)
            elif isinstance(result, list):
                for i, item in enumerate(result):
                    if isinstance(item, str):
                        result[i] = self._degrade_text(item)
                    elif isinstance(item, dict) and "text" in item:
                        item["text"] = self._degrade_text(item["text"])

            return result

        return degraded_method

    def intercept_model(self, target: Any) -> None:
        """
        Intercept the model's generation methods to degrade outputs.

        Args:
            target: The model or agent to intercept
        """
        # Save target in original_methods if not already there
        if target not in self.original_methods:
            self.original_methods[target] = {}

        # Look for common model output methods across frameworks
        model_methods = [
            "generate", "complete", "chat", "predict", "generate_text",
            "__call__", "invoke"  # For function-like models
        ]

        intercepted = False

        for method_name in model_methods:
            if hasattr(target, method_name) and callable(getattr(target, method_name)):
                # Save original method
                if method_name not in self.original_methods[target]:
                    self.original_methods[target][method_name] = getattr(target, method_name)

                    # Replace with degraded version
                    degraded_method = self._create_degraded_method(self.original_methods[target][method_name])
                    setattr(target, method_name, degraded_method)

                    logger.info(f"Intercepted {method_name} on {target.__class__.__name__}")
                    intercepted = True

        if not intercepted:
            logger.warning(f"Could not identify any model methods to intercept on {target.__class__.__name__}")

    def restore_models(self) -> None:
        """Restore all intercepted model methods to their original implementations."""
        for target, methods in self.original_methods.items():
            for method_name, original_method in methods.items():
                setattr(target, method_name, original_method)
                logger.info(f"Restored original {method_name} on {target.__class__.__name__}")

    def run(self, target: Any) -> Dict[str, Any]:
        """
        Execute the model degradation scenario against the target system.

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
            "degradation_level": self.degradation_level,
            "degradation_types_applied": self.degradation_types,
            "models_intercepted": []
        }

        try:
            # Identify the model to intercept
            # This is highly framework-dependent

            # First, check if the target itself is a model
            model_like_attrs = ["generate", "complete", "chat", "predict", "__call__"]
            is_model = any(hasattr(target, attr) and callable(getattr(target, attr))
                         for attr in model_like_attrs)

            if is_model:
                # Target is the model itself
                self.intercept_model(target)
                details["models_intercepted"].append(f"{target.__class__.__name__}")
            else:
                # Look for model attributes on the target
                for attr_name in dir(target):
                    if attr_name.startswith("_"):
                        continue

                    attr = getattr(target, attr_name)

                    # Check if this attribute looks like a model
                    attr_is_model = any(hasattr(attr, model_attr) and callable(getattr(attr, model_attr))
                                     for model_attr in model_like_attrs)

                    # Also check attribute name for clues
                    model_name_indicators = ["model", "llm", "gpt", "language_model", "backbone"]
                    name_suggests_model = any(indicator in attr_name.lower()
                                           for indicator in model_name_indicators)

                    if attr_is_model or name_suggests_model:
                        self.intercept_model(attr)
                        details["models_intercepted"].append(f"{attr_name}:{attr.__class__.__name__}")

            if not details["models_intercepted"]:
                observations.append("Could not identify any models to intercept")
                return {
                    "success": False,
                    "observations": observations,
                    "details": details
                }

            observations.append(f"Intercepted {len(details['models_intercepted'])} models")
            observations.append(f"Applied degradation level: {self.degradation_level}")
            observations.append("Degradation types: " + ", ".join(self.degradation_types))

            # Provide guidance on how to test with the degraded model
            observations.append(
                "To test: Run tasks with this scenario active and observe if the agent "
                "can still achieve its goals despite degraded model quality"
            )

            # For now, success is based on whether we could intercept methods
            success = len(details["models_intercepted"]) > 0

        finally:
            # Always restore the original methods
            self.restore_models()
            observations.append("Restored all intercepted models")

        self.teardown()

        return {
            "success": success,
            "observations": observations,
            "details": details
        }
