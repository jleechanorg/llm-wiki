---
title: "Abstract Base Class (ABC)"
type: concept
tags: [python, design-patterns, object-oriented-programming, abstraction, interfaces]
sources: [test-service-provider-abstract-base-class]
last_updated: 2026-04-08
---

## Summary
Python's ABC (Abstract Base Class) module provides a mechanism for defining abstract classes that cannot be instantiated directly. Subclasses must implement all abstract methods defined by the base class.

## Key Characteristics
- **Cannot be instantiated** — an ABC must be subclassed
- **Abstract methods** — @abstractmethod decorator enforces implementation in subclasses
- **Interface enforcement** — ensures contracts between base and derived classes
- **Pythonic alternative** to traditional interfaces (like Java's interfaces)

## Usage Pattern

```python
from abc import ABC, abstractmethod

class MyABC(ABC):
    @abstractmethod
    def my_method(self):
        pass
```

## Connection to Test Service Provider
The TestServiceProvider ABC enforces that any service provider implementation must provide get_firestore(), get_gemini(), get_auth(), and cleanup() methods, ensuring consistent interface across mock and real implementations.

## Related Concepts
- [[Service Provider Pattern]] — runtime service implementation selection
- [[Strategy Pattern]] — interchangeable algorithm implementations
- [[Dependency Injection]] — external service configuration
