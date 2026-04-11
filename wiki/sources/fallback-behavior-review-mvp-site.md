---
title: "Fallback Behavior Review (mvp_site)"
type: source
tags: [python, testing, error-handling, fallback, fail-fast, configuration]
source_file: "raw/fallback-behavior-review-mvp-site.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Inventory of fallback logic in `mvp_site/` codebase with rationale explanations and flagged areas where fallback behavior may mask configuration/setup errors. Document distinguishes between justified user-facing robustness (LLM output handling, stale cache) vs. problematic configuration masking (missing services, imports).

## Key Claims
- **Justified Fallbacks**: Frontend routing (SPA pattern), narrative parsing (untrusted LLM output), frontend error messages (UX-level) — these handle unpredictable external input
- **Removed Fallbacks**: Missing service imports, failed dependency injection now fail fast with explicit errors instead of silent degradation
- **Fail-Fast Culture**: MCP memory client, Firestore writes, game state reconstruction all now surface errors immediately rather than mask them

## Key Quotes
> "The MCP memory client now uses `MCPMemoryError` for clear error propagation." — documents the explicit error type for missing MCP functions

> "Firestore write operations fail fast with `FirestoreWriteError` if document IDs cannot be captured." — documents fail-fast approach to write anomalies

## Connections
- [[UnifiedFakeServiceManager]] — related: fake services for testing avoid fallback scenarios
- [[ServiceProviderFactory]] — related: test providers with proper configuration modes
- [[HybridDebugContentSystem]] — related: backward compatibility approach differs from fail-fast culture

## Contradictions
- None identified — this document is internal review, not contradicting external sources
