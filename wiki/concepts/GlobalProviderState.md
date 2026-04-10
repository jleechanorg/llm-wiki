---
title: "Global Provider State"
type: concept
tags: [python, state-management, testing]
sources: ["service-provider-factory"]
last_updated: 2026-04-08
---

Module-level global state pattern using _current_provider variable to track the active service provider across test runs. Functions set_service_provider(), get_current_provider(), and reset_global_provider() provide controlled access to this singleton state.

## Related Concepts
- [[ServiceProviderFactory]] — maintains global state
- [[TestServiceProvider]] — interface for provider instances
