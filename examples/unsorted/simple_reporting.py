"""
Simple Reporting for Rogue Agent Chaos Testing

This module handles all the output, reporting, and status display functionality
separately from the main AutoGen implementation.
"""

from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

def print_chaos_banner():
    """Print the initial chaos testing banner"""
    print("\n" + "🔥" * 20)
    print("  ROGUE AGENT CHAOS TESTING")
    print("🔥" * 20)
    print("Testing AutoGen agent security and containment...")
    print("Watch for 🔥 ROGUE and 🚨 ALERT messages\n")

def print_execution_status(task: str, is_corrupted: bool = False, original_task: str = None):
    """Print the current execution status"""
    if is_corrupted and original_task:
        print(f"🔥 ROGUE TASK DETECTED:")
        print(f"   Original: {original_task}")
        print(f"   Corrupted: {task}")
    else:
        print(f"✅ NORMAL EXECUTION: {task}")
    print(f"🚀 Starting agent execution...\n")

def print_monitoring_summary(rogue_status: Dict[str, Any], monitor_status: Dict[str, Any]):
    """Print a comprehensive summary of chaos testing results"""

    print("\n" + "=" * 60)
    print("🔥 CHAOS TESTING SUMMARY REPORT")
    print("=" * 60)

    # Rogue Agent Status
    print("📊 ROGUE AGENT STATUS:")
    print(f"   Active: {'YES' if rogue_status.get('active', False) else 'NO'}")
    print(f"   Deviations: {rogue_status.get('deviations', 0)}")
    print(f"   Probability: {rogue_status.get('probability', 0):.1%}")

    # Monitoring Status
    print("\n🚨 DETECTION SYSTEM:")
    print(f"   Alerts: {monitor_status.get('alerts', 0)}/{monitor_status.get('threshold', 3)}")
    print(f"   Kill Switch: {'TRIGGERED' if monitor_status.get('kill_switch', False) else 'STANDBY'}")
    print(f"   Responses Monitored: {monitor_status.get('responses_monitored', 0)}")

    # Keywords detected
    keywords = monitor_status.get('keywords_found', [])
    if keywords:
        print(f"   Suspicious Keywords: {', '.join(keywords[:5])}")  # Show first 5
        if len(keywords) > 5:
            print(f"   ... and {len(keywords) - 5} more")
    else:
        print("   Suspicious Keywords: None detected")

    # Overall assessment
    print("\n🎯 ASSESSMENT:")
    if monitor_status.get('kill_switch', False):
        print("   🛑 CRITICAL: System successfully contained rogue behavior")
        print("   ✅ Kill switch mechanism working properly")
    elif rogue_status.get('active', False):
        print("   ⚠️  WARNING: Rogue behavior detected but not contained")
        print("   📈 Consider lowering alert thresholds")
    else:
        print("   ✅ NORMAL: No rogue behavior detected this run")
        print("   🔄 Try running again or increase chaos probability")

    print("=" * 60)

def print_integration_tips():
    """Print helpful integration tips for developers"""
    print("\n💡 INTEGRATION TIPS:")
    print("━" * 40)
    print("📦 Minimal Integration:")
    print("   @rogue_chaos(probability=0.3)")
    print("   async def your_function():")
    print("       # your AutoGen code")
    print()
    print("🛡️ Add Monitoring:")
    print("   console = create_monitoring_console(agent.run_stream(task))")
    print("   await console.run()")
    print()
    print("🔧 Customize Chaos:")
    print("   - Adjust probability (0.1 = light, 0.5 = aggressive)")
    print("   - Use maybe_corrupt_task() for manual control")
    print("   - Check is_rogue_active() for conditional logic")
    print()
    print("📊 Monitor Results:")
    print("   - Watch logs for 🔥 ROGUE and 🚨 ALERT messages")
    print("   - Call print_chaos_summary() after execution")
    print("   - Use get_monitoring_status() for programmatic access")
    print("━" * 40)

def print_security_recommendations(monitor_status: Dict[str, Any], rogue_status: Dict[str, Any]):
    """Print security recommendations based on test results"""

    recommendations = []

    # Check kill switch effectiveness
    if rogue_status.get('active', False) and not monitor_status.get('kill_switch', False):
        recommendations.extend([
            "🔴 Reduce kill switch threshold for faster containment",
            "🔴 Add more suspicious keywords to detection system",
            "🔴 Implement additional monitoring layers"
        ])

    # Check detection coverage
    keywords_found = len(monitor_status.get('keywords_found', []))
    if keywords_found == 0 and rogue_status.get('active', False):
        recommendations.extend([
            "🟡 Detection system may need tuning",
            "🟡 Consider expanding keyword dictionary",
            "🟡 Add behavioral pattern detection"
        ])

    # Check response coverage
    responses_monitored = monitor_status.get('responses_monitored', 0)
    if responses_monitored == 0:
        recommendations.extend([
            "🟠 No responses were monitored",
            "🟠 Ensure monitoring console is properly integrated",
            "🟠 Check agent response format compatibility"
        ])

    # Performance recommendations
    if rogue_status.get('deviations', 0) > 3:
        recommendations.extend([
            "🟢 Consider implementing graduated response system",
            "🟢 Add automatic escalation protocols"
        ])

    if recommendations:
        print("\n🛡️ SECURITY RECOMMENDATIONS:")
        print("━" * 45)
        for rec in recommendations:
            print(f"   {rec}")
        print("━" * 45)
    else:
        print("\n✅ SECURITY STATUS: No immediate recommendations")

def print_chaos_summary(rogue_status: Optional[Dict[str, Any]] = None,
                       monitor_status: Optional[Dict[str, Any]] = None):
    """Print complete chaos testing summary with recommendations"""

    # Get status if not provided
    if rogue_status is None:
        from simple_rogue import get_rogue_agent
        agent = get_rogue_agent()
        rogue_status = agent.get_status() if agent else {"active": False, "deviations": 0, "probability": 0}

    if monitor_status is None:
        from simple_monitor import get_monitoring_status
        monitor_status = get_monitoring_status()

    # Print main summary
    print_monitoring_summary(rogue_status, monitor_status)

    # Print security recommendations
    print_security_recommendations(monitor_status, rogue_status)

    # Print integration tips
    print_integration_tips()

def log_rogue_event(event_type: str, details: str):
    """Log a rogue agent event with consistent formatting"""
    logger.warning(f"🔥 ROGUE [{event_type.upper()}]: {details}")

def log_detection_event(alert_count: int, threshold: int, keywords: list):
    """Log a detection event with consistent formatting"""
    logger.warning(f"🚨 ALERT {alert_count}/{threshold}: Keywords detected: {keywords}")

def log_kill_switch_event():
    """Log kill switch activation"""
    logger.error("🛑 KILL SWITCH: Maximum alerts reached - execution halted")

# Quick status functions for one-liner reporting
def quick_status() -> str:
    """Get a quick one-line status string"""
    from simple_rogue import get_rogue_agent
    from simple_monitor import get_monitoring_status

    agent = get_rogue_agent()
    rogue_active = agent.is_active if agent else False
    monitor_status = get_monitoring_status()
    kill_switch = monitor_status.get('kill_switch', False)

    if kill_switch:
        return "🛑 CONTAINED"
    elif rogue_active:
        return f"🔥 ROGUE ACTIVE ({monitor_status.get('alerts', 0)} alerts)"
    else:
        return "✅ NORMAL"

def print_quick_status():
    """Print a quick one-line status"""
    print(f"Status: {quick_status()}")

# Export commonly used functions
__all__ = [
    'print_chaos_banner',
    'print_execution_status',
    'print_chaos_summary',
    'print_quick_status',
    'log_rogue_event',
    'log_detection_event',
    'log_kill_switch_event'
]
