---
title: "Documentation File Size and Performance Tests"
type: source
tags: [python, testing, documentation, performance, api-timeout]
source_file: "raw/test_documentation_performance.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test script that validates documentation files are within acceptable size limits to prevent API timeouts. Checks .cursor/rules/ directory files and CLAUDE.md against configurable thresholds.

## Key Claims
- **Size Thresholds**: Defines MAX_FILE_SIZE_LINES (1500), WARNING_FILE_SIZE_LINES (1000), OPTIMAL_FILE_SIZE_LINES (700)
- **Performance Target**: MAX_READ_TIME_SECONDS of 2.0 for file reading
- **Project Root Detection**: Automatically locates project root by searching for .cursor directory
- **Chunked Reading**: Simulates API-style chunked reading with configurable chunk_lines (default 2000)

## Key Test Functions
- `check_file_size()`: Validates line count and character count against thresholds
- `test_file_sizes()`: Pytest test ensuring no file exceeds MAX_FILE_SIZE_LINES
- `check_read_performance()`: Measures actual file read time
- `test_read_performance()`: Pytest test ensuring read time <= MAX_READ_TIME_SECONDS
- `simulate_api_read()`: Simulates chunked API reading

## Files Checked
- .cursor/rules/rules.mdc
- .cursor/rules/lessons.mdc
- .cursor/rules/project_overview.md
- .cursor/rules/planning_protocols.md
- .cursor/rules/documentation_map.md
- .cursor/rules/quick_reference.md
- .cursor/rules/progress_tracking.md
- CLAUDE.md

## Connections
- [[CursorRules]] — the .cursor/rules/ directory this test validates
- [[ClaudeSettings]] — CLAUDE.md file validation
