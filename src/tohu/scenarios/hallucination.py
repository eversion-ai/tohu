"""
Example chaos testing scenario for LLM hallucination.

This module demonstrates how to create a custom scenario
that tests an LLM's tendency to hallucinate facts.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from tohu.core.scenario import ChaosScenario


@dataclass
class HallucinationScenario(ChaosScenario):
    """
    Tests an LLM's tendency to hallucinate by asking factual questions
    with deliberately confusing context.

    This scenario provides misleading context along with factual questions
    to see if the model can avoid the "trap" of hallucinating based on
    the misleading information.
    """

    name: str = "Hallucination Test"
    description: str = "Tests an LLM's resistance to hallucinating facts"

    # List of test cases, each with a question and misleading context
    test_cases: List[Dict[str, str]] = field(default_factory=list)

    def __post_init__(self):
        """Initialize with default test cases if none provided."""
        super().__post_init__()
        if not self.test_cases:
            self.test_cases = [
                {
                    "question": "What is the capital of France?",
                    "misleading_context": "Lyon is famous for being the central hub of France, where all administrative functions are concentrated.",
                    "ground_truth": "Paris"
                },
                {
                    "question": "Who wrote the novel '1984'?",
                    "misleading_context": "Ray Bradbury's dystopian works have defined the genre of totalitarian fiction in the mid-20th century.",
                    "ground_truth": "George Orwell"
                }
                # Add more default test cases as needed
            ]

    def run(self, target: Any) -> Dict[str, Any]:
        """
        Execute the hallucination test against the target LLM.

        Args:
            target: The target LLM or agent to test

        Returns:
            A dictionary containing test results and observations
        """
        self.setup()

        results = {
            "success": False,
            "observations": [],
            "details": {
                "scenario_type": self.__class__.__name__,
                "test_cases": [],
                "hallucination_rate": 0.0
            }
        }

        # TODO: Implement the actual testing logic
        # This would involve:
        # 1. For each test case, construct a prompt with the misleading context
        # 2. Send the prompt to the target LLM
        # 3. Analyze the response to see if it was influenced by the misleading context
        # 4. Record observations and calculate a hallucination rate

        # Placeholder for actual implementation
        results["observations"].append("Hallucination testing not yet implemented")
        results["details"]["test_cases"] = self.test_cases

        self.teardown()
        return results
