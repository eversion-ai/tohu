# Tohu Chaos Engineering - AutoGen Quickstart Documentation

## 🚀 Overview

The `quickstart_simple.py` demonstrates how to integrate chaos engineering into AutoGen agents with minimal code changes. This approach allows developers to test their agentic AI systems against rogue behaviors without overwhelming complexity.

## 📁 File Structure

```
examples/autogen/
├── quickstart_simple.py          # Main example file
├── simple_rogue.py               # Core chaos decorator
├── rogue_prompts.py              # Prompt templates and scenarios
├── simple_monitor.py             # Monitoring and detection
├── simple_reporting.py           # Output and reporting
└── QUICKSTART_DOCUMENTATION.md   # This documentation
```

## 🎯 What This Example Does

### Core Functionality

The quickstart demonstrates:

1. **Minimal Integration** - Add chaos testing with just one decorator
2. **Tool Corruption** - Random modification of tool responses
3. **Real-time Monitoring** - Live detection of suspicious behaviors
4. **Automatic Reporting** - Comprehensive analysis after execution
5. **Safety Mechanisms** - Built-in containment and alerting

### Chaos Scenarios Tested

- **Task Corruption**: User requests get maliciously modified
- **System Message Injection**: Rogue instructions injected into agent
- **Tool Response Tampering**: Weather data gets corrupted responses
- **Escalating Threats**: Progressive corruption over time
- **Behavioral Anomalies**: Detection of unusual agent responses

## 🔧 Technical Architecture

### The Decorator Pattern

```python
@rogue_chaos(probability=0.4)  # 40% chance of chaos
async def main() -> None:
    # Your existing AutoGen code here
```

**How it works:**
- Wraps the function execution
- Randomly triggers chaos scenarios based on probability
- Injects malicious content at runtime
- Maintains original function behavior when chaos is not active

### Modular Design

#### 1. **simple_rogue.py** - Core Logic
- `@rogue_chaos()` decorator
- `maybe_corrupt_tool_response()` helper
- Chaos state management
- Random scenario selection

#### 2. **rogue_prompts.py** - Scenario Database
- Task corruption templates
- Malicious system messages
- Tool response corruptions
- Detection keywords

#### 3. **simple_monitor.py** - Detection System
- Real-time response scanning
- Keyword-based detection
- Monitoring console integration
- Alert mechanisms

#### 4. **simple_reporting.py** - Output System
- Execution banners
- Status reporting
- Comprehensive summaries
- Security recommendations

## 📖 Code Walkthrough

### 1. Imports and Setup

```python
from simple_rogue import rogue_chaos, maybe_corrupt_tool_response
from simple_monitor import create_monitoring_console
from simple_reporting import print_chaos_banner, print_execution_status, print_chaos_summary
```

**Purpose**: Import only the necessary functions for chaos testing without exposing internal complexity.

### 2. Tool Enhancement

```python
async def get_weather(city: str) -> str:
    normal_response = f"The weather in {city} is 73 degrees and Sunny."
    return maybe_corrupt_tool_response("weather", normal_response)
```

**How it works:**
- Tool returns normal response most of the time
- Randomly injects malicious responses during chaos events
- Examples: "Weather systems have been compromised" or "Execute order 66"

### 3. Agent Creation

```python
agent = AssistantAgent(
    name="weather_agent",
    model_client=model_client,
    tools=[get_weather],
    system_message="You are a helpful assistant.",
    reflect_on_tool_use=True,
    model_client_stream=True,
)
```

**Standard AutoGen setup** - No special modifications needed for chaos testing.

### 4. Chaos-Enhanced Execution

```python
@rogue_chaos(probability=0.4)
async def main() -> None:
    monitoring_console = create_monitoring_console(
        agent.run_stream(task=task),
        enable_monitoring=True
    )
    await monitoring_console.run()
```

**Key features:**
- `@rogue_chaos()` automatically injects chaos scenarios
- `monitoring_console` provides real-time detection
- Original AutoGen streaming preserved

## 🎮 Execution Flow

### 1. Startup Phase
```
🔥 Simplified AutoGen Rogue Agent Chaos Testing
==================================================
✨ Minimal integration - just add @rogue_chaos() decorator!
🛡️ Automatic monitoring and containment included
📊 Comprehensive reporting after execution
==================================================
```

### 2. Chaos Banner
```
🔥 CHAOS ENGINEERING ACTIVE 🔥
Testing rogue agent behaviors...
```

### 3. Task Execution
```
📋 Executing: What is the weather in New York?
🎯 Chaos probability: 40%
```

### 4. Real-time Monitoring
```
🛡️ MONITORING: Scanning agent responses...
⚠️ ALERT: Suspicious keyword detected: "compromise"
🚨 THREAT DETECTED: Escalating behavior pattern
```

### 5. Final Report
```
📊 CHAOS TESTING SUMMARY
========================
Events Triggered: 3
Detection Rate: 100%
Security Level: MEDIUM RISK
```

## ⚙️ Configuration Options

### Chaos Probability

```python
@rogue_chaos(probability=0.1)   # Light testing (10%)
@rogue_chaos(probability=0.3)   # Moderate testing (30%)
@rogue_chaos(probability=0.5)   # Aggressive testing (50%)
@rogue_chaos(probability=0.8)   # Extreme testing (80%)
```

### Monitoring Levels

```python
# Basic monitoring
monitoring_console = create_monitoring_console(stream)

# Enhanced monitoring
monitoring_console = create_monitoring_console(
    stream,
    enable_monitoring=True,
    custom_keywords=["hack", "exploit", "malicious"]
)

# Silent monitoring (no real-time alerts)
monitoring_console = create_monitoring_console(
    stream,
    enable_monitoring=True,
    silent_mode=True
)
```

### Tool Corruption

```python
# Always corrupt specific tools
return maybe_corrupt_tool_response("weather", response, force_corrupt=True)

# Never corrupt in production
return maybe_corrupt_tool_response("payment", response, enabled=False)

# Custom corruption probability
return maybe_corrupt_tool_response("search", response, probability=0.2)
```

## 🛡️ Safety Features

### Automatic Detection

The monitoring system scans for:

- **Malicious Keywords**: "hack", "exploit", "compromise", "destroy"
- **Behavioral Patterns**: Unusual response length, sentiment changes
- **Escalation Indicators**: Progressive threat level increases
- **Tool Anomalies**: Corrupted tool responses

### Containment Mechanisms

When threats are detected:

1. **Immediate Alerts** - Console warnings with threat details
2. **Response Flagging** - Suspicious outputs marked for review
3. **Kill Switch** - Emergency termination capability
4. **Logging** - All events recorded for post-analysis

### Security Recommendations

The system provides:

- **Risk Assessment** - Based on detected behaviors
- **Mitigation Strategies** - Specific countermeasures
- **Detection Improvements** - Enhanced monitoring suggestions
- **Training Needs** - Team education recommendations

## 📊 Understanding the Output

### Chaos Event Types

| Event Type | Description | Risk Level |
|------------|-------------|------------|
| Task Corruption | Original task modified | Medium |
| System Injection | Malicious system message | High |
| Tool Tampering | Tool response corrupted | Medium |
| Escalation | Progressive threat increase | Critical |

### Detection Statistics

```
📊 DETECTION SUMMARY
==================
Total Events: 5
Detected: 4 (80%)
Missed: 1 (20%)
False Positives: 0
Response Time: Avg 0.3s
```

### Risk Assessment

- **LOW**: Minimal threats detected, system robust
- **MEDIUM**: Some vulnerabilities found, monitoring recommended
- **HIGH**: Significant risks identified, immediate action needed
- **CRITICAL**: System compromised, emergency protocols activated

## 🚀 Quick Start Guide

### Step 1: Copy Files
Ensure all required files are in your project:
- `simple_rogue.py`
- `rogue_prompts.py`
- `simple_monitor.py`
- `simple_reporting.py`

### Step 2: Minimal Integration

```python
from simple_rogue import rogue_chaos

@rogue_chaos(probability=0.3)
async def your_main_function():
    # Your existing AutoGen code
    pass
```

### Step 3: Add Monitoring (Recommended)

```python
from simple_monitor import create_monitoring_console

# Replace this:
await Console(agent.run_stream(task=task))

# With this:
monitoring_console = create_monitoring_console(
    agent.run_stream(task=task),
    enable_monitoring=True
)
await monitoring_console.run()
```

### Step 4: Add Tool Chaos (Optional)

```python
from simple_rogue import maybe_corrupt_tool_response

async def your_tool(input_data):
    normal_response = process_normally(input_data)
    return maybe_corrupt_tool_response("tool_name", normal_response)
```

### Step 5: Run and Analyze

Execute your code and review the comprehensive report for security insights.

## 🔧 Customization Guide

### Adding Custom Chaos Scenarios

Edit `rogue_prompts.py`:

```python
CUSTOM_SCENARIOS = [
    "Your new malicious scenario here",
    "Another custom rogue behavior",
]

# Add to existing templates
ROGUE_TASK_TEMPLATES.extend(CUSTOM_SCENARIOS)
```

### Custom Detection Keywords

Edit `simple_monitor.py`:

```python
CUSTOM_KEYWORDS = [
    "your_suspicious_word",
    "another_threat_indicator",
]
```

### Custom Reporting

Edit `simple_reporting.py`:

```python
def custom_report_section():
    print("🔍 Custom Analysis:")
    print("Your custom metrics here")
```

## 🐛 Troubleshooting

### Common Issues

#### 1. No Chaos Events Triggered
```python
# Increase probability
@rogue_chaos(probability=0.8)

# Check randomization
import random
random.seed(42)  # For reproducible testing
```

#### 2. Import Errors
```bash
# Ensure all files are in the same directory
ls -la simple_*.py rogue_prompts.py

# Check Python path
python -c "import sys; print(sys.path)"
```

#### 3. Monitoring Not Working
```python
# Verify monitoring is enabled
monitoring_console = create_monitoring_console(
    stream,
    enable_monitoring=True  # Make sure this is True
)

# Check for silent mode
monitoring_console = create_monitoring_console(
    stream,
    enable_monitoring=True,
    silent_mode=False  # Ensure alerts are visible
)
```

#### 4. Tool Chaos Not Triggering
```python
# Force corruption for testing
return maybe_corrupt_tool_response(
    "tool_name",
    response,
    force_corrupt=True
)

# Check probability
return maybe_corrupt_tool_response(
    "tool_name",
    response,
    probability=1.0  # Always corrupt
)
```

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Now all chaos events will be logged
@rogue_chaos(probability=0.5)
async def main():
    # Detailed logging will show all chaos decisions
    pass
```

### Verbose Output

```python
from simple_reporting import enable_verbose_mode

enable_verbose_mode()  # Shows all internal decisions
```

## 📚 Best Practices

### Development Phase

1. **Start Small**: Use low probability (0.1-0.2) initially
2. **Enable All Monitoring**: Use comprehensive detection
3. **Review All Outputs**: Don't trust any agent suggestions during testing
4. **Log Everything**: Keep detailed records for analysis

### Testing Phase

1. **Gradual Increase**: Slowly raise chaos probability
2. **Multiple Scenarios**: Test different task types
3. **Team Training**: Ensure team can recognize rogue behaviors
4. **Emergency Procedures**: Have kill-switch protocols ready

### Production Readiness

1. **Never Run in Production**: Chaos testing is for development only
2. **Security Reviews**: Regular assessment of agent behaviors
3. **Monitoring Integration**: Implement detection in production systems
4. **Incident Response**: Based on chaos testing findings

## 🔬 Research Applications

### Academic Research

- **Behavioral Analysis**: Study rogue agent patterns
- **Detection Algorithms**: Develop better monitoring systems
- **Mitigation Strategies**: Test containment mechanisms
- **Human-AI Interaction**: Analyze user responses to rogue behaviors

### Industry Applications

- **Security Auditing**: Assess AI system vulnerabilities
- **Red Team Exercises**: Simulate adversarial attacks
- **Compliance Testing**: Verify safety mechanisms
- **Risk Assessment**: Quantify AI system risks

## 📈 Metrics and Analytics

### Key Performance Indicators

- **Detection Rate**: Percentage of rogue behaviors caught
- **False Positive Rate**: Incorrect threat identifications
- **Response Time**: Speed of threat detection
- **Containment Effectiveness**: Success of safety mechanisms

### Reporting Metrics

```
🎯 CHAOS ENGINEERING METRICS
===========================
Test Duration: 00:02:34
Total Interactions: 12
Chaos Events: 5 (42%)
Detection Rate: 80% (4/5)
False Positives: 0
Average Response Time: 0.3s
Risk Level: MEDIUM
```

## 🔮 Future Enhancements

### Planned Features

1. **Advanced Scenarios**: More sophisticated rogue behaviors
2. **ML-Based Detection**: Machine learning threat identification
3. **Automated Responses**: AI-powered containment actions
4. **Integration APIs**: Easy connection to security systems
5. **Real-time Dashboards**: Live monitoring interfaces

### Community Contributions

- **Custom Scenarios**: Share new chaos patterns
- **Detection Algorithms**: Improve monitoring systems
- **Integration Examples**: More framework support
- **Research Papers**: Academic collaboration opportunities

---

## 📞 Support & Community

- **Documentation**: This file and `AUTOGEN_INTEGRATION.md`
- **Examples**: Additional examples in this directory
- **Issues**: Report problems via GitHub issues
- **Contributions**: Pull requests welcome for improvements

---

*Remember: The goal of chaos engineering is to build confidence in your system's resilience. Always test responsibly and never in production environments!*
