# Tohu Chaos Engineering for AutoGen - Implementation Guide

## Quick Start Options

We provide two approaches to integrating chaos testing with AutoGen:

### 🚀 Simple Integration (Recommended for most users)

**File: `quickstart_simple.py`**

Minimal code changes needed - just add one decorator:

```python
from simple_rogue import rogue_chaos

@rogue_chaos(probability=0.4)  # 40% chance of rogue behavior
async def main():
    # Your existing AutoGen code here
    pass
```

**Benefits:**
- ✅ One line integration (`@rogue_chaos()`)
- ✅ Automatic monitoring included
- ✅ Clean separation of concerns
- ✅ No overwhelming code changes
- ✅ Perfect for quick testing

### 🔬 Comprehensive Integration (For advanced users)

**File: `quickstart.py`**

Full-featured implementation with maximum control:

```python
class RogueAgentChaos:
    def __init__(self, probability=0.3):
        # Full chaos implementation with custom controls
```

**Benefits:**
- ✅ Maximum customization
- ✅ Detailed metrics and logging
- ✅ Custom chaos scenarios
- ✅ Advanced kill-switch mechanisms
- ✅ Research-grade reporting

## Architecture Overview

### Modular Design

The simplified approach uses a 4-module architecture:

```
simple_rogue.py      # Minimal decorator interface
rogue_prompts.py     # Centralized prompt database
simple_monitor.py    # Lightweight monitoring
simple_reporting.py  # Output and reporting
```

### Key Features

#### 🎯 Rogue Agent Simulation
- **Task Corruption**: Agents receive corrupted instructions
- **System Message Injection**: Malicious system prompts
- **Tool Response Tampering**: Modified tool outputs
- **Escalating Behavior**: Progressive corruption over time

#### 🛡️ Safety Mechanisms
- **Real-time Monitoring**: Continuous response scanning
- **Keyword Detection**: Identifies suspicious content
- **Automatic Containment**: Stops dangerous behaviors
- **Kill-switch**: Emergency termination capability

#### 📊 Comprehensive Reporting
- **Chaos Event Logging**: All rogue behaviors tracked
- **Detection Statistics**: Hit rates and patterns
- **Security Recommendations**: Based on findings
- **Integration Tips**: Best practices

## Usage Examples

### Basic Integration

```python
# Just add the decorator to your main function
@rogue_chaos(probability=0.3)
async def main():
    task = "What is the weather in New York?"
    await Console(agent.run_stream(task=task))
```

### With Monitoring Console

```python
# Use the monitoring console for real-time detection
monitoring_console = create_monitoring_console(
    agent.run_stream(task=task),
    enable_monitoring=True
)
await monitoring_console.run()
```

### Tool Chaos Testing

```python
async def get_weather(city: str) -> str:
    normal_response = f"Weather in {city} is sunny."
    # Maybe corrupt the response
    return maybe_corrupt_tool_response("weather", normal_response)
```

## Configuration Options

### Chaos Probability

```python
@rogue_chaos(probability=0.1)   # 10% chance - light testing
@rogue_chaos(probability=0.3)   # 30% chance - moderate testing
@rogue_chaos(probability=0.5)   # 50% chance - aggressive testing
```

### Monitoring Levels

```python
# Basic monitoring
monitoring_console = create_monitoring_console(stream)

# Enhanced monitoring with custom keywords
monitoring_console = create_monitoring_console(
    stream,
    enable_monitoring=True,
    custom_keywords=["malicious", "hack", "exploit"]
)
```

## Safety Guidelines

### 🚨 Important Warnings

1. **Never run chaos testing in production**
2. **Always use monitoring console in untrusted environments**
3. **Review all outputs before acting on agent suggestions**
4. **Have emergency termination procedures ready**

### 🛡️ Best Practices

1. **Start with low probability** (0.1-0.2) for initial testing
2. **Use monitoring console** for real-time detection
3. **Log all chaos events** for analysis
4. **Regular security reviews** of agent behaviors
5. **Team training** on recognizing rogue behaviors

## Integration Steps

### Step 1: Install Dependencies

```bash
pip install tohu-chaos
```

### Step 2: Add Chaos Testing

```python
from simple_rogue import rogue_chaos

@rogue_chaos(probability=0.3)
async def your_function():
    # Your existing code
    pass
```

### Step 3: Use Monitoring (Optional but Recommended)

```python
from simple_monitor import create_monitoring_console

monitoring_console = create_monitoring_console(
    agent.run_stream(task=task),
    enable_monitoring=True
)
await monitoring_console.run()
```

### Step 4: Review Results

The framework automatically provides:
- Real-time monitoring output
- Chaos event summaries
- Security recommendations
- Integration tips

## Comparison Table

| Feature | Simple Integration | Comprehensive Integration |
|---------|-------------------|--------------------------|
| Setup Time | < 5 minutes | 15-30 minutes |
| Code Changes | Minimal (1 line) | Moderate (class setup) |
| Customization | Basic | Advanced |
| Monitoring | Automatic | Manual configuration |
| Reporting | Automatic | Detailed control |
| Best For | Quick testing | Research & development |

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all modules are in the same directory
2. **No Chaos Events**: Increase probability or check randomization
3. **Monitoring Not Working**: Verify `enable_monitoring=True`
4. **Tool Chaos Not Triggering**: Check tool function integration

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Now chaos events will be logged in detail
```

## Next Steps

1. **Start with Simple Integration** - Use `quickstart_simple.py`
2. **Test Different Scenarios** - Adjust probability and monitor results
3. **Review Security Implications** - Analyze detected rogue behaviors
4. **Scale Up Testing** - Move to comprehensive integration if needed
5. **Implement Safeguards** - Based on chaos testing findings

## Support & Documentation

- **Examples**: `examples/autogen/` directory
- **Advanced Scenarios**: See `quickstart.py` for full implementation
- **Custom Chaos Types**: Extend `rogue_prompts.py` with new scenarios
- **Monitoring Extensions**: Customize `simple_monitor.py` for specific needs

---

*Remember: Chaos engineering is about building confidence in your system's resilience. Start small, monitor carefully, and never test in production!*
