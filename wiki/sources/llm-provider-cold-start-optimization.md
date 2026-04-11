---
title: "LLM Provider Module — Cold-Start Optimization"
type: source
tags: [llm-providers, python, cold-start-optimization, lazy-loading, performance]
source_file: "raw/llm-provider-cold-start-optimization.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module implementing lazy loading for LLM provider submodules (cerebras, gemini, openclaw, openrouter). Uses `__getattr__` for cold-start optimization, deferring expensive imports like google.genai (~840ms) until first access. Re-exports ContextTooLargeError and check_context_too_large for backward compatibility.

## Key Claims
- **Cold-Start Optimization**: Provider submodules NOT eagerly imported; load on first attribute access via `__getattr__`
- **Lazy Loading Pattern**: `importlib.import_module()` defers ~840ms google.genai import until needed
- **Backward Compatibility**: Re-exports ContextTooLargeError and check_context_too_large for existing code
- **Supported Providers**: cerebras_provider, gemini_provider, openclaw_provider, openrouter_provider, provider_utils

## Technical Details
```python
def __getattr__(name: str):
    if name in (...):
        module = importlib.import_module(f"mvp_site.llm_providers.{name}")
        globals()[name] = module  # Cache after first access
        return module
    raise AttributeError(...)
```

## Connections
- [[ContextTooLargeError]] — exception re-exported for backward compat
- [[ProviderUtils]] — utility module for providercommon functionality

## Contradictions
- None identified
