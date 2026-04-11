---
title: "Firebase Mock Mode Initialization Tests"
type: source
tags: [python, testing, firebase, mock-mode, initialization, warmup]
source_file: "raw/test_firebase_mock_mode.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Tests that Firebase initialization is properly skipped when MOCK_SERVICES_MODE environment variable is set. Verifies both main.py and world_logic.py correctly check for mock mode to avoid unnecessary Firestore connections at startup.

## Key Claims
- **Mock Mode Skips Warmup**: When MOCK_SERVICES_MODE=true, create_app() does not invoke _warm_startup_lazy_dependencies()
- **Explicit Flag Works**: DISABLE_STARTUP_WARMUP env var independently controls warmup behavior
- **Non-Blocking Warmup**: Warmup path must not synchronously block on Firestore query latency (>0.25s threshold)
- **Thread Safety**: Warmup threads complete before test teardown

## Key Quotes
> "Warmup path must not block startup on Firestore query latency."

> "Mock mode should skip startup lazy warmup side effects."

## Connections
- Related to [[Fake Services Unit Tests]] — both test mock service behavior
- Uses [[Firestore Service]] for database operations
- Controlled via [[Environment Variable Configuration]] pattern

## Contradictions
- None identified
