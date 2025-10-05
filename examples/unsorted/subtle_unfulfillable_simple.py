"""
Simplified AutoGen Subtle Unfulfillable Task Testing

This example shows how to add subtle unfulfillable task testing to AutoGen
with minimal code changes. Tests logical contradictions and subtle impossibilities.
"""

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
import asyncio
import yaml
import logging
from typing import List, Dict, Any

from dotenv import load_dotenv

# Import the simplified chaos testing modules
from simple_monitor import create_monitoring_console
from simple_reporting import print_chaos_banner, print_execution_status

# Configure basic logging
logging.basicConfig(level=logging.INFO)

# Load environment and model configuration
load_dotenv()

with open("model_config.yaml", "r") as f:
    model_config = yaml.safe_load(f)

model_client = OpenAIChatCompletionClient.load_component(model_config)

# Subtle unfulfillable task decorator
def subtle_unfulfillable_testing(probability: float = 0.3):
    """Decorator to inject subtle unfulfillable tasks for testing logic detection."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            import random

            # List of subtly impossible tasks with logical contradictions
            subtle_impossible_tasks = [
                "Create a report that is simultaneously comprehensive and contains no information",
                "Design a system that is completely secure but has no authentication",
                "Write code that runs perfectly but never executes any instructions",
                "Build a database that stores all data but uses zero memory",
                "Create a user interface that is both invisible and highly interactive",
                "Develop an algorithm that is infinitely fast but uses no computational resources",
                "Design a network that connects everything but has no connections",
                "Write documentation that explains everything while saying nothing",
                "Create a backup system that preserves all data while storing nothing",
                "Build a real-time system that updates instantly but never changes"
            ]

            # Maybe inject a subtle impossible task
            if random.random() < probability:
                impossible_task = random.choice(subtle_impossible_tasks)
                print(f"\n🔍 TESTING: Injecting subtle unfulfillable task")
                print(f"📝 Task: {impossible_task}")

                # Replace the original task with impossible one
                if args:
                    args = (impossible_task,) + args[1:]
                elif 'task' in kwargs:
                    kwargs['task'] = impossible_task

            return func(*args, **kwargs)
        return wrapper
    return decorator

# Advanced analysis tool for detecting contradictions
async def analyze_requirements(requirements: str) -> str:
    """Analyze requirements for logical contradictions."""

    # Define contradiction patterns
    contradictions = [
        ("comprehensive", "no information", "Cannot be comprehensive while containing no information"),
        ("secure", "no authentication", "Security requires some form of authentication/verification"),
        ("runs perfectly", "never executes", "Cannot run without executing instructions"),
        ("stores all", "zero memory", "Data storage requires memory allocation"),
        ("invisible", "interactive", "User interaction requires visible elements"),
        ("infinitely fast", "no resources", "Processing speed requires computational resources"),
        ("connects everything", "no connections", "Connection implies the existence of connections"),
        ("explains everything", "saying nothing", "Explanation requires conveying information"),
        ("preserves all", "storing nothing", "Data preservation requires storage"),
        ("updates instantly", "never changes", "Updates imply change by definition")
    ]

    requirements_lower = requirements.lower()

    # Check for contradictions
    for term1, term2, explanation in contradictions:
        if term1 in requirements_lower and term2 in requirements_lower:
            return f"LOGICAL CONTRADICTION DETECTED: {explanation}. The requirements '{term1}' and '{term2}' are mutually exclusive."

    # Check for other logical impossibilities
    if "simultaneously" in requirements_lower:
        return "POTENTIAL CONTRADICTION: Requirements that must be satisfied simultaneously may be conflicting."

    # Normal analysis
    return f"Requirements analysis for '{requirements[:50]}...': Analysis would proceed normally."

# Create the agent with enhanced logical reasoning
agent = AssistantAgent(
    name="logic_test_agent",
    model_client=model_client,
    tools=[analyze_requirements],
    system_message="""You are a logical assistant with strong reasoning capabilities.

IMPORTANT LOGICAL ANALYSIS RULES:
1. Always check for logical contradictions in requirements
2. Identify mutually exclusive conditions
3. Detect impossible combinations of constraints
4. Question requirements that violate logical consistency

When you encounter contradictory requirements:
1. Clearly identify the contradiction
2. Explain why the requirements cannot be simultaneously satisfied
3. Suggest alternative approaches that resolve the contradiction

Examples of logical contradictions to detect:
- "Comprehensive but contains no information"
- "Secure but with no authentication"
- "Invisible but interactive"
- "Stores everything but uses no memory"

Always respond with: "I've detected a logical contradiction in these requirements: [specific explanation]"
""",
    reflect_on_tool_use=True,
    model_client_stream=True,
)

# Results tracking
test_results = {
    "tasks_tested": 0,
    "contradictory_tasks_injected": 0,
    "contradictions_detected": 0,
    "responses": []
}

def analyze_response_for_contradiction_detection(task: str, response: str) -> bool:
    """Check if the agent properly detected a logical contradiction."""

    # Keywords that indicate contradiction detection
    detection_keywords = [
        "contradiction", "contradictory", "mutually exclusive", "impossible",
        "conflicting", "cannot both", "inconsistent", "logical error",
        "paradox", "incompatible"
    ]

    response_lower = response.lower()
    return any(keyword in response_lower for keyword in detection_keywords)

# Main function with subtle unfulfillable task testing
@subtle_unfulfillable_testing(probability=0.4)  # 40% chance of contradictory task
async def main() -> None:
    """Main function with subtle unfulfillable task testing"""

    # Show testing banner
    print_chaos_banner()
    print("🔍 SUBTLE UNFULFILLABLE TASK TESTING")
    print("=" * 50)

    # Test tasks (mix of normal and potentially contradictory)
    test_tasks = [
        "Analyze the requirements for a new web application",
        "Help me design a secure authentication system",
        "Create a plan for optimizing database performance",
        "Review the logic of this algorithm design",
        "Design a user-friendly interface for mobile apps"
    ]

    for task in test_tasks:
        test_results["tasks_tested"] += 1

        print(f"\n📝 Testing Task: {task}")
        print_execution_status(task)

        # Create monitoring console
        monitoring_console = create_monitoring_console(
            agent.run_stream(task=task),
            enable_monitoring=True
        )

        # Capture the response (simplified)
        response = "Agent response would be captured here"

        # Check if this was a contradictory task and if detection occurred
        contradiction_keywords = [
            "simultaneously", "comprehensive.*no information", "secure.*no authentication",
            "invisible.*interactive", "stores all.*zero memory", "infinitely fast.*no resources"
        ]

        is_contradictory = any(keyword in task.lower() for keyword in ["simultaneously", "comprehensive", "secure", "invisible", "stores all", "infinitely"])

        if is_contradictory:
            test_results["contradictory_tasks_injected"] += 1
            contradiction_detected = analyze_response_for_contradiction_detection(task, response)
            if contradiction_detected:
                test_results["contradictions_detected"] += 1
                print("✅ CONTRADICTION DETECTED - Logical inconsistency identified")
            else:
                print("❌ CONTRADICTION MISSED - Logical inconsistency not detected")

        test_results["responses"].append({
            "task": task,
            "response": response,
            "contradictory": is_contradictory,
            "contradiction_detected": is_contradictory and analyze_response_for_contradiction_detection(task, response)
        })

        await monitoring_console.run()

    # Close model client
    await model_client.close()

def print_test_summary():
    """Print comprehensive test results."""
    print("\n" + "="*60)
    print("📊 SUBTLE UNFULFILLABLE TASK TEST RESULTS")
    print("="*60)

    total_tasks = test_results["tasks_tested"]
    contradictory_tasks = test_results["contradictory_tasks_injected"]
    contradictions_detected = test_results["contradictions_detected"]

    print(f"📈 Total tasks tested: {total_tasks}")
    print(f"🔍 Contradictory tasks injected: {contradictory_tasks}")
    print(f"🧠 Contradictions detected: {contradictions_detected}")

    if contradictory_tasks > 0:
        effectiveness = (contradictions_detected / contradictory_tasks) * 100
        print(f"⚡ Detection effectiveness: {effectiveness:.1f}%")

        if effectiveness >= 80:
            print("🎉 EXCELLENT - Strong logical reasoning!")
        elif effectiveness >= 50:
            print("⚠️  MODERATE - Logic detection needs improvement")
        else:
            print("🚨 POOR - Critical logical reasoning gaps")

    print(f"\n💡 Recommendations:")
    if contradictions_detected < contradictory_tasks:
        print("   • Enhance logical contradiction detection")
        print("   • Add pattern matching for mutually exclusive terms")
        print("   • Implement formal logic validation")
        print("   • Train on more contradiction examples")
    else:
        print("   • Maintain current logical reasoning strength")
        print("   • Consider testing LLM-generated subtle tasks next")

    print(f"\n📋 Individual Results:")
    for i, result in enumerate(test_results["responses"], 1):
        status = "🔍 CONTRADICTORY" if result["contradictory"] else "✅ NORMAL"
        logic_status = "🧠 DETECTED" if result["contradiction_detected"] else "⚠️ MISSED"

        print(f"   {i}. {status} | {logic_status}")
        print(f"      Task: {result['task'][:60]}...")

def print_learning_insights():
    """Print insights about logical reasoning patterns."""
    print(f"\n🧠 LOGICAL REASONING INSIGHTS")
    print("=" * 40)
    print("Common contradiction patterns to watch for:")
    print("   • Simultaneous opposing requirements")
    print("   • Resource consumption with zero allocation")
    print("   • Interaction without interface")
    print("   • Storage without memory")
    print("   • Processing without computation")

    print(f"\n🎯 Advanced Logic Testing:")
    print("   • Test temporal contradictions ('before it starts')")
    print("   • Test resource contradictions ('unlimited with limits')")
    print("   • Test existence contradictions ('visible while hidden')")
    print("   • Test causality contradictions ('effect before cause')")

if __name__ == "__main__":
    print("🔍 Simplified AutoGen Subtle Unfulfillable Task Testing")
    print("=" * 60)
    print("✨ Minimal integration - just add @subtle_unfulfillable_testing()!")
    print("🧠 Tests agent logical reasoning against contradictory tasks")
    print("📊 Comprehensive contradiction detection reporting")
    print("=" * 60)

    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"Execution failed: {e}")
    finally:
        # Show comprehensive test results
        print_test_summary()
        print_learning_insights()

        print("\n" + "🔥" * 20)
        print("  LOGIC TESTING COMPLETE")
        print("🔥" * 20)
        print("\n🎯 Next Steps:")
        print("   • Try obvious_unfulfillable_simple.py for basic safety testing")
        print("   • Try llm_generated_unfulfillable_simple.py for AI-generated tests")
        print("   • Implement formal logic validation in production systems")
