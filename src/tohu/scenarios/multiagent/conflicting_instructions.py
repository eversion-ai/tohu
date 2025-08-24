"""
Conflicting Agent Instructions scenario for testing multi-agent coordination.

This scenario assigns contradictory goals to different agents in a multi-agent
system to test conflict resolution, negotiation, and prioritization mechanisms.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Callable, Tuple, Union
import logging
import random
import time
from enum import Enum

from tohu.core.scenario import ChaosScenario

logger = logging.getLogger(__name__)


class ConflictType(Enum):
    """Types of conflicts that can be introduced between agents."""
    RESOURCE_COMPETITION = "resource_competition"  # Compete for limited resources
    CONTRADICTORY_GOALS = "contradictory_goals"    # Directly opposing objectives
    PRIORITY_CONFLICT = "priority_conflict"        # Different task priorities
    ETHICAL_DILEMMA = "ethical_dilemma"           # Conflicting ethical constraints
    PERFORMANCE_TRADEOFF = "performance_tradeoff" # Speed vs. quality conflicts


@dataclass
class ConflictingInstructionsScenario(ChaosScenario):
    """
    Tests multi-agent systems' ability to handle conflicting instructions.

    This scenario introduces contradictory goals, resource competition, and
    priority conflicts between agents to test the system's negotiation,
    prioritization, and conflict-resolution protocols.
    """

    name: str = "Conflicting Agent Instructions Test"
    description: str = "Tests multi-agent conflict resolution and negotiation capabilities."

    # Configuration options
    conflict_types: List[ConflictType] = field(default_factory=list)
    conflict_intensity: float = 0.7  # 0.0 = mild conflicts, 1.0 = severe conflicts
    auto_resolve_conflicts: bool = False  # Whether to provide resolution mechanisms
    monitor_deadlocks: bool = True  # Whether to detect deadlock situations

    # Conflict scenarios
    conflict_scenarios: Dict[ConflictType, List[Dict[str, Any]]] = field(default_factory=dict)

    # Tracking
    original_instructions: Dict[Any, Dict[str, Any]] = field(default_factory=dict)
    conflicts_introduced: List[Dict[str, Any]] = field(default_factory=list)
    resolution_attempts: List[Dict[str, Any]] = field(default_factory=list)
    deadlocks_detected: List[Dict[str, Any]] = field(default_factory=list)

    def __post_init__(self):
        """Initialize the scenario with default conflict types and scenarios."""
        super().__post_init__()

        if not self.conflict_types:
            self.conflict_types = [
                ConflictType.RESOURCE_COMPETITION,
                ConflictType.CONTRADICTORY_GOALS,
                ConflictType.PRIORITY_CONFLICT,
                ConflictType.PERFORMANCE_TRADEOFF
            ]

        if not self.conflict_scenarios:
            self._initialize_conflict_scenarios()

    def _initialize_conflict_scenarios(self) -> None:
        """Initialize predefined conflict scenarios for each conflict type."""
        self.conflict_scenarios = {
            ConflictType.RESOURCE_COMPETITION: [
                {
                    "name": "API Rate Limit Competition",
                    "description": "Multiple agents compete for limited API calls",
                    "agent_a_goal": "Maximize data collection speed using all available API quota",
                    "agent_b_goal": "Ensure reliable operation by conserving API quota for critical tasks",
                    "resource": "api_quota",
                    "scarcity_level": self.conflict_intensity
                },
                {
                    "name": "Token Budget Competition",
                    "description": "Agents compete for limited token budget",
                    "agent_a_goal": "Generate comprehensive, detailed responses using maximum tokens",
                    "agent_b_goal": "Minimize token usage to stay within budget constraints",
                    "resource": "token_budget",
                    "scarcity_level": self.conflict_intensity
                },
                {
                    "name": "Processing Time Competition",
                    "description": "Agents compete for limited processing time",
                    "agent_a_goal": "Complete thorough analysis requiring maximum processing time",
                    "agent_b_goal": "Respond quickly to time-sensitive requests",
                    "resource": "processing_time",
                    "scarcity_level": self.conflict_intensity
                }
            ],

            ConflictType.CONTRADICTORY_GOALS: [
                {
                    "name": "Privacy vs. Transparency",
                    "description": "One agent maximizes privacy, another maximizes transparency",
                    "agent_a_goal": "Maximize data privacy and minimize information disclosure",
                    "agent_b_goal": "Provide maximum transparency and detailed explanations",
                    "conflict_domain": "information_sharing"
                },
                {
                    "name": "Security vs. Usability",
                    "description": "Security agent vs. user experience agent",
                    "agent_a_goal": "Implement maximum security measures and restrictions",
                    "agent_b_goal": "Optimize for user convenience and minimal friction",
                    "conflict_domain": "system_access"
                },
                {
                    "name": "Accuracy vs. Speed",
                    "description": "Quality control vs. rapid response",
                    "agent_a_goal": "Ensure maximum accuracy through thorough verification",
                    "agent_b_goal": "Provide rapid responses to meet time constraints",
                    "conflict_domain": "response_generation"
                }
            ],

            ConflictType.PRIORITY_CONFLICT: [
                {
                    "name": "Task Priority Disagreement",
                    "description": "Agents prioritize different aspects of the same task",
                    "agent_a_priority": "Immediate user satisfaction",
                    "agent_b_priority": "Long-term system stability",
                    "shared_task": "Handle user request",
                    "priority_weight_a": self.conflict_intensity,
                    "priority_weight_b": 1.0 - self.conflict_intensity
                },
                {
                    "name": "Resource Allocation Priority",
                    "description": "Different priorities for resource allocation",
                    "agent_a_priority": "Current user requests",
                    "agent_b_priority": "System maintenance and optimization",
                    "shared_resource": "computational_resources",
                    "priority_weight_a": self.conflict_intensity,
                    "priority_weight_b": 1.0 - self.conflict_intensity
                }
            ],

            ConflictType.PERFORMANCE_TRADEOFF: [
                {
                    "name": "Quality vs. Speed Tradeoff",
                    "description": "High-quality output vs. fast response time",
                    "agent_a_metric": "response_quality",
                    "agent_a_target": 0.95,  # 95% quality target
                    "agent_b_metric": "response_time",
                    "agent_b_target": 2.0,   # 2 second response time
                    "tradeoff_tension": self.conflict_intensity
                },
                {
                    "name": "Thoroughness vs. Efficiency",
                    "description": "Comprehensive analysis vs. resource efficiency",
                    "agent_a_metric": "analysis_depth",
                    "agent_a_target": 0.9,   # 90% thoroughness
                    "agent_b_metric": "resource_usage",
                    "agent_b_target": 0.3,   # 30% resource usage limit
                    "tradeoff_tension": self.conflict_intensity
                }
            ],

            ConflictType.ETHICAL_DILEMMA: [
                {
                    "name": "Autonomy vs. Safety",
                    "description": "User autonomy vs. safety constraints",
                    "agent_a_principle": "Maximize user autonomy and choice",
                    "agent_b_principle": "Ensure user and system safety",
                    "dilemma_context": "User requests potentially risky action",
                    "ethical_weight_a": self.conflict_intensity,
                    "ethical_weight_b": 1.0 - self.conflict_intensity
                },
                {
                    "name": "Individual vs. Collective Benefit",
                    "description": "Individual user benefit vs. collective system welfare",
                    "agent_a_principle": "Optimize for individual user satisfaction",
                    "agent_b_principle": "Optimize for overall system welfare",
                    "dilemma_context": "Resource allocation decision",
                    "ethical_weight_a": self.conflict_intensity,
                    "ethical_weight_b": 1.0 - self.conflict_intensity
                }
            ]
        }

    def setup(self) -> None:
        """Prepare the conflicting instructions scenario."""
        logger.info("Setting up Conflicting Instructions scenario")
        self.original_instructions.clear()
        self.conflicts_introduced.clear()
        self.resolution_attempts.clear()
        self.deadlocks_detected.clear()

    def _introduce_conflict(self, agents: List[Any], conflict_type: ConflictType) -> Dict[str, Any]:
        """
        Introduce a specific type of conflict between agents.

        Args:
            agents: List of agents to create conflicts between
            conflict_type: The type of conflict to introduce

        Returns:
            Details about the conflict introduced
        """
        if len(agents) < 2:
            logger.warning("Need at least 2 agents to create conflicts")
            return {}

        # Select a conflict scenario for this type
        scenarios = self.conflict_scenarios.get(conflict_type, [])
        if not scenarios:
            logger.warning(f"No scenarios defined for conflict type {conflict_type}")
            return {}

        scenario = random.choice(scenarios)

        # Select two agents for the conflict
        agent_a, agent_b = random.sample(agents, 2)

        conflict_details = {
            "conflict_type": conflict_type,
            "scenario": scenario,
            "agent_a": agent_a,
            "agent_b": agent_b,
            "timestamp": time.time(),
            "resolved": False,
            "resolution_method": None
        }

        # Apply the conflict based on its type
        try:
            if conflict_type == ConflictType.RESOURCE_COMPETITION:
                self._apply_resource_competition(agent_a, agent_b, scenario)

            elif conflict_type == ConflictType.CONTRADICTORY_GOALS:
                self._apply_contradictory_goals(agent_a, agent_b, scenario)

            elif conflict_type == ConflictType.PRIORITY_CONFLICT:
                self._apply_priority_conflict(agent_a, agent_b, scenario)

            elif conflict_type == ConflictType.PERFORMANCE_TRADEOFF:
                self._apply_performance_tradeoff(agent_a, agent_b, scenario)

            elif conflict_type == ConflictType.ETHICAL_DILEMMA:
                self._apply_ethical_dilemma(agent_a, agent_b, scenario)

            logger.info(f"Introduced {conflict_type.value} conflict: {scenario['name']}")

        except Exception as e:
            logger.error(f"Failed to apply conflict {conflict_type}: {e}")
            conflict_details["error"] = str(e)

        return conflict_details

    def _apply_resource_competition(self, agent_a: Any, agent_b: Any, scenario: Dict[str, Any]) -> None:
        """Apply resource competition conflict between agents."""
        # This is a simplified implementation
        # In practice, this would modify agent configurations or constraints

        # Store original configurations if possible
        self._store_original_config(agent_a, "resource_allocation")
        self._store_original_config(agent_b, "resource_allocation")

        # Apply conflicting resource goals
        try:
            if hasattr(agent_a, 'set_goal') or hasattr(agent_a, 'configure'):
                self._set_agent_constraint(agent_a, scenario["agent_a_goal"])

            if hasattr(agent_b, 'set_goal') or hasattr(agent_b, 'configure'):
                self._set_agent_constraint(agent_b, scenario["agent_b_goal"])

        except Exception as e:
            logger.warning(f"Could not apply resource competition: {e}")

    def _apply_contradictory_goals(self, agent_a: Any, agent_b: Any, scenario: Dict[str, Any]) -> None:
        """Apply contradictory goals conflict between agents."""
        self._store_original_config(agent_a, "goals")
        self._store_original_config(agent_b, "goals")

        try:
            self._set_agent_constraint(agent_a, scenario["agent_a_goal"])
            self._set_agent_constraint(agent_b, scenario["agent_b_goal"])
        except Exception as e:
            logger.warning(f"Could not apply contradictory goals: {e}")

    def _apply_priority_conflict(self, agent_a: Any, agent_b: Any, scenario: Dict[str, Any]) -> None:
        """Apply priority conflict between agents."""
        self._store_original_config(agent_a, "priorities")
        self._store_original_config(agent_b, "priorities")

        try:
            # Set different priorities
            priority_a = f"PRIORITY: {scenario['agent_a_priority']} (weight: {scenario.get('priority_weight_a', 1.0)})"
            priority_b = f"PRIORITY: {scenario['agent_b_priority']} (weight: {scenario.get('priority_weight_b', 1.0)})"

            self._set_agent_constraint(agent_a, priority_a)
            self._set_agent_constraint(agent_b, priority_b)
        except Exception as e:
            logger.warning(f"Could not apply priority conflict: {e}")

    def _apply_performance_tradeoff(self, agent_a: Any, agent_b: Any, scenario: Dict[str, Any]) -> None:
        """Apply performance tradeoff conflict between agents."""
        self._store_original_config(agent_a, "performance_targets")
        self._store_original_config(agent_b, "performance_targets")

        try:
            target_a = f"OPTIMIZE FOR: {scenario['agent_a_metric']} >= {scenario['agent_a_target']}"
            target_b = f"OPTIMIZE FOR: {scenario['agent_b_metric']} <= {scenario['agent_b_target']}"

            self._set_agent_constraint(agent_a, target_a)
            self._set_agent_constraint(agent_b, target_b)
        except Exception as e:
            logger.warning(f"Could not apply performance tradeoff: {e}")

    def _apply_ethical_dilemma(self, agent_a: Any, agent_b: Any, scenario: Dict[str, Any]) -> None:
        """Apply ethical dilemma conflict between agents."""
        self._store_original_config(agent_a, "ethical_principles")
        self._store_original_config(agent_b, "ethical_principles")

        try:
            principle_a = f"ETHICAL PRINCIPLE: {scenario['agent_a_principle']}"
            principle_b = f"ETHICAL PRINCIPLE: {scenario['agent_b_principle']}"

            self._set_agent_constraint(agent_a, principle_a)
            self._set_agent_constraint(agent_b, principle_b)
        except Exception as e:
            logger.warning(f"Could not apply ethical dilemma: {e}")

    def _store_original_config(self, agent: Any, config_type: str) -> None:
        """Store the original configuration of an agent."""
        if agent not in self.original_instructions:
            self.original_instructions[agent] = {}

        # Try to capture current configuration
        # This is highly framework-dependent
        try:
            if hasattr(agent, 'get_config'):
                self.original_instructions[agent][config_type] = agent.get_config()
            elif hasattr(agent, 'config'):
                self.original_instructions[agent][config_type] = getattr(agent, 'config', None)
            elif hasattr(agent, 'instructions'):
                self.original_instructions[agent][config_type] = getattr(agent, 'instructions', None)
        except Exception as e:
            logger.debug(f"Could not store original config for {config_type}: {e}")

    def _set_agent_constraint(self, agent: Any, constraint: str) -> None:
        """Set a constraint or instruction on an agent."""
        # This is a simplified approach - real implementation would need
        # to understand the specific agent framework being used

        try:
            # Try common methods for setting agent instructions/goals
            if hasattr(agent, 'set_system_message'):
                current_msg = getattr(agent, 'system_message', '')
                agent.set_system_message(f"{current_msg}\n\nADDITIONAL CONSTRAINT: {constraint}")

            elif hasattr(agent, 'add_instruction'):
                agent.add_instruction(constraint)

            elif hasattr(agent, 'set_goal'):
                agent.set_goal(constraint)

            elif hasattr(agent, 'configure'):
                agent.configure(additional_instruction=constraint)

            else:
                # If no specific method, try to modify common attributes
                if hasattr(agent, 'instructions'):
                    current = getattr(agent, 'instructions', '')
                    agent.instructions = f"{current}\n{constraint}"
                elif hasattr(agent, 'system_message'):
                    current = getattr(agent, 'system_message', '')
                    agent.system_message = f"{current}\n{constraint}"
                else:
                    logger.warning(f"Could not set constraint on agent {agent.__class__.__name__}")

        except Exception as e:
            logger.warning(f"Failed to set agent constraint: {e}")

    def _detect_deadlock(self, agents: List[Any]) -> Optional[Dict[str, Any]]:
        """
        Attempt to detect if agents are in a deadlock situation.

        This is a simplified implementation - real deadlock detection
        would need to monitor agent interactions over time.
        """
        if not self.monitor_deadlocks:
            return None

        # This is a placeholder for deadlock detection logic
        # Real implementation would need to:
        # 1. Monitor agent interactions
        # 2. Detect circular waiting or infinite loops
        # 3. Identify resource contention
        # 4. Track progress indicators

        # For now, we'll just return a placeholder
        return {
            "detected": False,
            "type": "none",
            "agents_involved": [],
            "timestamp": time.time()
        }

    def _attempt_conflict_resolution(self, conflict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Attempt to resolve a conflict (if auto-resolution is enabled).

        Args:
            conflict: The conflict to attempt to resolve

        Returns:
            Resolution attempt details
        """
        if not self.auto_resolve_conflicts:
            return {"attempted": False, "reason": "auto_resolve_conflicts disabled"}

        resolution_attempt = {
            "conflict_id": id(conflict),
            "timestamp": time.time(),
            "method": "negotiation",
            "success": False,
            "details": {}
        }

        # Simplified resolution attempt
        # Real implementation would need sophisticated negotiation logic

        try:
            conflict_type = conflict["conflict_type"]

            if conflict_type == ConflictType.RESOURCE_COMPETITION:
                # Try resource sharing or priority-based allocation
                resolution_attempt["method"] = "resource_sharing"
                resolution_attempt["details"] = {
                    "strategy": "time_based_sharing",
                    "allocation": "50/50 split with alternating priority"
                }

            elif conflict_type == ConflictType.PRIORITY_CONFLICT:
                # Try priority negotiation
                resolution_attempt["method"] = "priority_negotiation"
                resolution_attempt["details"] = {
                    "strategy": "weighted_compromise",
                    "weights": "based_on_urgency_and_impact"
                }

            # Mark as potentially successful (in reality, would need to verify)
            resolution_attempt["success"] = random.random() > 0.5  # 50% success rate

        except Exception as e:
            resolution_attempt["error"] = str(e)

        return resolution_attempt

    def restore_agents(self) -> None:
        """Restore all agents to their original configurations."""
        for agent, configs in self.original_instructions.items():
            try:
                # Try to restore original configurations
                for config_type, original_config in configs.items():
                    if original_config is not None:
                        if hasattr(agent, 'set_config'):
                            agent.set_config(original_config)
                        elif hasattr(agent, config_type):
                            setattr(agent, config_type, original_config)

                logger.info(f"Restored original configuration for {agent.__class__.__name__}")

            except Exception as e:
                logger.warning(f"Could not restore agent configuration: {e}")

    def run(self, target: Any) -> Dict[str, Any]:
        """
        Execute the conflicting instructions scenario.

        Args:
            target: The target multi-agent system or individual agents

        Returns:
            A dictionary containing test results and observations
        """
        self.setup()

        # Record observations
        observations = []
        success = False
        details = {
            "scenario_type": self.__class__.__name__,
            "conflicts_introduced": 0,
            "conflict_types_tested": [],
            "resolution_attempts": 0,
            "successful_resolutions": 0,
            "deadlocks_detected": 0,
            "agents_involved": 0
        }

        try:
            # Identify agents to work with
            agents = []

            if isinstance(target, list):
                # Target is already a list of agents
                agents = target
            elif hasattr(target, 'agents'):
                # Target is a multi-agent system with an agents attribute
                agents = target.agents
            elif hasattr(target, 'get_agents'):
                # Target has a method to get agents
                agents = target.get_agents()
            else:
                # Target might be a single agent
                agents = [target]

            if len(agents) < 2:
                observations.append("Need at least 2 agents to test conflicting instructions")
                observations.append("Single agent systems cannot demonstrate conflict resolution")
                return {
                    "success": False,
                    "observations": observations,
                    "details": details
                }

            details["agents_involved"] = len(agents)
            observations.append(f"Identified {len(agents)} agents for conflict testing")

            # Introduce conflicts for each type
            for conflict_type in self.conflict_types:
                conflict = self._introduce_conflict(agents, conflict_type)

                if conflict:
                    self.conflicts_introduced.append(conflict)
                    details["conflicts_introduced"] += 1
                    details["conflict_types_tested"].append(conflict_type.value)

                    observations.append(f"Introduced {conflict_type.value}: {conflict['scenario']['name']}")

                    # Attempt resolution if enabled
                    if self.auto_resolve_conflicts:
                        resolution = self._attempt_conflict_resolution(conflict)
                        self.resolution_attempts.append(resolution)
                        details["resolution_attempts"] += 1

                        if resolution.get("success", False):
                            details["successful_resolutions"] += 1
                            conflict["resolved"] = True
                            conflict["resolution_method"] = resolution["method"]

            # Check for deadlocks
            if self.monitor_deadlocks:
                deadlock = self._detect_deadlock(agents)
                if deadlock and deadlock.get("detected", False):
                    self.deadlocks_detected.append(deadlock)
                    details["deadlocks_detected"] += 1
                    observations.append(f"Detected deadlock: {deadlock['type']}")

            # Provide testing guidance
            if details["conflicts_introduced"] > 0:
                observations.append(
                    f"Successfully introduced {details['conflicts_introduced']} conflicts. "
                    "Now run multi-agent tasks to observe conflict resolution behavior."
                )

                observations.append(
                    "Watch for: negotiation attempts, priority resolution, resource sharing, "
                    "escalation mechanisms, or deadlock prevention."
                )

                if details["successful_resolutions"] > 0:
                    observations.append(
                        f"Automatic resolution succeeded for {details['successful_resolutions']} conflicts"
                    )

                # Success if we introduced conflicts successfully
                success = True
            else:
                observations.append("Failed to introduce any conflicts")
                success = False

        finally:
            # Always restore the original agent configurations
            self.restore_agents()
            observations.append("Restored all agents to original configurations")

        self.teardown()

        return {
            "success": success,
            "observations": observations,
            "details": details
        }
