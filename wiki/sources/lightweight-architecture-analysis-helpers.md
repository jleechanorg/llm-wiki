---
title: "Lightweight Architecture Analysis Helpers"
type: source
tags: [testing, architecture, analysis, static-analysis, test-infrastructure]
source_file: "raw/lightweight-architecture-analysis-helpers.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Lightweight architecture analysis helpers used by architectural decision tests. Provides simple, deterministic analysis for local files without relying on external tooling. Surfaces key metadata and formatted summaries expected by the test suite.

## Key Claims
- **Lightweight Design**: Intentionally keeps analysis lightweight without heavyweight static analysis
- **File Analysis**: Reads file contents, captures short preview, and returns counts as proxies for "patterns"
- **Dual Analysis Support**: Provides formatting for both Claude and LLM analysis outputs
- **Error Handling**: Returns error payloads when files don't exist or can't be read

## Key Code Components
- `analyze_file_architecture(filepath)`: Returns dict with size_chars, fake_patterns, fake_details, content_preview
- `format_architecture_report(scope_data, dual_analysis)`: Formats architecture report string

## Connections
- [[Test Infrastructure]] — used by architectural decision tests
- [[Static Analysis]] — contrasts with heavyweight approaches

## Contradictions
- None identified
