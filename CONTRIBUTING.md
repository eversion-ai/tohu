# Contributing to Tohu

Thank you for your interest in contributing to Tohu! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

This project and everyone participating in it is governed by the [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How to Contribute

### Reporting Bugs

Before submitting a bug report:

1. Check the issue tracker to see if the bug has already been reported.
2. If it hasn't, create a new issue with a clear description of the problem.
3. Include as much relevant information as possible, such as:
   - Steps to reproduce the bug
   - Expected behavior
   - Actual behavior
   - Environment details (OS, Python version, etc.)
   - Screenshots or logs, if applicable

### Suggesting Enhancements

1. Check the issue tracker to see if the enhancement has already been suggested.
2. If it hasn't, create a new issue clearly labeled as an enhancement request.
3. Provide a clear description of the proposed enhancement and its benefits.

### Contributing Code

1. Fork the repository.
2. Create a new branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes, following the coding style and guidelines.
4. Add or update tests as necessary.
5. Run the tests to ensure they pass:
   ```bash
   pytest
   ```
6. Run linting and type checking:
   ```bash
   ruff check .
   mypy src/tohu
   ```
7. Commit your changes with a descriptive commit message.
8. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
9. Submit a pull request to the main repository.

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/eversion-ai/tohu.git
   cd tohu
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the package in development mode:
   ```bash
   pip install -e ".[dev,test]"
   ```

## Coding Guidelines

### Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/) guidelines.
- Use type annotations for all function parameters and return values.
- Write docstrings following the [Google style](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).
- Run your code through our linters before submitting:
  ```bash
  ruff check .
  mypy src/tohu
  ```

### Testing

- Write tests for all new features and bug fixes.
- Aim for high test coverage.
- Run the test suite before submitting changes:
  ```bash
  pytest
  ```

### Git Commit Messages

- Use clear, descriptive commit messages.
- Start with a short summary line (50 chars or less).
- Optionally, follow with a blank line and a more detailed explanation.

## Creating New Scenarios

Tohu is designed to be extensible with new chaos testing scenarios. To create a new scenario:

1. Create a new file in `src/tohu/scenarios/`.
2. Define a class that inherits from `ChaosScenario`.
3. Implement the required methods, including `run()`.
4. Add the scenario to `src/tohu/scenarios/__init__.py`.
5. Add tests for your scenario in `tests/`.

Example:

```python
from dataclasses import dataclass
from typing import Any, Dict
from tohu.core import ChaosScenario

@dataclass
class MyNewScenario(ChaosScenario):
    """
    Description of what this scenario tests.
    """
    name = "My New Test Scenario"
    description = "Tests how agents handle specific conditions."

    def run(self, target: Any) -> Dict[str, Any]:
        # Implementation goes here
        return {
            "success": True,
            "observations": ["Observation 1", "Observation 2"],
            "details": {"scenario_type": self.__class__.__name__}
        }
```

## License

By contributing to Tohu, you agree that your contributions will be licensed under the project's [Apache 2.0 License](LICENSE).
