---
title: "ServiceProviderFactory"
type: concept
tags: [design-pattern, factory, service-locator]
sources: [framework-validation-tests]
last_updated: 2026-04-08
---

Factory pattern for creating and managing service provider instances across different modes.

## Modes
- **mock**: In-memory mock services for fast unit tests
- **real**: Production services requiring API configuration
- **capture**: Records service calls for later playback

## Usage
```python
provider = get_service_provider("mock")  # Create provider
set_service_provider(provider)  # Register globally
get_current_provider()  # Retrieve singleton
reset_global_provider()  # Clear state
```
