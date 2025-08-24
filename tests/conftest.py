"""
Configuration and fixtures for pytest.
"""

import pytest
import sys
from pathlib import Path

# Add the src directory to the path so tests can import the package
# This is needed when running tests before the package is installed
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture
def mock_agent():
    """
    Create a mock agent for testing chaos scenarios.

    Returns:
        A simple object with methods that can be intercepted and tested
    """
    class MockAgent:
        def __init__(self):
            self.responses = {}
            self.call_history = []

        def generate(self, prompt):
            """Generate a response to a prompt."""
            self.call_history.append(("generate", prompt))
            if prompt in self.responses:
                return self.responses[prompt]
            return "I don't have a specific response for this prompt."

        def set_response(self, prompt, response):
            """Set a canned response for a specific prompt."""
            self.responses[prompt] = response

    return MockAgent()
