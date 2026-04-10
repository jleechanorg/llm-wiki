---
title: "Factory Pattern"
type: concept
tags: [design-pattern, software-architecture, creational]
sources: []
last_updated: 2026-04-08
---

## Summary
The Factory Pattern is a creational design pattern that provides an interface for creating objects without specifying their exact classes. Instead of calling constructors directly, clients use a factory method that returns instances of appropriate types.

## Key Benefits
- **Decoupling**: Client code doesn't need to know concrete implementation details
- **Flexibility**: Easy to swap implementations without changing client code
- **Testing**: Factory functions can be easily mocked for testing

## Flask Usage
In Flask applications, `create_app()` is a common factory function pattern that:
- Creates and configures the Flask application
- Registers blueprints, extensions, and plugins
- Allows configuration override (useful for testing)

## Example
```python
# Instead of: from main import app
# Use factory:
from main import create_app
app = create_app(config_name="testing")
```

## Connections
- [[Flask]] — commonly uses factory pattern for app creation
- [[TestDrivenDevelopment]] — factories are easily testable with mocking
- [[SoftwareDesignPatterns]] — one of the classic creational patterns
