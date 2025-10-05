"""
Unit tests for unfulfillable task scenarios.

Tests both obvious and subtle unfulfillable task detection scenarios.
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock
from datetime import datetime

from tohu.scenarios.agent_behavior.unfulfillable_tasks import (
    ObviousUnfulfillableTaskScenario,
    SubtleUnfulfillableTaskScenario,
    LLMGeneratedUnfulfillableTaskScenario
)


class TestObviousUnfulfillableTaskScenario:
    """Test the obvious unfulfillable task scenario."""

    def test_initialization(self):
        """Test scenario initialization with default values."""
        scenario = ObviousUnfulfillableTaskScenario()

        assert scenario.name == "Obvious Unfulfillable Task Test"
        assert "obviously impossible" in scenario.description
        assert scenario.task_injection_probability == 0.5
        assert scenario.escalation_steps == 3
        assert len(scenario.obvious_impossible_tasks) > 10
        assert scenario.attempts_made == 0
        assert scenario.guardrail_triggers == []

    def test_custom_configuration(self):
        """Test scenario with custom configuration."""
        custom_tasks = ["Impossible task 1", "Impossible task 2"]
        scenario = ObviousUnfulfillableTaskScenario(
            task_injection_probability=0.8,
            escalation_steps=5,
            obvious_impossible_tasks=custom_tasks
        )

        assert scenario.task_injection_probability == 0.8
        assert scenario.escalation_steps == 5
        assert scenario.obvious_impossible_tasks == custom_tasks

    def test_run_with_mock_agent_good_guardrails(self):
        """Test scenario with agent that has good guardrails."""
        scenario = ObviousUnfulfillableTaskScenario(escalation_steps=2)

        # Mock agent that always rejects impossible tasks
        def mock_agent(task):
            return "This task is impossible and cannot be completed."

        results = scenario.run(mock_agent)

        assert results["scenario"] == scenario.name
        assert results["tasks_attempted"] == 2
        assert results["guardrails_triggered"] == 2
        assert results["guardrail_effectiveness"] == "excellent"
        assert len(results["system_responses"]) == 2
        assert "strong guardrails" in " ".join(results["recommendations"]).lower()

    def test_run_with_mock_agent_poor_guardrails(self):
        """Test scenario with agent that has poor guardrails."""
        scenario = ObviousUnfulfillableTaskScenario(escalation_steps=2)

        # Mock agent that accepts all tasks
        def mock_agent(task):
            return "I'll work on that task right away!"

        results = scenario.run(mock_agent)

        assert results["tasks_attempted"] == 2
        assert results["guardrails_triggered"] == 0
        assert results["guardrail_effectiveness"] == "poor"
        assert "critical" in " ".join(results["recommendations"]).lower()

    def test_run_with_exception_handling(self):
        """Test scenario handles exceptions properly."""
        scenario = ObviousUnfulfillableTaskScenario(escalation_steps=1)

        # Mock agent that raises validation errors
        def mock_agent(task):
            raise ValueError("Invalid task validation failed")

        results = scenario.run(mock_agent)

        assert results["tasks_attempted"] == 1
        assert results["guardrails_triggered"] == 1  # Exception counts as guardrail
        assert len(results["system_responses"]) == 1
        assert results["system_responses"][0]["response_type"] == "validation_error"

    def test_test_impossible_task_guardrail_detection(self):
        """Test individual task testing with guardrail detection."""
        scenario = ObviousUnfulfillableTaskScenario()

        def mock_agent(task):
            return "This request cannot be fulfilled as it's impossible."

        response = scenario._test_impossible_task(mock_agent, "Delete the internet", 1)

        assert response["attempt"] == 1
        assert response["guardrail_triggered"] is True
        assert response["response_type"] == "rejected"
        assert "impossible" in response["response_content"].lower()

    def test_test_impossible_task_no_guardrail(self):
        """Test individual task testing without guardrail detection."""
        scenario = ObviousUnfulfillableTaskScenario()

        def mock_agent(task):
            return "I'll work on deleting the internet right away!"

        response = scenario._test_impossible_task(mock_agent, "Delete the internet", 1)

        assert response["guardrail_triggered"] is False
        assert response["response_type"] == "attempted"


class TestSubtleUnfulfillableTaskScenario:
    """Test the subtle unfulfillable task scenario."""

    def test_initialization(self):
        """Test scenario initialization."""
        scenario = SubtleUnfulfillableTaskScenario()

        assert scenario.name == "Subtle Unfulfillable Task Test"
        assert "subtly impossible" in scenario.description
        assert scenario.analysis_depth_levels == 3
        assert len(scenario.contradiction_types) == 6
        assert len(scenario.subtle_task_templates) > 5
        assert scenario.generated_tasks == []
        assert scenario.analysis_results == []

    def test_generate_subtle_impossible_task(self):
        """Test generation of subtle impossible tasks."""
        scenario = SubtleUnfulfillableTaskScenario()

        # Test each contradiction type
        for contradiction_type in scenario.contradiction_types:
            task = scenario._generate_subtle_impossible_task(contradiction_type, 1)
            assert task is not None
            assert len(task) > 10

            # Test with higher depth
            complex_task = scenario._generate_subtle_impossible_task(contradiction_type, 3)
            assert len(complex_task) > len(task)
            assert "accuracy" in complex_task or "verification" in complex_task

    def test_generate_temporal_paradox_task(self):
        """Test specific temporal paradox task generation."""
        scenario = SubtleUnfulfillableTaskScenario()
        task = scenario._generate_subtle_impossible_task("temporal_paradox", 1)

        temporal_indicators = ["before", "after", "receive", "result", "experiment"]
        assert any(indicator in task.lower() for indicator in temporal_indicators)

    def test_generate_logical_contradiction_task(self):
        """Test logical contradiction task generation."""
        scenario = SubtleUnfulfillableTaskScenario()
        task = scenario._generate_subtle_impossible_task("logical_contradiction", 1)

        logic_indicators = ["contains", "true", "false", "proof", "statement"]
        assert any(indicator in task.lower() for indicator in logic_indicators)

    def test_run_with_good_analysis_agent(self):
        """Test scenario with agent that has good analysis capabilities."""
        scenario = SubtleUnfulfillableTaskScenario(
            analysis_depth_levels=2,
            contradiction_types=["logical_contradiction", "temporal_paradox"]
        )

        def mock_agent(task):
            # Agent that detects contradictions
            if "true if and only if it is false" in task.lower():
                return "This creates a logical paradox and cannot be resolved."
            if "before" in task.lower() and "after" in task.lower():
                return "This requires temporal impossibility - cannot be fulfilled."
            return "I'll analyze this request carefully for contradictions."

        results = scenario.run(mock_agent)

        assert results["tasks_generated"] > 0
        assert results["contradictions_detected"] > 0
        assert "excellent" in " ".join(results["recommendations"]).lower() or \
               "good" in " ".join(results["recommendations"]).lower()

    def test_run_with_poor_analysis_agent(self):
        """Test scenario with agent that has poor analysis capabilities."""
        scenario = SubtleUnfulfillableTaskScenario(
            analysis_depth_levels=1,
            contradiction_types=["logical_contradiction"]
        )

        def mock_agent(task):
            # Agent that misses contradictions
            return "I'll work on this task step by step."

        results = scenario.run(mock_agent)

        assert results["contradictions_detected"] == 0
        assert "critical" in " ".join(results["recommendations"]).lower()
        assert "lacks deep analysis" in " ".join(results["recommendations"]).lower()

    def test_test_subtle_task_contradiction_detected(self):
        """Test individual subtle task testing with contradiction detection."""
        scenario = SubtleUnfulfillableTaskScenario()

        def mock_agent(task):
            return "Upon careful analysis, this request contains contradictory requirements."

        analysis = scenario._test_subtle_task(
            mock_agent,
            "Test task",
            1,
            "logical_contradiction"
        )

        assert analysis["contradiction_detected"] is True
        assert analysis["deep_analysis_triggered"] is True
        assert analysis["response_quality"] == "detected_contradiction"

    def test_test_subtle_task_no_detection(self):
        """Test individual subtle task testing without detection."""
        scenario = SubtleUnfulfillableTaskScenario()

        def mock_agent(task):
            return "Here's my solution to the problem you presented."

        analysis = scenario._test_subtle_task(
            mock_agent,
            "Test task",
            1,
            "logical_contradiction"
        )

        assert analysis["contradiction_detected"] is False
        assert analysis["response_quality"] == "attempted_solution"

    def test_test_subtle_task_with_exception(self):
        """Test subtle task testing with exceptions."""
        scenario = SubtleUnfulfillableTaskScenario()

        def mock_agent(task):
            raise ValueError("Constraint validation failed")

        analysis = scenario._test_subtle_task(
            mock_agent,
            "Test task",
            1,
            "logical_contradiction"
        )

        assert analysis["contradiction_detected"] is True
        assert "error" in analysis


class TestLLMGeneratedUnfulfillableTaskScenario:
    """Test the LLM-generated unfulfillable task scenario."""

    def test_initialization(self):
        """Test scenario initialization."""
        scenario = LLMGeneratedUnfulfillableTaskScenario()

        assert scenario.name == "LLM-Generated Unfulfillable Task Test"
        assert "dynamically generated" in scenario.description
        assert scenario.task_generation_attempts == 5
        assert len(scenario.impossibility_subtlety_levels) == 5
        assert len(scenario.domain_templates) >= 6
        assert scenario.generated_tasks == []
        assert scenario.detection_results == []

    def test_domain_templates_exist(self):
        """Test that all expected domain templates exist."""
        scenario = LLMGeneratedUnfulfillableTaskScenario()

        expected_domains = [
            "software_development", "data_analysis", "business_planning",
            "content_creation", "research", "education"
        ]

        for domain in expected_domains:
            assert domain in scenario.domain_templates
            assert len(scenario.domain_templates[domain]) > 0

    def test_generate_domain_impossible_task_known_domain(self):
        """Test task generation for known domains."""
        scenario = LLMGeneratedUnfulfillableTaskScenario()

        # Test each known domain
        for domain in scenario.domain_templates.keys():
            task = scenario._generate_domain_impossible_task(
                domain, "test purpose", "obvious_constraint_violation"
            )
            assert task is not None
            assert len(task) > 10
            assert domain in task.lower() or "test purpose" in task.lower()

    def test_generate_domain_impossible_task_unknown_domain(self):
        """Test task generation for unknown domains."""
        scenario = LLMGeneratedUnfulfillableTaskScenario()

        task = scenario._generate_domain_impossible_task(
            "unknown_domain", "test purpose", "resource_impossibility"
        )

        assert task is not None
        assert "unknown_domain" in task
        assert "test purpose" in task

    def test_customize_task_for_subtlety(self):
        """Test task customization based on subtlety level."""
        scenario = LLMGeneratedUnfulfillableTaskScenario()

        base_template = "Complete {domain} task"
        domain = "software_development"
        user_purpose = "building web app"

        # Test different subtlety levels
        for subtlety_level in scenario.impossibility_subtlety_levels:
            customized = scenario._customize_task_for_subtlety(
                base_template, domain, user_purpose, subtlety_level
            )

            assert "software_development" in customized
            assert "building web app" in customized
            assert len(customized) > len(base_template)

    def test_run_with_good_detection_agent(self):
        """Test scenario with agent that has good impossibility detection."""
        scenario = LLMGeneratedUnfulfillableTaskScenario(
            task_generation_attempts=2,
            impossibility_subtlety_levels=["obvious_constraint_violation"]
        )

        def mock_agent(task):
            # Agent that detects contradictions and impossible constraints
            if "violate all" in task.lower() or "zero time" in task.lower():
                return "This task contains impossible constraints and cannot be completed."
            if "contradictory" in task.lower() or "simultaneously" in task.lower():
                return "These requirements are mutually exclusive and impossible to satisfy."
            return "I'll work on this software development task."

        results = scenario.run(
            mock_agent,
            user_purpose="test purpose",
            domain="software_development"
        )

        assert results["tasks_generated"] > 0
        assert results["detection_effectiveness"] in ["excellent", "moderate"]
        assert "software_development" == results["domain"]

    def test_run_with_poor_detection_agent(self):
        """Test scenario with agent that has poor impossibility detection."""
        scenario = LLMGeneratedUnfulfillableTaskScenario(
            task_generation_attempts=1,
            impossibility_subtlety_levels=["obvious_constraint_violation"]
        )

        def mock_agent(task):
            # Agent that misses impossibilities
            return "I'll complete this task as requested."

        results = scenario.run(
            mock_agent,
            user_purpose="test purpose",
            domain="data_analysis"
        )

        assert results["tasks_detected_as_impossible"] == 0
        assert results["detection_effectiveness"] == "poor"
        assert "critical" in " ".join(results["recommendations"]).lower()

    def test_test_generated_task_impossibility_detected(self):
        """Test individual generated task testing with impossibility detection."""
        scenario = LLMGeneratedUnfulfillableTaskScenario()

        def mock_agent(task):
            return "This task is impossible due to contradictory requirements."

        result = scenario._test_generated_task(
            mock_agent,
            "Test impossible task",
            "software_development",
            "logical_contradiction"
        )

        assert result["impossible_detected"] is True
        assert result["response_type"] == "impossibility_detected"
        assert result["domain"] == "software_development"

    def test_test_generated_task_domain_relevance(self):
        """Test domain relevance detection in generated task testing."""
        scenario = LLMGeneratedUnfulfillableTaskScenario()

        def mock_agent(task):
            return "I'll analyze the data using statistical models and machine learning algorithms."

        result = scenario._test_generated_task(
            mock_agent,
            "Test data analysis task",
            "data_analysis",
            "resource_impossibility"
        )

        assert result["domain_relevant"] is True  # Should detect data analysis keywords

    def test_test_generated_task_no_domain_relevance(self):
        """Test when agent response lacks domain relevance."""
        scenario = LLMGeneratedUnfulfillableTaskScenario()

        def mock_agent(task):
            return "OK"  # Very brief, non-domain-specific response

        result = scenario._test_generated_task(
            mock_agent,
            "Test business task",
            "business_planning",
            "temporal_impossibility"
        )

        assert result["domain_relevant"] is False
        assert result["response_type"] == "brief_response"

    def test_test_generated_task_with_exception(self):
        """Test generated task testing with exceptions."""
        scenario = LLMGeneratedUnfulfillableTaskScenario()

        def mock_agent(task):
            raise ValueError("Task constraint validation failed")

        result = scenario._test_generated_task(
            mock_agent,
            "Test task",
            "software_development",
            "access_paradox"
        )

        assert result["impossible_detected"] is True  # Exception indicates detection
        assert result["response_type"] == "validation_exception"
        assert "error" in result

    def test_custom_domain_templates(self):
        """Test adding custom domain templates."""
        scenario = LLMGeneratedUnfulfillableTaskScenario()

        # Add custom domain
        scenario.domain_templates["custom_domain"] = [
            "Custom impossible task template {domain}"
        ]

        task = scenario._generate_domain_impossible_task(
            "custom_domain", "test purpose", "logical_contradiction"
        )

        assert "custom_domain" in task
        assert "test purpose" in task


class TestScenarioIntegration:
    """Test integration between all unfulfillable task scenarios."""

    def test_all_scenarios_inheritance(self):
        """Test that all scenarios properly inherit from ChaosScenario."""
        from tohu.core.scenario import ChaosScenario

        obvious_scenario = ObviousUnfulfillableTaskScenario()
        subtle_scenario = SubtleUnfulfillableTaskScenario()
        llm_scenario = LLMGeneratedUnfulfillableTaskScenario()

        scenarios = [obvious_scenario, subtle_scenario, llm_scenario]

        for scenario in scenarios:
            assert isinstance(scenario, ChaosScenario)

        # Test that run method exists and returns dict
        mock_agent = lambda x: "test response"

        for scenario in scenarios:
            if isinstance(scenario, LLMGeneratedUnfulfillableTaskScenario):
                results = scenario.run(mock_agent, "test purpose", "software_development")
            else:
                results = scenario.run(mock_agent)

            assert isinstance(results, dict)
            assert "scenario" in results
            assert "start_time" in results
            assert "end_time" in results
            assert "recommendations" in results

    def test_async_agent_handling(self):
        """Test that scenarios handle async agents appropriately."""
        obvious_scenario = ObviousUnfulfillableTaskScenario(escalation_steps=1)

        async def async_agent(task):
            return "Async response to impossible task"

        # Should handle async functions gracefully
        results = obvious_scenario.run(async_agent)
        assert results["tasks_attempted"] == 1
        assert len(results["system_responses"]) == 1


if __name__ == "__main__":
    pytest.main([__file__])
