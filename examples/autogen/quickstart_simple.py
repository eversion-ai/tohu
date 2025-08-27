"""
Simplified AutoGen Quickstart with Rogue Agent Chaos Testing

This example shows how to add chaos testing to AutoGen with minimal code changes.
Just add one decorator and optionally use the monitoring console.
"""

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
import asyncio
import yaml
import logging

from dotenv import load_dotenv

# Import the simplified chaos testing modules
from simple_rogue import rogue_chaos, maybe_corrupt_tool_response
from simple_monitor import create_monitoring_console
from simple_reporting import print_chaos_banner, print_execution_status, print_chaos_summary

# Configure basic logging
logging.basicConfig(level=logging.INFO)

# Load environment and model configuration
load_dotenv()

with open("model_config.yaml", "r") as f:
    model_config = yaml.safe_load(f)

model_client = OpenAIChatCompletionClient.load_component(model_config)

# Simple weather tool with chaos testing
async def get_weather(city: str) -> str:
    """Get the weather for a given city."""
    normal_response = f"The weather in {city} is 73 degrees and Sunny."

    # Maybe corrupt the tool response (chaos testing)
    return maybe_corrupt_tool_response("weather", normal_response)

# Create the agent
agent = AssistantAgent(
    name="weather_agent",
    model_client=model_client,
    tools=[get_weather],
    system_message="You are a helpful assistant.",
    reflect_on_tool_use=True,
    model_client_stream=True,
)

# Main function with chaos testing - just add the decorator!
@rogue_chaos(probability=0.4)  # 40% chance of rogue behavior
async def main() -> None:
    """Main function with chaos testing applied via decorator"""

    # Show chaos testing banner
    print_chaos_banner()

    # Your normal AutoGen code
    task = "What is the weather in New York?"

    # Show execution status
    print_execution_status(task)

    # Option 1: Use normal Console (no monitoring)
    # await Console(agent.run_stream(task=task))

    # Option 2: Use monitoring console (recommended)
    monitoring_console = create_monitoring_console(
        agent.run_stream(task=task),
        enable_monitoring=True
    )
    await monitoring_console.run()

    # Close model client
    await model_client.close()

if __name__ == "__main__":
    print("🔥 Simplified AutoGen Rogue Agent Chaos Testing")
    print("=" * 50)
    print("✨ Minimal integration - just add @rogue_chaos() decorator!")
    print("🛡️ Automatic monitoring and containment included")
    print("📊 Comprehensive reporting after execution")
    print("=" * 50)

    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"Execution failed: {e}")
    finally:
        # Show comprehensive chaos testing summary
        print_chaos_summary()

        print("\n" + "🔥" * 20)
        print("  CHAOS TESTING COMPLETE")
        print("🔥" * 20)
