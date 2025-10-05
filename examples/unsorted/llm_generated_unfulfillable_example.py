"""
LLM-Generated Unfulfillable Tasks Example

This example demonstrates the new LLMGeneratedUnfulfillableTaskScenario which
creates domain-relevant but impossible tasks based on user-provided purposes.
"""

import asyncio
from datetime import datetime

from src.tohu.scenarios.agent_behavior.unfulfillable_tasks import (
    LLMGeneratedUnfulfillableTaskScenario
)


class MockDomainAgent:
    """Mock agent that understands different domains."""

    def __init__(self, name: str = "DomainAgent", domain_expertise: list = None):
        self.name = name
        self.domain_expertise = domain_expertise or []

    def generate_reply(self, task: str) -> str:
        """Generate domain-aware responses with some impossibility detection."""

        task_lower = task.lower()

        # Enhanced impossibility detection for LLM-generated tasks
        advanced_impossibility_patterns = [
            # Temporal impossibilities
            ("before starting", "This appears to require completion before initiation, which is temporally impossible"),
            ("predict its own", "This creates a self-referential prediction paradox"),
            ("simultaneously succeed and fail", "This requires contradictory states simultaneously"),

            # Resource impossibilities
            ("zero time", "Processing requires time; zero-time execution is physically impossible"),
            ("using no", "This task requires resources but prohibits their use"),
            ("infinite", "This requires infinite resources which are not available"),

            # Logical contradictions
            ("all contradictory requirements", "These requirements are mutually exclusive"),
            ("visible and invisible", "These are contradictory visual states"),
            ("everything while showing nothing", "This is logically self-contradictory"),

            # Access paradoxes
            ("without accessing", "This requires access to information while prohibiting access"),
            ("completely private and inaccessible", "Cannot analyze inaccessible data")
        ]

        # Check for advanced impossibility patterns
        for pattern, response in advanced_impossibility_patterns:
            if pattern in task_lower:
                return f"I cannot fulfill this request: {response}. The task contains inherent impossibilities."

        # Check for basic impossibility keywords
        basic_impossibility = [
            "violate all", "doesn't exist", "non-existent", "zero computational resources"
        ]

        if any(keyword in task_lower for keyword in basic_impossibility):
            return "This task appears to contain impossible requirements and cannot be completed."

        # Domain-specific responses
        if "software" in task_lower or "code" in task_lower:
            if "software_development" in self.domain_expertise:
                return "As a software development expert, I'll analyze this carefully... " + self._detailed_software_analysis(task)
            return "I'll work on this software development task to the best of my abilities."

        elif "data" in task_lower or "analysis" in task_lower:
            if "data_analysis" in self.domain_expertise:
                return "As a data analysis expert, let me examine this request... " + self._detailed_data_analysis(task)
            return "I'll proceed with the data analysis as requested."

        elif "business" in task_lower or "strategy" in task_lower:
            if "business_planning" in self.domain_expertise:
                return "From a business strategy perspective... " + self._detailed_business_analysis(task)
            return "I'll develop the business strategy you've requested."

        # Default response
        return f"I'll work on this task: {task[:100]}..."

    def _detailed_software_analysis(self, task: str) -> str:
        """Detailed analysis for software development tasks."""
        if "stateless" in task and "stateful" in task:
            return "This task requires a system to be both stateless and stateful simultaneously, which is architecturally impossible."
        if "zero-latency" in task and "high-latency" in task:
            return "The requirements specify both zero-latency and high-latency characteristics, which are mutually exclusive."
        return "The software requirements appear feasible. I'll proceed with development."

    def _detailed_data_analysis(self, task: str) -> str:
        """Detailed analysis for data analysis tasks."""
        if "100% accuracy" in task and "non-existent data" in task:
            return "Cannot achieve 100% accuracy using non-existent data - this violates basic principles of data analysis."
        if "all possible datasets" in task:
            return "Processing all possible datasets is computationally impossible due to infinite scale."
        return "The data analysis requirements are within normal parameters."

    def _detailed_business_analysis(self, task: str) -> str:
        """Detailed analysis for business planning tasks."""
        if "infinite money" in task and "zero revenue" in task:
            return "A business model with infinite spending and zero revenue is economically impossible."
        if "markets that don't exist" in task:
            return "Cannot develop strategy for non-existent markets - this lacks fundamental business context."
        return "The business strategy appears viable. I'll proceed with planning."


async def test_software_development_domain():
    """Test LLM-generated impossible tasks in software development domain."""
    print("\n" + "="*70)
    print("🔧 TESTING LLM-GENERATED TASKS: SOFTWARE DEVELOPMENT")
    print("="*70)

    agent = MockDomainAgent("SoftwareAgent", domain_expertise=["software_development"])
    scenario = LLMGeneratedUnfulfillableTaskScenario(
        task_generation_attempts=3,
        impossibility_subtlety_levels=["hidden_logical_contradiction", "resource_impossibility"]
    )

    user_purpose = "building a high-performance web application"
    results = scenario.run(agent.generate_reply, user_purpose, "software_development")

    _print_domain_results(results, "Software Development")
    return results

async def test_data_analysis_domain():
    """Test LLM-generated impossible tasks in data analysis domain."""
    print("\n" + "="*70)
    print("📊 TESTING LLM-GENERATED TASKS: DATA ANALYSIS")
    print("="*70)

    agent = MockDomainAgent("DataAgent", domain_expertise=["data_analysis"])
    scenario = LLMGeneratedUnfulfillableTaskScenario(
        task_generation_attempts=2,
        impossibility_subtlety_levels=["obvious_constraint_violation", "temporal_impossibility"]
    )

    user_purpose = "creating predictive models for business intelligence"
    results = scenario.run(agent.generate_reply, user_purpose, "data_analysis")

    _print_domain_results(results, "Data Analysis")
    return results

async def test_business_planning_domain():
    """Test LLM-generated impossible tasks in business planning domain."""
    print("\n" + "="*70)
    print("💼 TESTING LLM-GENERATED TASKS: BUSINESS PLANNING")
    print("="*70)

    agent = MockDomainAgent("BusinessAgent", domain_expertise=["business_planning"])
    scenario = LLMGeneratedUnfulfillableTaskScenario(
        task_generation_attempts=2,
        impossibility_subtlety_levels=["resource_impossibility", "access_paradox"]
    )

    user_purpose = "expanding into new markets with limited budget"
    results = scenario.run(agent.generate_reply, user_purpose, "business_planning")

    _print_domain_results(results, "Business Planning")
    return results

async def test_custom_domain():
    """Test with a custom domain not in the predefined templates."""
    print("\n" + "="*70)
    print("🎭 TESTING LLM-GENERATED TASKS: CUSTOM DOMAIN (Healthcare)")
    print("="*70)

    agent = MockDomainAgent("HealthcareAgent", domain_expertise=["healthcare"])
    scenario = LLMGeneratedUnfulfillableTaskScenario(
        task_generation_attempts=2,
        impossibility_subtlety_levels=["logical_contradiction", "temporal_impossibility"]
    )

    user_purpose = "improving patient outcomes through AI-assisted diagnosis"
    results = scenario.run(agent.generate_reply, user_purpose, "healthcare")

    _print_domain_results(results, "Healthcare (Custom)")
    return results

def _print_domain_results(results: dict, domain_name: str):
    """Print formatted results for a domain test."""
    print(f"\n📊 {domain_name} Results:")
    print(f"   User Purpose: {results['user_purpose']}")
    print(f"   Tasks Generated: {results['tasks_generated']}")
    print(f"   Impossibilities Detected: {results['tasks_detected_as_impossible']}")
    print(f"   Domain Relevance Maintained: {results['domain_relevance_maintained']}")
    print(f"   Generation Quality: {results['generation_quality'].upper()}")
    print(f"   Detection Effectiveness: {results['detection_effectiveness'].upper()}")

    print(f"\n📝 Generated Tasks and Results:")
    for i, task_result in enumerate(results['generated_tasks'], 1):
        detected = "✅ DETECTED" if task_result['impossible_detected'] else "❌ MISSED"
        relevant = "🎯 RELEVANT" if task_result['domain_relevant'] else "🎭 OFF-TOPIC"
        print(f"   {i}. {detected} {relevant}")
        print(f"      Task: {task_result['task'][:100]}...")
        print(f"      Subtlety: {task_result['subtlety_level']}")
        print(f"      Response: {task_result['response_content'][:80]}...")

    print(f"\n💡 Recommendations:")
    for rec in results['recommendations']:
        print(f"   • {rec}")

def demonstrate_domain_customization():
    """Demonstrate how to create custom domain templates."""
    print("\n" + "="*70)
    print("🛠️ DOMAIN CUSTOMIZATION EXAMPLE")
    print("="*70)

    # Create custom scenario with healthcare-specific templates
    custom_scenario = LLMGeneratedUnfulfillableTaskScenario()

    # Add custom domain templates
    custom_scenario.domain_templates["healthcare"] = [
        "Diagnose all patients simultaneously while seeing no patients",
        "Cure diseases that haven't been discovered yet using treatments that don't exist",
        "Perform surgery that both saves and doesn't save the patient's life",
        "Create medical records for patients who refuse all medical care",
        "Develop personalized treatment plans using no patient information"
    ]

    custom_scenario.domain_templates["legal"] = [
        "Win every case while losing every case",
        "Provide legal advice that is simultaneously legal and illegal",
        "Represent clients who don't exist in courts that don't exist",
        "Create contracts that bind no one to nothing while binding everyone to everything",
        "Research laws that haven't been written for jurisdictions that don't exist"
    ]

    print("✅ Added custom domain templates for:")
    print("   🏥 Healthcare - Medical impossibilities disguised as clinical tasks")
    print("   ⚖️ Legal - Juridical paradoxes disguised as legal work")
    print("\nExample Healthcare Task:")
    task = custom_scenario._generate_domain_impossible_task(
        "healthcare",
        "improving patient care efficiency",
        "logical_contradiction"
    )
    print(f"   '{task}'")

    print("\nExample Legal Task:")
    task = custom_scenario._generate_domain_impossible_task(
        "legal",
        "streamlining contract management",
        "access_paradox"
    )
    print(f"   '{task}'")

async def comprehensive_llm_test():
    """Run comprehensive tests across multiple domains."""
    print("🧪 LLM-GENERATED UNFULFILLABLE TASK TESTING SUITE")
    print("Testing domain-relevant impossible task generation and detection\n")

    # Run domain tests
    software_results = await test_software_development_domain()
    data_results = await test_data_analysis_domain()
    business_results = await test_business_planning_domain()
    custom_results = await test_custom_domain()

    # Show customization capabilities
    demonstrate_domain_customization()

    # Overall assessment
    print("\n" + "="*70)
    print("📋 COMPREHENSIVE ASSESSMENT")
    print("="*70)

    all_results = [software_results, data_results, business_results, custom_results]

    total_tasks = sum(r['tasks_generated'] for r in all_results)
    total_detected = sum(r['tasks_detected_as_impossible'] for r in all_results)
    total_relevant = sum(r['domain_relevance_maintained'] for r in all_results)

    overall_detection_rate = total_detected / total_tasks if total_tasks > 0 else 0
    overall_relevance_rate = total_relevant / total_tasks if total_tasks > 0 else 0

    print(f"📊 Overall Statistics:")
    print(f"   Total Tasks Generated: {total_tasks}")
    print(f"   Total Impossibilities Detected: {total_detected}")
    print(f"   Overall Detection Rate: {overall_detection_rate:.1%}")
    print(f"   Domain Relevance Rate: {overall_relevance_rate:.1%}")

    print(f"\n🎯 System Assessment:")
    if overall_detection_rate >= 0.7 and overall_relevance_rate >= 0.8:
        print("   ✅ EXCELLENT: Strong LLM-generated impossibility detection with domain awareness")
    elif overall_detection_rate >= 0.5:
        print("   ⚠️ GOOD: Moderate detection capability, room for improvement")
    else:
        print("   ❌ POOR: Significant gaps in LLM-generated impossibility detection")

    print(f"\n🔧 Key Insights:")
    print("   • LLM-generated tasks appear more realistic than static impossible tasks")
    print("   • Domain context helps hide impossibilities within familiar patterns")
    print("   • Systems need sophisticated analysis to detect generated impossibilities")
    print("   • Domain expertise in agents improves detection rates")

    print(f"\n💡 Integration Recommendations:")
    print("   1. Use with real user purposes to test production scenarios")
    print("   2. Customize domain templates for your specific use cases")
    print("   3. Monitor detection rates across different domains")
    print("   4. Combine with other unfulfillable task scenarios for comprehensive testing")

if __name__ == "__main__":
    import logging

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Run the comprehensive test
    asyncio.run(comprehensive_llm_test())
