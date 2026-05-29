---
title: "Circular Import"
type: concept
tags: [python, imports, architecture]
sources: [stream-event-type]
last_updated: 2026-04-08
---

A Python import cycle where module A imports B and B imports A. 

### Examples in Codebase
1. **StreamEvent**: Extracted into a small "dependency leaf" module to break the cycle between [[StreamingOrchestrator]] and [[LlmService]].
2. **Backend Adjustment Registry**: Refactored in [PR #7112](https://github.com/jleechanorg/worldarchitect.ai/pull/7112) (Bead [[rev-xetuw]]) by extracting all enums, type definitions, and validations into a neutral `backend_adjustment_types.py` module to break a circular dependency between `backend_adjustment_registry.py` and `backend_adjustment_specs.py`.

**Solution Pattern:** Extract the shared dependency into a third module that both original modules import, without either importing the other. Keep the original module as a backward-compatible shim re-exporting the extracted symbols if external callers import from it.

