# Tohu 🚧 Under Heavy Development - Pre-Alpha 🚧

**Please note:** This project is in the very early stages of development. The code is not yet functional, and the API is subject to significant change. The examples below represent the **target design** and are for discussion and contribution purposes. We welcome contributors to help us make this vision a reality\!

-----

## Overview

Tohu is a planned chaos engineering framework for testing the robustness and reliability of agentic AI systems. It will allow you to inject precise, controlled failures into your agent workflows to ensure they can handle unexpected situations before they reach production.

Similar to how chaos engineering has become essential for testing distributed systems, Tohu aims to bring these same rigorous principles to the world of agentic AI.

-----

## The Vision

Our goal is to create a community-driven, framework-agnostic tool that becomes the standard for reliability testing in agentic AI. We envision a future where developers can confidently deploy complex agent systems, knowing they are resilient by design, not fragile by default.

**Key Goals:**

  * **Framework Agnostic:** Build a core engine with adapters for all major agent frameworks (AutoGen, Pydantic AI, LangChain, CrewAI, etc.).
  * **Extensible Scenario Library:** Create a rich, open-source library of common failure modes that the community can easily contribute to.
  * **Simple & Powerful API:** Design an intuitive interface for both running pre-built scenarios and creating complex, custom ones.
  * **Actionable Insights:** Provide clear, detailed results that help developers pinpoint weaknesses and build more resilient agents.

-----

## Proposed API & Usage (Target Design)

The following examples illustrate the intended API and user experience we are working towards.

#### Basic Usage

```python
# NOTE: This code is an example of the target API and is not yet implemented.

from tohu.core import ChaosEngine
from tohu.scenarios import HallucinationScenario

# The ChaosEngine will orchestrate scenarios
engine = ChaosEngine()

# Create a target AI agent to test (replace with your agent creation code)
my_agent = create_your_agent()

# Run a built-in scenario against the agent
results = engine.run_scenario("HallucinationScenario", my_agent)

# The engine will return structured results for analysis
print(f"Success: {results['success']}")
print("Observations:")
for obs in results["observations"]:
    print(f"- {obs}")
```

#### Creating Custom Scenarios

```python
# NOTE: This is a proposed design for the custom scenario API.

from dataclasses import dataclass
from typing import Any, Dict
from tohu.core import ChaosScenario

@dataclass
class MyCustomScenario(ChaosScenario):
    """
    A custom scenario to test a specific aspect of your AI agent.
    """
    name = "My Custom Scenario"
    description = "Tests how my agent handles a specific edge case."

    def run(self, target: Any) -> Dict[str, Any]:
        # Your testing logic will go here.
        # Apply chaos conditions, observe, and record results.

        return {
            "success": True,  # or False
            "observations": [
                "The agent correctly identified the impossible goal.",
                "The agent exited gracefully without excessive token usage."
            ],
        }

# Register and run your custom scenario
engine = ChaosEngine()
engine.register_scenario(MyCustomScenario)
results = engine.run_scenario("MyCustomScenario", my_agent)
```

-----

## How to Contribute

This project will be shaped by the community, and we are actively looking for contributors\! Whether you're a developer, an AI researcher, or just passionate about AI reliability, there are many ways to help.

  * **Discuss the API Design:** Do you have ideas for the API? Open an issue to discuss the proposed design.
  * **Propose Scenarios:** What are the most painful failure modes you've encountered? Share your use cases in the Issues or on Discord.
  * **Help with Integrations:** If you have deep expertise in a specific agent framework, we'd love your help designing the adapters.
  * **Write Code:** Once the core API is stable, we'll need help building out the scenario library, CLI, and framework integrations.

-----

## Development Setup

To get started with the codebase for contribution, clone the repository and set up the development environment:

```bash
git clone https://github.com/your-repo/tohu.git
cd tohu
pip install -e ".[dev,test]"
```

-----

## High-Level Roadmap

This is a tentative plan and will be influenced by community feedback.

  * [ ] **Phase 1: Core Engine & API:** Solidify the `ChaosEngine` and `ChaosScenario` base classes.
  * [ ] **Phase 2: First Adapter:** Build the first framework integration (e.g., for AutoGen) to prove the model.
  * [ ] **Phase 3: Initial Scenario Library:** Implement the first set of common scenarios (e.g., Hallucination, Tool Failure).
  * [ ] **Phase 4: CLI Implementation:** Build out the command-line interface for running tests.
  * [ ] **Phase 5: Community Contribution:** Expand the library of scenarios and adapters with the help of the community.

-----

# Getting Started

uv pip install -e ".[dev,test,autogen]"

## License

This project is planned to be licensed under the Apache License 2.0. See the `LICENSE` file for details.
