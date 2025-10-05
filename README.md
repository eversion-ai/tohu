# 🔄 Repository Moved

**This repository has moved to [https://github.com/eversion-ai/tohu](https://github.com/eversion-ai/tohu)**

Please update your bookmarks and references. All future development, issues, and discussions will take place in the new location.

---

# Tohu 🌊

## Chaos Engineering Framework for Agentic AI Systems

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Development Status](https://img.shields.io/badge/status-alpha-yellow.svg)]()

**Tohu** is a comprehensive chaos engineering framework designed to ensure the robustness, reliability, and safety of agentic AI systems. By enabling controlled failure injection into agent workflows, Tohu helps teams identify and address vulnerabilities before deployment, building confidence in AI agent reliability.

Drawing from proven chaos engineering principles used in distributed systems, Tohu adapts these methodologies to meet the unique challenges of autonomous AI agents operating in production environments.

---

## 🎯 Why Tohu?

As organizations increasingly rely on autonomous AI agents for critical operations, ensuring their reliability and safety becomes essential. Tohu provides a systematic approach to:

- **Build Resilient Agents** - Validate agent behavior against 18+ realistic failure scenarios
- **Discover Vulnerabilities Early** - Identify edge cases and weaknesses in controlled testing environments
- **Deploy with Confidence** - Ensure agents can gracefully handle unexpected conditions
- **Establish Safety Baselines** - Measure and track agent reliability with comprehensive metrics
- **Maintain Framework Flexibility** - Integrate seamlessly with AutoGen, Pydantic AI, and custom frameworks

---

## ✨ Key Capabilities

### 🎪 Extensive Scenario Library
- **18+ Production-Ready Scenarios** covering agent behavior, infrastructure resilience, security, and multi-agent coordination
- **Multi-Layer Safety Validation** - Progressive testing from obvious to subtle failure modes
- **Behavioral Testing** - Verify containment mechanisms and safety protocols
- **Infrastructure Resilience** - Validate handling of API failures, latency spikes, and resource constraints
- **Security Hardening** - Test defenses against prompt injection, data corruption, and adversarial inputs

### 🔌 Seamless Framework Integration
- **AutoGen** - Decorator-based integration with comprehensive monitoring
- **Pydantic AI** - Type-safe chaos injection with native support
- **Extensible Design** - Straightforward adapter pattern for additional frameworks

### 🎨 Developer-Friendly API
```python
# Simple integration pattern
@rogue_agent_chaos(deviation_probability=0.3)
async def your_agent_function():
    # Existing agent code remains unchanged
    pass
```

### 📈 Production-Grade Features
- **Environment-Aware Configuration** - Adjustable chaos injection rates for dev, staging, and production
- **Comprehensive Observability** - Detailed logging and metrics integration
- **Actionable Insights** - Clear threat detection and reliability reporting
- **CI/CD Ready** - Integration patterns for automated testing pipelines

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

# Execute against your agent
results = engine.run_scenario(
    "RogueAgentScenario",
    your_agent,
    deviation_probability=0.3
)

# Review results
print(f"Success: {results['success']}")
print(f"Observations: {results['observations']}")
```

#### 2. Using Decorator Pattern (AutoGen)

```python
from examples.autogen_demos.simple_rogue import rogue_chaos

# Add chaos testing with a single decorator
@rogue_chaos(probability=0.3)
async def main():
    # Your existing AutoGen implementation
    agent = AssistantAgent(...)
    result = await agent.run(task)
    return result

asyncio.run(main())
```

#### 3. Safety Guardrail Testing

```python
from tohu.scenarios.agent_behavior import (
    ObviousUnfulfillableTaskScenario,
    SubtleUnfulfillableTaskScenario,
    LLMGeneratedUnfulfillableTaskScenario
)

# Test detection of impossible tasks
obvious = ObviousUnfulfillableTaskScenario(escalation_steps=5)
results = obvious.run(your_agent)
print(f"Guardrail effectiveness: {results['guardrail_effectiveness']}")

# Test logical reasoning
subtle = SubtleUnfulfillableTaskScenario(
    analysis_depth_levels=3,
    contradiction_types=['logical_contradiction', 'resource_impossibility']
)
results = subtle.run(your_agent)
print(f"Contradictions detected: {results['contradictions_detected']}")

# Test domain-specific validation
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
    """Custom scenario for testing specific agent behavior."""

    name: str = "My Custom Test"
    description: str = "Tests custom edge case handling"

    # Custom configuration
    failure_rate: float = 0.3

    def setup(self) -> None:
        """Prepare the testing environment."""
        print(f"Initializing {self.name}")

    def run(self, target: Any) -> Dict[str, Any]:
        """Execute the test scenario."""
        observations = []

        # Custom testing logic
        try:
            result = target.perform_action()
            observations.append("Agent handled the edge case successfully")
            success = True
        except Exception as e:
            observations.append(f"Agent encountered issue: {e}")
            success = False

        return {
            "success": success,
            "observations": observations,
            "metrics": {"failure_rate": self.failure_rate}
        }

# Usage
engine = ChaosEngine()
engine.register_scenario(MyCustomScenario)
results = engine.run_scenario("MyCustomScenario", my_agent)
```

---

## 📚 Scenario Library

Tohu provides **18 production-ready scenarios** organized into 4 testing categories:

### 🤖 Agent Behavior (7 scenarios)
1. **RogueAgentScenario** - Validates containment mechanisms and safety protocols
2. **StupidSelectorsScenario** - Tests decision-making under constrained conditions
3. **AbruptConversationsScenario** - Validates state management during interruptions
4. **WrongTerminationScenario** - Tests goal completion logic with edge cases
5. **ObviousUnfulfillableTaskScenario** - Validates detection of clearly impossible requests
6. **SubtleUnfulfillableTaskScenario** - Tests identification of logical contradictions
7. **LLMGeneratedUnfulfillableTaskScenario** - Validates domain-specific impossibility detection

### 🏗️ Infrastructure (6 scenarios)
8. **ToolLLMFailureScenario** - Simulates API failures, timeouts, and rate limits
9. **ModelDegradationScenario** - Tests graceful degradation with alternative models
10. **CorruptedStateScenario** - Validates resilience to data corruption
11. **WrongContextMemoryScenario** - Tests handling of incorrect context information
12. **ResourceExhaustionScenario** - Validates behavior under resource constraints
13. **HighLatencyScenario** - Tests performance under degraded response times

### 🔒 Security (3 scenarios)
14. **PromptInjectionScenario** - Validates defenses against prompt manipulation
15. **DataPoisoningScenario** - Tests handling of corrupted data inputs
16. **HallucinationScenario** - Validates detection and mitigation of false information

### 👥 Multi-Agent (2 scenarios)
17. **OscillatingConversationsScenario** - Tests multi-agent interaction stability
18. **ConflictingInstructionsScenario** - Validates handling of contradictory directives

Detailed documentation for each scenario is available in [SCENARIOS.md](SCENARIOS.md).

---

## 📦 Examples & Integration Guides

### AutoGen Examples
Located in `examples/autogen_demos/`:
- **`quickstart.py`** - Comprehensive rogue agent testing
- **`quickstart_simple.py`** - Minimal integration pattern
- **`obvious_unfulfillable_simple.py`** - Basic safety validation
- **`subtle_unfulfillable_simple.py`** - Logical reasoning tests
- **`llm_generated_unfulfillable_simple.py`** - Domain expertise validation
- **`comprehensive_unfulfillable_simple.py`** - Complete safety test suite

See the [AutoGen README](examples/autogen_demos/README.md) for detailed implementation guidance.

### Pydantic AI Examples
Located in `examples/pydantic_ai_demos/`:
- **`basic_rogue_agent.py`** - Type-safe rogue agent testing

See the [Pydantic AI README](examples/pydantic_ai_demos/README.md) for setup instructions.

---

## 🧪 Testing

```bash
# Execute all tests
pytest

# Generate coverage report
pytest --cov=tohu --cov-report=html

# Run specific test suite
pytest tests/test_unfulfillable_tasks.py

# Verbose output
pytest -v
```

---

## 🛠️ Development Setup

### Prerequisites
- Python 3.12 or higher
- pip or uv package manager

### Setup Instructions

```bash
# Clone the repository
git clone https://github.com/eversion-ai/tohu.git
cd tohu

# Install development dependencies
pip install -e ".[dev,test,autogen]"

# Or using uv (recommended)
uv pip install -e ".[dev,test,autogen]"

# Run linting
ruff check .

# Run type checking
mypy src/tohu

# Execute tests
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

We welcome contributions from the community! Please review [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to get involved.

### Ways to Contribute
- **Report Issues** - Submit bugs and feature requests via [GitHub Issues](https://github.com/eversion-ai/tohu/issues)
- **Enhance Documentation** - Improve guides and add practical examples
- **Develop Scenarios** - Contribute new testing scenarios to the library
- **Build Integrations** - Create adapters for additional AI frameworks
- **Improve Testing** - Expand test coverage and quality
- **Share Experiences** - Document real-world usage and lessons learned

---

## 📖 Documentation

- **[Scenario Documentation](SCENARIOS.md)** - Complete guide to all 18 scenarios
- **[AutoGen Integration Guide](examples/autogen_demos/README.md)** - AutoGen setup and patterns
- **[Pydantic AI Integration Guide](examples/pydantic_ai_demos/README.md)** - Pydantic AI examples
- **[Contributing Guide](CONTRIBUTING.md)** - Contribution guidelines and process
- **[API Documentation](docs/)** - Detailed API reference

---

## 🗺️ Roadmap

### ✅ Current Release
- Core chaos engine and scenario framework
- 18 production-ready scenarios across 4 categories
- AutoGen integration with decorator patterns
- Pydantic AI integration
- Comprehensive test suite
- Example implementations and documentation

### 🚧 Active Development
- CLI tool for streamlined test execution
- Enhanced monitoring and metrics dashboard
- LangChain framework adapter
- CrewAI framework adapter

### 🔮 Future Vision
- Production chaos injection capabilities
- Automated chaos experiment scheduling
- Advanced analytics and reporting
- MLOps platform integrations
- Community scenario sharing platform

---

## 📄 License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for complete details.

---

## 🙏 Acknowledgments

Tohu draws inspiration from chaos engineering principles pioneered by Netflix's Chaos Monkey, adapting these proven methodologies to address the unique challenges of agentic AI systems. We're grateful to all contributors and the broader AI safety community for their ongoing support and collaboration.

---

## 📬 Contact & Community

- **Issues & Bug Reports**: [GitHub Issues](https://github.com/eversion-ai/tohu/issues)
- **Feature Discussions**: [GitHub Discussions](https://github.com/eversion-ai/tohu/discussions)
- **Email**: harelix@eversion.ai

---

**⚠️ Important Note**: Tohu is designed for controlled testing and security research environments. Always implement appropriate safeguards when conducting chaos testing, particularly in systems handling production workloads or sensitive data.
