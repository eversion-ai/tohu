"""
Command-line interface for the Tohu chaos engineering framework.

This module provides a CLI for running chaos scenarios and
managing Tohu configurations.
"""

import typer
import logging
from typing import Optional
import sys
import importlib

from tohu.core import ChaosEngine

app = typer.Typer(
    name="tohu",
    help="Chaos engineering framework for agentic AI systems",
    add_completion=False,
)

logger = logging.getLogger(__name__)


@app.command()
def run(
    scenario: str = typer.Argument(..., help="Name of the scenario to run"),
    target: Optional[str] = typer.Option(
        None, "--target", "-t", help="Module path to the target system or agent"
    ),
    config: Optional[str] = typer.Option(
        None, "--config", "-c", help="Path to a configuration file"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
):
    """
    Run a chaos testing scenario against a target system.
    """
    # Set up logging
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Create the engine
    engine = ChaosEngine()

    # Report available scenarios
    available_scenarios = engine.list_scenarios()
    if not available_scenarios:
        typer.echo("No scenarios available. Make sure Tohu is properly installed.")
        raise typer.Exit(code=1)

    if scenario not in available_scenarios:
        typer.echo(f"Scenario '{scenario}' not found. Available scenarios:")
        for s in available_scenarios:
            typer.echo(f"  - {s}")
        raise typer.Exit(code=1)

    # Load target if specified
    target_system = None
    if target:
        try:
            module_path, attr_name = target.rsplit(".", 1)
            module = importlib.import_module(module_path)
            target_system = getattr(module, attr_name)
            typer.echo(f"Loaded target system from {target}")
        except (ValueError, ImportError, AttributeError) as e:
            typer.echo(f"Error loading target system: {e}")
            raise typer.Exit(code=1)

    # TODO: Load configuration from file if specified

    # Run the scenario
    typer.echo(f"Running scenario: {scenario}")
    try:
        results = engine.run_scenario(scenario, target_system)

        # Display results
        typer.echo("\nResults:")
        typer.echo(f"  Success: {results['success']}")
        typer.echo("\nObservations:")
        for obs in results.get("observations", []):
            typer.echo(f"  - {obs}")

        # Exit with appropriate code
        if not results["success"]:
            typer.echo("\nScenario test failed.")
            raise typer.Exit(code=1)

        typer.echo("\nScenario test completed successfully.")

    except Exception as e:
        typer.echo(f"Error running scenario: {e}")
        if verbose:
            import traceback
            typer.echo(traceback.format_exc())
        raise typer.Exit(code=1)


@app.command()
def list():
    """
    List all available chaos testing scenarios.
    """
    engine = ChaosEngine()
    scenarios = engine.list_scenarios()

    if not scenarios:
        typer.echo("No scenarios available.")
        return

    typer.echo("Available scenarios:")
    for scenario in scenarios:
        typer.echo(f"  - {scenario}")


def main():
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
