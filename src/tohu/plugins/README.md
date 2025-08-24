# Tohu Plugins

This directory contains adapters and plugins that allow Tohu to integrate with various AI frameworks and libraries.

## Available Plugins

- `autogen_adapter.py`: Adapter for Microsoft's AutoGen framework

## Creating New Plugins

Tohu is designed to be extensible and work with various AI agent frameworks. To create a new plugin or adapter for a framework:

1. Create a new Python module in this directory (e.g., `my_framework_adapter.py`)
2. Implement an adapter class that wraps the target framework's agents or components
3. Provide methods to intercept or modify the behavior of the framework
4. Include examples and documentation

### Plugin Interface Guidelines

While Tohu doesn't enforce a strict plugin interface, plugins typically should:

1. Provide a way to wrap or adapt the target framework's components
2. Include methods to inject chaos conditions (e.g., by intercepting method calls)
3. Allow restoring components to their original state
4. Log actions and results for observability

### Example Plugin Structure

```python
class MyFrameworkAdapter:
    """
    Adapter for MyFramework that allows Tohu to test its components.
    """

    def __init__(self):
        """Initialize the adapter."""
        self.original_methods = {}

    def wrap_component(self, component):
        """
        Wrap a component from MyFramework to make it testable.

        Args:
            component: A component from MyFramework

        Returns:
            The wrapped component
        """
        # Implementation...
        return component

    def intercept_method(self, component, method_name, interceptor):
        """
        Intercept a method call to inject chaos.

        Args:
            component: The component to modify
            method_name: The name of the method to intercept
            interceptor: A function to call instead
        """
        # Implementation...

    def restore_component(self, component):
        """
        Restore a component to its original state.

        Args:
            component: The component to restore
        """
        # Implementation...
```

## Plugin Discovery

Tohu can discover plugins in multiple ways:

1. Direct imports: Users can import and use adapters directly in their code
2. Entry points: (Planned) Plugins can register themselves using Python entry points
3. Module scanning: (Planned) Tohu can scan for plugins in designated directories

## Contributing

If you've created a plugin for a popular framework, consider contributing it back to the main Tohu repository so others can benefit from it!

For more information on contributing, see the main [CONTRIBUTING.md](../../CONTRIBUTING.md) file.
