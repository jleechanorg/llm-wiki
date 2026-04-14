---
title: "Capture CLI"
type: source
tags: [cli, capture, mock-validation, testing]
sources: []
last_updated: 2026-04-14
---

## Summary

Command-line interface for capture analysis and mock validation. Provides subcommands for analyzing captures, comparing with mock responses, creating baselines, cleanup, and listing capture files. Integrates with capture_analysis module and cleanup functions from capture module.

## Key Claims

- **Five Subcommands**: analyze, compare, baseline, cleanup, list
- **Analyze Command**: Analyzes captures from last N days, generates performance/error reports
- **Compare Command**: Compares capture file with mock responses, shows accuracy score and differences
- **Baseline Command**: Creates mock baseline from capture file using first successful response per service.operation
- **Cleanup Command**: Removes captures older than N days using cleanup_old_captures()
- **List Command**: Shows capture files with size and modification time, sorted newest first
- **Default Capture Dir**: Uses TEST_CAPTURE_DIR env var or tempfile.gettempdir()/test_captures

## Key Quotes

> "Analyze and validate captured service interactions"

> "Export TEST_MODE=capture to enable capture mode during tests"

## Connections

- [[CaptureAnalysis]] — CaptureAnalyzer class for backend analysis
- [[CaptureExample]] — usage examples and demo
- [[APITesting]] — testing CLI tools

## Contradictions

- None identified