---
title: "Startup Import Lazy Loading Tests"
type: source
tags: [tdd, unit-testing, python, import, lazy-loading, performance]
source_file: "raw/startup-import-lazy-loading-tests.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Regression tests validating that lazy-loading refactors keep heavy cloud-backed modules out of the startup path. Tests verify `google.genai` and `google.cloud.firestore` are not loaded when importing `mvp_site.streaming_orchestrator` or `mvp_site.main`.

## Key Claims
- **Lazy Proxies Registered**: Lazy modules are registered in `sys.modules` immediately via LazyLoader, but their bodies (which pull heavy dependencies) must not execute until first attribute access
- **Heavy Transitive Deps Deferred**: `google.genai` and `google.cloud.firestore` must NOT be loaded at import time — this is the critical cold-start check
- **Module Bodies Not Executed**: Bodies of `firestore_service`, `gemini_provider`, and `llm_service` are deferred despite being imported transitively
- **main.py Deferral Verified**: `mvp_site.main` import keeps all cloud-backed modules out of the startup path

## Test Functions
- `test_streaming_orchestrator_import_keeps_heavy_modules_lazy` — validates streaming_orchestrator import doesn't execute heavy module bodies
- `test_streaming_orchestrator_llm_service_body_deferred` — proves llm_service body hasn't executed (google.genai absent)
- `test_main_import_defers_cloud_backed_modules` — critical check that google.genai is not loaded on main import

## Key Technical Details
- `_is_lazy_proxy()` checks if a module is a LazyLoader proxy by verifying `__spec__.loader` is a LazyLoader instance
- `_clear_modules()` / `_restore_modules()` utilities for clean module state isolation between tests
- Tests use module snapshotting to ensure clean import environment

## Connections
- Related to [[ColdStartOptimization]] — reducing startup latency by deferring heavy imports
- Implements [[LazyLoading]] pattern for Python modules
- Tests verify [[ImportPerformance]] requirements
