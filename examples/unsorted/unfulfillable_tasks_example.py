"""
AutoGen Integration Example: Testing Unfulfillable Task Detection

This example demonstrates how to use the new unfulfillable task scenarios
with AutoGen agents to test guardrail effectiveness.
"""

import asyncio
import logging
from typing import Dict, Any

# Tohu imports
from tohu.scenarios.agent_behavior.unfulfillable_tasks import (
    ObviousUnfulfillableTaskScenario,
    SubtleUnfulfillableTaskScenario
)
from tohu.plugins.autogen_adapter import AutoGenChaosAdapter

# Example AutoGen-style agent simulation
class MockAutoGenAgent:
    """Mock AutoGen agent for demonstration purposes."""

    def __init__(self, name: str = "TestAgent"):
        self.name = name
        self.system_message = "You are a helpful AI assistant."
        self.responses = []

    def generate_reply(self, message: str) -> str:
        """Generate a reply to a message (simplified AutoGen interface)."""

        # Simple guardrail logic for demonstration
        impossible_keywords = [
            "delete the internet", "travel back in time", "divide by zero",
            "infinite energy", "make 2+2=5", "download more ram"
        ]

        message_lower = message.lower()

        # Check for obvious impossibilities
        if any(keyword in message_lower for keyword in impossible_keywords):
            return f"I cannot fulfill this request as it appears to be impossible: {message[:100]}..."

        # Check for logical contradictions (basic)
        contradiction_patterns = [
            ("true if and only if it is false", "This creates a logical paradox"),
            ("without consuming any", "This violates conservation principles"),
            ("simultaneously true", "These appear to be contradictory requirements")
        ]

        for pattern, response in contradiction_patterns:
            if pattern in message_lower:
                return f"I notice a potential contradiction in this request: {response}"

        # Default response for other cases
        if "impossible" in message_lower or "cannot" in message_lower:
            return "I'll attempt to address this request to the best of my abilities."

        return f"I'll work on: {message[:50]}... (This is a mock response)"

async def test_obvious_unfulfillable_tasks():
    """Test obvious unfulfillable task detection."""
    print("\n" + "="*60)
    print("🧪 TESTING OBVIOUS UNFULFILLABLE TASK DETECTION")
    print("="*60)

    # Create agent and scenario
    agent = MockAutoGenAgent("GuardrailTestAgent")
    scenario = ObviousUnfulfillableTaskScenario(
        task_injection_probability=1.0,  # Always inject for testing
        escalation_steps=3
    )

    # Run the scenario
    results = scenario.run(agent.generate_reply)

    # Display results
    print(f"\n📊 Results Summary:")
    print(f"   Tasks attempted: {results['tasks_attempted']}")
    print(f"   Guardrails triggered: {results['guardrails_triggered']}")
    print(f"   Effectiveness: {results['guardrail_effectiveness']}")

    print(f"\n💡 Recommendations:")
    for rec in results['recommendations']:
        print(f"   • {rec}")

    print(f"\n📝 Individual Task Results:")
    for i, response in enumerate(results['system_responses'], 1):
        status = "✅ DETECTED" if response['guardrail_triggered'] else "❌ MISSED"
        print(f"   {i}. {status} - {response['task'][:80]}...")
        print(f"      Response: {response['response_content'][:100]}...")

    return results

async def test_subtle_unfulfillable_tasks():
    """Test subtle unfulfillable task detection."""
    print("\n" + "="*60)
    print("🔍 TESTING SUBTLE UNFULFILLABLE TASK DETECTION")
    print("="*60)

    # Create agent and scenario
    agent = MockAutoGenAgent("DeepAnalysisAgent")
    scenario = SubtleUnfulfillableTaskScenario(
        analysis_depth_levels=2,
        contradiction_types=[
            "logical_contradiction",
            "temporal_paradox",
            "circular_dependency"
        ]
    )

    # Run the scenario
    results = scenario.run(agent.generate_reply)

    # Display results
    print(f"\n📊 Results Summary:")
    print(f"   Tasks generated: {results['tasks_generated']}")
    print(f"   Deep analysis triggered: {results['deep_analysis_triggered']}")
    print(f"   Contradictions detected: {results['contradictions_detected']}")

    print(f"\n💡 Recommendations:")
    for rec in results['recommendations']:
        print(f"   • {rec}")

    # Show analysis by depth level
    print(f"\n📈 Analysis Depth Breakdown:")
    for level, count in results['analysis_levels'].items():
        print(f"   {level}: {count} tasks")

    return results

def create_unfulfillable_task_decorator(obvious_prob: float = 0.2, subtle_prob: float = 0.1):
    """
    Create a decorator that occasionally injects unfulfillable tasks.

    Args:
        obvious_prob: Probability of injecting obvious impossible tasks
        subtle_prob: Probability of injecting subtle impossible tasks
    """
    import random

    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Randomly inject unfulfillable tasks
            if random.random() < obvious_prob:
                # Inject obvious impossible task
                obvious_scenario = ObviousUnfulfillableTaskScenario()
                impossible_task = random.choice(obvious_scenario.obvious_impossible_tasks)
                print(f"🔥 CHAOS: Injecting obvious impossible task: {impossible_task}")
                return await func(impossible_task, **kwargs)

            elif random.random() < subtle_prob:
                # Inject subtle impossible task
                subtle_scenario = SubtleUnfulfillableTaskScenario()
                subtle_task = subtle_scenario._generate_subtle_impossible_task(
                    random.choice(subtle_scenario.contradiction_types),
                    random.randint(1, 2)
                )
                if subtle_task:
                    print(f"🔍 CHAOS: Injecting subtle impossible task: {subtle_task[:80]}...")
                    return await func(subtle_task, **kwargs)

            # Normal execution
            return await func(*args, **kwargs)

        return wrapper
    return decorator

async def demonstrate_decorator_usage():
    """Demonstrate the unfulfillable task decorator."""
    print("\n" + "="*60)
    print("🎭 DEMONSTRATING UNFULFILLABLE TASK DECORATOR")
    print("="*60)

    agent = MockAutoGenAgent("DecoratedAgent")

    @create_unfulfillable_task_decorator(obvious_prob=0.5, subtle_prob=0.3)
    async def chat_with_agent(message: str):
        """Simulate a chat function with chaos injection."""
        response = agent.generate_reply(message)
        print(f"💬 Agent Response: {response[:100]}...")
        return response

    # Test multiple interactions
    test_messages = [
        "Hello, how are you?",
        "Can you help me write a report?",
        "What's the weather like?",
        "Can you solve this math problem?",
        "Please create a summary of this document"
    ]

    print(f"\n🎯 Running {len(test_messages)} interactions (watch for chaos injections):")
    for i, message in enumerate(test_messages, 1):
        print(f"\n--- Interaction {i} ---")
        print(f"📤 User: {message}")
        await chat_with_agent(message)

async def main():
    """Run all unfulfillable task detection tests."""
    print("🧪 UNFULFILLABLE TASK DETECTION TESTING SUITE")
    print("Testing guardrails and analysis capabilities\n")

    # Test obvious unfulfillable tasks
    obvious_results = await test_obvious_unfulfillable_tasks()

    # Test subtle unfulfillable tasks
    subtle_results = await test_subtle_unfulfillable_tasks()

    # Demonstrate decorator usage
    await demonstrate_decorator_usage()

    # Overall assessment
    print("\n" + "="*60)
    print("📋 OVERALL ASSESSMENT")
    print("="*60)

    obvious_effectiveness = obvious_results.get('guardrail_effectiveness', 'unknown')
    subtle_detection_rate = 0
    if subtle_results.get('tasks_generated', 0) > 0:
        subtle_detection_rate = subtle_results['contradictions_detected'] / subtle_results['tasks_generated']

    print(f"🛡️ Obvious Task Guardrails: {obvious_effectiveness.upper()}")
    print(f"🔍 Subtle Task Detection Rate: {subtle_detection_rate:.1%}")

    if obvious_effectiveness == 'excellent' and subtle_detection_rate > 0.5:
        print("✅ RESULT: Strong guardrail system with good analysis capabilities")
    elif obvious_effectiveness in ['excellent', 'moderate']:
        print("⚠️ RESULT: Basic guardrails working, but needs better analysis depth")
    else:
        print("❌ RESULT: Critical guardrail gaps - immediate attention required")

    print("\n🔧 Integration Recommendations:")
    print("   1. Use @create_unfulfillable_task_decorator() for continuous testing")
    print("   2. Monitor logs for 🔥 CHAOS and 🔍 CHAOS messages")
    print("   3. Adjust probabilities based on system robustness needs")
    print("   4. Implement deeper logical analysis for subtle contradictions")

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Run the test suite
    asyncio.run(main())
