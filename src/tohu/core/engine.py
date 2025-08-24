"""
Core chaos engine implementation for Tohu.

This module contains the main ChaosEngine class that orchestrates
the execution of chaos scenarios.
"""

from typing import Dict, List, Optional, Type
import logging
from dataclasses import dataclass, field
import importlib
import pkgutil
from pathlib import Path

from tohu.core.scenario import ChaosScenario

logger = logging.getLogger(__name__)


@dataclass
class ChaosEngine:
    """
    The main orchestrator for running chaos scenarios against AI agents.

    The ChaosEngine is responsible for:
    1. Discovering available scenarios
    2. Executing scenarios against target systems
    3. Collecting and reporting results

    Attributes:
        scenarios: A dictionary of registered scenarios by name
        loaded_plugins: A list of loaded plugin modules
    """

    scenarios: Dict[str, Type[ChaosScenario]] = field(default_factory=dict)
    loaded_plugins: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Initialize the engine by discovering built-in scenarios."""
        self._discover_scenarios()

    def _discover_scenarios(self):
        """
        Discover and register all available scenarios.

        This method searches for scenarios in:
        1. Built-in scenarios module
        2. Installed plugins (via entry points, coming soon)
        """
        # Import built-in scenarios
        from tohu import scenarios as builtin_scenarios

        # Scan the scenarios package
        scenarios_path = Path(builtin_scenarios.__file__).parent
        for _, name, is_pkg in pkgutil.iter_modules([str(scenarios_path)]):
            if not is_pkg and not name.startswith("_"):
                try:
                    module = importlib.import_module(f"tohu.scenarios.{name}")
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if (isinstance(attr, type) and
                            issubclass(attr, ChaosScenario) and
                            attr is not ChaosScenario):
                            scenario_name = attr.__name__
                            self.scenarios[scenario_name] = attr
                            logger.debug(f"Registered scenario: {scenario_name}")
                except ImportError as e:
                    logger.error(f"Failed to import scenario module {name}: {e}")

        # TODO: Discover plugins via entry points

    def register_scenario(self, scenario_class: Type[ChaosScenario]) -> None:
        """
        Register a new scenario class with the engine.

        Args:
            scenario_class: The scenario class to register
        """
        scenario_name = scenario_class.__name__
        self.scenarios[scenario_name] = scenario_class
        logger.debug(f"Manually registered scenario: {scenario_name}")

    def load_plugin(self, plugin_module_name: str) -> None:
        """
        Load a plugin module that may contain additional scenarios.

        Args:
            plugin_module_name: The full module name of the plugin to load
        """
        try:
            importlib.import_module(plugin_module_name)
            self.loaded_plugins.append(plugin_module_name)
            logger.info(f"Loaded plugin: {plugin_module_name}")
            # Re-discover scenarios to include newly loaded ones
            self._discover_scenarios()
        except ImportError as e:
            logger.error(f"Failed to load plugin {plugin_module_name}: {e}")

    def run_scenario(self,
                    scenario_name: str,
                    target_system: Optional[object] = None,
                    **kwargs) -> dict:
        """
        Run a specific chaos scenario by name.

        Args:
            scenario_name: The name of the scenario to run
            target_system: The target system or agent to test
            **kwargs: Additional configuration parameters for the scenario

        Returns:
            A dictionary containing the results and observations

        Raises:
            ValueError: If the specified scenario is not found
        """
        if scenario_name not in self.scenarios:
            raise ValueError(f"Scenario '{scenario_name}' not found. "
                            f"Available scenarios: {list(self.scenarios.keys())}")

        scenario_class = self.scenarios[scenario_name]
        scenario = scenario_class(**kwargs)

        logger.info(f"Running scenario: {scenario_name}")
        results = scenario.run(target_system)

        return {
            "scenario": scenario_name,
            "success": results.get("success", False),
            "observations": results.get("observations", []),
            "details": results
        }

    def list_scenarios(self) -> List[str]:
        """
        List all available scenarios.

        Returns:
            A list of scenario names
        """
        return list(self.scenarios.keys())
