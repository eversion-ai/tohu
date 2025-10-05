# Tohu �

## Chaos Engineering Framework for Agentic AI Systems

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Development Status](https://img.shields.io/badge/status-alpha-yellow.svg)]()

**Tohu** is a production-ready chaos engineering framework for testing the robustness, reliability, and safety of agentic AI systems. It allows you to inject precise, controlled failures into your agent workflows to ensure they can handle unexpected situations before they reach production.

Similar to how chaos engineering has become essential for testing distributed systems, Tohu brings these same rigorous principles to the world of agentic AI.

---

## 🎯 Why Tohu?

As AI agents become more autonomous and are deployed in critical systems, their reliability and safety become paramount. Tohu helps you:

- **🛡️ Build Resilient Agents** - Test your agents against 18+ failure scenarios before production
- **🔍 Discover Hidden Weaknesses** - Find edge cases and vulnerabilities in controlled environments
- **🚀 Deploy with Confidence** - Know your agents can handle real-world chaos and adversarial conditions
- **📊 Measure Safety** - Quantify agent reliability with comprehensive testing metrics
- **🔧 Framework Agnostic** - Works with AutoGen, Pydantic AI, and extensible to any framework

---

## ✨ Key Features

### 🎪 Comprehensive Scenario Library
- **18+ Built-in Scenarios** covering agent behavior, infrastructure, security, and multi-agent interactions
- **Unfulfillable Task Testing** - Three-layer safety validation (obvious, subtle, LLM-generated impossibilities)
- **Rogue Agent Simulation** - Test containment mechanisms and kill-switch systems
- **Infrastructure Chaos** - Simulate API failures, latency, resource exhaustion, and state corruption
- **Security Testing** - Prompt injection, data poisoning, and adversarial attacks

### 🔌 Framework Integration
- **AutoGen** - Full decorator-based integration with monitoring and reporting
- **Pydantic AI** - Native support with type-safe chaos injection
- **Extensible Architecture** - Easy to add support for new frameworks

### 🎨 Simple & Powerful API
```python
# Minimal integration - just add a decorator!
@rogue_agent_chaos(deviation_probability=0.3)
async def your_agent_function():
    # Your existing agent code works unchanged
    pass
```

### 📈 Production Ready
- **Configurable chaos rates** for different environments (dev/staging/prod)
- **Comprehensive logging** and monitoring integration
- **Detailed metrics** and threat detection
- **CI/CD integration** patterns included

---

## 🚀 Quick Start

### Installation

```bash
# Install with AutoGen support
pip install -e ".[autogen]"

# Install with Pydantic AI support
pip install -e ".[pydantic-ai]"

# Install with development tools
pip install -e ".[dev,test]"
```

### Basic Usage

#### 1. Using the Core Engine

```python
from tohu.core import ChaosEngine
from tohu.scenarios.agent_behavior import RogueAgentScenario

# Initialize the chaos engine
engine = ChaosEngine()

# Register a scenario
engine.register_scenario(RogueAgentScenario)

# Run against your agent
results = engine.run_scenario(
    "RogueAgentScenario",
    your_agent,
    deviation_probability=0.3
)

# Analyze results
print(f"Success: {results['success']}")
print(f"Observations: {results['observations']}")
```

#### 2. Using Decorator Pattern (AutoGen)

```python
from examples.autogen_demos.simple_rogue import rogue_chaos

# Just add one decorator!
@rogue_chaos(probability=0.3)
async def main():
    # Your existing AutoGen code
    agent = AssistantAgent(...)
    result = await agent.run(task)
    return result

asyncio.run(main())
```

#### 3. Unfulfillable Task Testing

```python
from tohu.scenarios.agent_behavior import (
    ObviousUnfulfillableTaskScenario,
    SubtleUnfulfillableTaskScenario,
    LLMGeneratedUnfulfillableTaskScenario
)

# Test obvious impossibilities (delete internet, time travel)
obvious = ObviousUnfulfillableTaskScenario(escalation_steps=5)
results = obvious.run(your_agent)
print(f"Guardrail effectiveness: {results['guardrail_effectiveness']}")

# Test subtle logical contradictions
subtle = SubtleUnfulfillableTaskScenario(
    analysis_depth_levels=3,
    contradiction_types=['logical_contradiction', 'resource_impossibility']
)
results = subtle.run(your_agent)
print(f"Contradictions detected: {results['contradictions_detected']}")

# Test LLM-generated domain-specific impossibilities
llm_gen = LLMGeneratedUnfulfillableTaskScenario(
    task_generation_attempts=5,
    impossibility_subtlety_levels=['obvious_constraint_violation']
)
results = llm_gen.run(
    your_agent,
    user_purpose="building a web application",
    domain="software_development"
)
print(f"Detection effectiveness: {results['detection_effectiveness']}")
```

### Creating Custom Scenarios

```python
from dataclasses import dataclass
from typing import Any, Dict
from tohu.core import ChaosScenario

@dataclass
class MyCustomScenario(ChaosScenario):
    """Custom scenario to test specific agent behavior."""

    name: str = "My Custom Test"
    description: str = "Tests custom edge case handling"

    # Add custom configuration
    failure_rate: float = 0.3

    def setup(self) -> None:
        """Prepare the scenario."""
        print(f"Setting up {self.name}")

    def run(self, target: Any) -> Dict[str, Any]:
        """Execute the test."""
        observations = []

        # Your custom testing logic
        try:
            result = target.perform_action()
            observations.append("Agent handled the edge case")
            success = True
        except Exception as e:
            observations.append(f"Agent failed: {e}")
            success = False

        return {
            "success": success,
            "observations": observations,
            "metrics": {"failure_rate": self.failure_rate}
        }

# Use it
engine = ChaosEngine()
engine.register_scenario(MyCustomScenario)
results = engine.run_scenario("MyCustomScenario", my_agent)
```

---

## 📚 Complete Scenario Library

Tohu includes **18 production-ready scenarios** organized into 4 categories:

### 🤖 Agent Behavior (7 scenarios)
1. **RogueAgentScenario** - Tests containment and kill-switch mechanisms
2. **StupidSelectorsScenario** - Tests decision-making with forced suboptimal selections
3. **AbruptConversationsScenario** - Tests state management during interruptions
4. **WrongTerminationScenario** - Tests goal-completion logic with impossible conditions
5. **ObviousUnfulfillableTaskScenario** - Tests detection of clearly impossible tasks
6. **SubtleUnfulfillableTaskScenario** - Tests detection of logical contradictions
7. **LLMGeneratedUnfulfillableTaskScenario** - Tests detection of domain-relevant impossible tasks

### 🏗️ Infrastructure (6 scenarios)
8. **ToolLLMFailureScenario** - Simulates API failures, timeouts, rate limits
9. **ModelDegradationScenario** - Tests graceful degradation with less capable models
10. **CorruptedStateScenario** - Tests resilience to data corruption
11. **WrongContextMemoryScenario** - Tests handling of incorrect context/memory
12. **ResourceExhaustionScenario** - Tests behavior under resource constraints
13. **HighLatencyScenario** - Tests performance with degraded response times

### 🔒 Security (3 scenarios)
14. **PromptInjectionScenario** - Tests resistance to prompt manipulation attacks
15. **DataPoisoningScenario** - Tests handling of corrupted training/context data
16. **HallucinationScenario** - Tests detection and mitigation of false information

### 👥 Multi-Agent (2 scenarios)
17. **OscillatingConversationsScenario** - Tests multi-agent conversation stability
18. **ConflictingInstructionsScenario** - Tests handling of contradictory agent goals

See [SCENARIOS.md](SCENARIOS.md) for detailed documentation of each scenario.

---

## 📦 Examples & Integration Guides

### AutoGen Examples
Located in `examples/autogen_demos/`:
- **`quickstart.py`** - Basic rogue agent chaos testing
- **`quickstart_simple.py`** - Minimal decorator pattern integration
- **`obvious_unfulfillable_simple.py`** - Basic safety guardrail testing
- **`subtle_unfulfillable_simple.py`** - Logical reasoning tests
- **`llm_generated_unfulfillable_simple.py`** - Domain expertise validation
- **`comprehensive_unfulfillable_simple.py`** - Multi-layer safety suite

See the [AutoGen README](examples/autogen_demos/README.md) for detailed usage instructions.

### Pydantic AI Examples
Located in `examples/pydantic_ai_demos/`:
- **`basic_rogue_agent.py`** - Rogue agent testing with Pydantic AI type safety

See the [Pydantic AI README](examples/pydantic_ai_demos/README.md) for setup and usage.

---

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=tohu --cov-report=html

# Run specific test file
pytest tests/test_unfulfillable_tasks.py

# Run with verbose output
pytest -v
```

---

## 🛠️ Development Setup

### Prerequisites
- Python 3.12 or higher
- pip or uv for package management

### Setup Instructions

```bash
# Clone the repository
git clone https://github.com/tohu-ai/tohu.git
cd tohu

# Install with all development dependencies
pip install -e ".[dev,test,autogen]"

# Or using uv (recommended)
uv pip install -e ".[dev,test,autogen]"

# Run linting
ruff check .

# Run type checking
mypy src/tohu

# Run tests
pytest
```

### Project Structure
```
tohu/
├── src/tohu/              # Core framework
│   ├── core/              # Engine and base classes
│   ├── scenarios/         # Scenario implementations
│   │   ├── agent_behavior/
│   │   ├── infrastructure/
│   │   ├── security/
│   │   └── multiagent/
│   └── plugins/           # Framework adapters
├── examples/              # Usage examples
│   ├── autogen_demos/     # AutoGen integration
│   └── pydantic_ai_demos/ # Pydantic AI integration
├── tests/                 # Test suite
└── docs/                  # Documentation
```

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Ways to Contribute
- 🐛 **Report bugs** and suggest features via [Issues](https://github.com/tohu-ai/tohu/issues)
- 📝 **Improve documentation** and add examples
- 🧪 **Add new scenarios** to the library
- 🔌 **Create framework adapters** for new AI frameworks
- ✅ **Write tests** to improve coverage
- 💬 **Share your experience** using Tohu in production

---

## 📖 Documentation

- **[Complete Scenario Documentation](SCENARIOS.md)** - Detailed guide to all 18 scenarios
- **[AutoGen Integration Guide](examples/autogen_demos/README.md)** - Full AutoGen setup and patterns
- **[Pydantic AI Integration Guide](examples/pydantic_ai_demos/README.md)** - Pydantic AI examples
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute to the project
- **[API Documentation](docs/)** - Detailed API reference

---

## 🗺️ Roadmap

### ✅ Completed
- [x] Core chaos engine and scenario framework
- [x] 18 production-ready scenarios across 4 categories
- [x] AutoGen integration with decorator patterns
- [x] Pydantic AI integration
- [x] Comprehensive test suite
- [x] Example implementations and documentation

### 🚧 In Progress
- [ ] CLI tool for running tests from command line
- [ ] Enhanced monitoring and metrics dashboard
- [ ] LangChain adapter
- [ ] CrewAI adapter

### 🔮 Future Plans
- [ ] Real-time chaos injection in production
- [ ] Chaos experiment scheduling and automation
- [ ] Advanced reporting and analytics
- [ ] Integration with MLOps platforms
- [ ] Chaos scenario marketplace/sharing

---

## 📄 License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Tohu is inspired by chaos engineering principles from Netflix's Chaos Monkey and applies them to the unique challenges of agentic AI systems. Special thanks to all contributors and the broader AI safety community.

---

## 📬 Contact & Community

- **Issues**: [GitHub Issues](https://github.com/tohu-ai/tohu/issues)
- **Discussions**: [GitHub Discussions](https://github.com/tohu-ai/tohu/discussions)
- **Email**: harelix@eversion.ai

---

**⚠️ Important**: Tohu is designed for testing and security research in controlled environments. Always use proper safeguards when testing chaos scenarios, especially in production systems.
