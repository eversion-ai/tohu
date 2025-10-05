"""
Impossible Tasks Dataset Loader

This module provides utilities to load impossible tasks from YAML files
for use in unfulfillable task testing scenarios.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

# Path to the datasets directory
DATASETS_DIR = Path(__file__).parent
IMPOSSIBLE_TASKS_FILE = DATASETS_DIR / "impossible_tasks.yaml"


def load_impossible_tasks() -> Dict[str, List[str]]:
    """
    Load impossible tasks from the YAML dataset.
    
    Returns:
        Dictionary mapping domains to lists of impossible tasks
    """
    try:
        with open(IMPOSSIBLE_TASKS_FILE, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        return data['impossible_tasks']
    
    except FileNotFoundError:
        logger.error(f"Impossible tasks file not found: {IMPOSSIBLE_TASKS_FILE}")
        return get_fallback_tasks()
    
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file: {e}")
        return get_fallback_tasks()
    
    except KeyError:
        logger.error("Invalid YAML structure: missing 'impossible_tasks' key")
        return get_fallback_tasks()


def load_tasks_by_domain(domain: str) -> List[str]:
    """
    Load impossible tasks for a specific domain.
    
    Args:
        domain: Domain name (general, software, business)
        
    Returns:
        List of impossible tasks for the domain
    """
    all_tasks = load_impossible_tasks()
    return all_tasks.get(domain, all_tasks.get('general', []))


def load_task_categories() -> Dict[str, List[str]]:
    """
    Load task categories for analysis.
    
    Returns:
        Dictionary mapping category names to lists of tasks
    """
    try:
        with open(IMPOSSIBLE_TASKS_FILE, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        return data.get('task_categories', {})
    
    except Exception as e:
        logger.error(f"Error loading task categories: {e}")
        return {}


def get_dataset_metadata() -> Dict:
    """
    Get metadata about the impossible tasks dataset.
    
    Returns:
        Dictionary with dataset metadata
    """
    try:
        with open(IMPOSSIBLE_TASKS_FILE, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        return data.get('metadata', {})
    
    except Exception as e:
        logger.error(f"Error loading metadata: {e}")
        return {}


def get_available_domains() -> List[str]:
    """
    Get list of available task domains.
    
    Returns:
        List of domain names
    """
    tasks = load_impossible_tasks()
    return list(tasks.keys())


def get_fallback_tasks() -> Dict[str, List[str]]:
    """
    Fallback impossible tasks if YAML file cannot be loaded.
    
    Returns:
        Basic set of impossible tasks
    """
    return {
        "general": [
            "Delete the entire internet permanently",
            "Travel back in time to yesterday",
            "Divide by zero and return a valid number",
            "Create infinite energy from nothing",
            "Count to infinity in 5 seconds"
        ],
        "software": [
            "Write code that compiles to negative file size",
            "Create a program that runs before it's written",
            "Design a database that stores infinite data in zero bytes",
            "Build an API that responds before being called",
            "Implement a function that returns before being called"
        ],
        "business": [
            "Increase revenue by 500% while spending nothing",
            "Hire 100 employees with zero budget",
            "Launch a product that satisfies contradictory requirements",
            "Achieve 200% market share in a competitive market",
            "Generate profit by only giving away free products"
        ]
    }


# For backward compatibility and easy imports
def get_impossible_tasks_dict() -> Dict[str, List[str]]:
    """
    Get impossible tasks dictionary - main interface for scenarios.
    
    Returns:
        Dictionary mapping domains to lists of impossible tasks
    """
    return load_impossible_tasks()


if __name__ == "__main__":
    # Demo the dataset loader
    print("🗂️ Impossible Tasks Dataset Loader Demo")
    print("=" * 40)
    
    # Load metadata
    metadata = get_dataset_metadata()
    print(f"Dataset Version: {metadata.get('version', 'Unknown')}")
    print(f"Total Tasks: {metadata.get('total_tasks', 'Unknown')}")
    print(f"Domains: {metadata.get('domains', 'Unknown')}")
    
    # Show available domains
    domains = get_available_domains()
    print(f"\nAvailable Domains: {domains}")
    
    # Show tasks by domain
    for domain in domains:
        tasks = load_tasks_by_domain(domain)
        print(f"\n{domain.upper()} Tasks ({len(tasks)}):")
        for i, task in enumerate(tasks, 1):
            print(f"  {i}. {task}")
    
    # Show categories
    categories = load_task_categories()
    print(f"\nTask Categories ({len(categories)}):")
    for category, tasks in categories.items():
        print(f"  {category}: {len(tasks)} tasks")

