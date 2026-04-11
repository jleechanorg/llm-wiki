---
title: "Documentation Size Monitor Script"
type: source
tags: [bash, monitoring, documentation, performance, api-timeout]
source_file: "raw/monitor_doc_sizes.sh"
sources: []
last_updated: 2026-04-08
---

## Summary
Bash script that monitors documentation file sizes to prevent API timeouts during AI-assisted operations. Checks Cursor rules files and CLAUDE.md against configurable line count thresholds (warning at 1000 lines, failure at 1500 lines).

## Key Claims
- **Threshold-Based Validation**: Fails at 1500 lines (MAX_LINES), warns at 1000 lines (WARNING_LINES)
- **Targeted Documentation Files**: Monitors .cursor/rules/*.mdc files and project CLAUDE.md
- **Exit Code Reporting**: Returns non-zero exit code when files exceed limits for CI/CD integration
- **Synchronized with Tests**: Designed to work alongside test_documentation_performance.py for comprehensive validation

## Key Features
- **Per-File Validation**: Checks each target file individually with pass/fail reporting
- **Human-Readable Output**: Uses emoji indicators (✅, ⚠️, ❌, ⏭️) for status display
- **Error Aggregation**: Tracks failure state and exits with code 1 if any file fails
- **Graceful Missing File Handling**: Skips non-existent files with informational message

## Connections
- [[DocumentationPerformance]] — related testing concept for file size validation
- [[CursorRules]] — the target .mdc files being monitored
- [[APITimeoutPrevention]] — the operational goal this script serves

## Contradictions
- None identified
