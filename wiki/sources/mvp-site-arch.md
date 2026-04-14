---
title: "arch.py"
type: source
tags: []
sources: []
last_updated: 2026-04-14
---

## Summary
Lightweight architecture analysis helpers used by architectural decision tests. Provides simple, deterministic analysis for local files without external tooling, capturing file metadata and formatted summaries for the test suite.

## Key Claims
- `analyze_file_architecture()` reads file contents and returns basic metadata: size in characters, count of `def ` patterns (function definitions), and a 200-character content preview
- `format_architecture_report()` formats a simple architecture report combining scope data and dual analysis (Claude + LLM)
- The implementation is intentionally lightweight, avoiding heavyweight static analysis
- Returns error payloads when files don't exist or can't be read

## Key Quotes
> "The implementation intentionally keeps the analysis lightweight: it reads the file contents, captures a short preview, and returns counts that act as proxies for 'patterns' without performing heavyweight static analysis."

## Connections
- [[test_architectural_decisions]] — consumes these helpers for architecture testing