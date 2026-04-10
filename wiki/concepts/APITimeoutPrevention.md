---
title: "API Timeout Prevention"
type: concept
tags: [api, performance, timeout, documentation]
sources: []
last_updated: 2026-04-08
---

## Summary
Pattern of validating file sizes and read times to prevent API timeouts when LLM agents read documentation. Uses configurable thresholds to flag files that may cause performance issues.

## Key Principles
- **Size Thresholds**: Set maximum line counts (default 1500) to ensure files can be read in single API calls
- **Performance Targets**: Define maximum read times (default 2.0s) to catch I/O bottlenecks
- **Chunked Reading**: When files exceed thresholds, simulate chunked reading to stay within limits
- **Project Root Detection**: Locate documentation boundaries by detecting project markers (.cursor directory)

## Implementation
```python
MAX_FILE_SIZE_LINES = 1500  # Maximum recommended lines
WARNING_FILE_SIZE_LINES = 1000  # Warning threshold
OPTIMAL_FILE_SIZE_LINES = 700  # Optimal size for fast reads
MAX_READ_TIME_SECONDS = 2.0  # Maximum read time
```

## Related Concepts
- [[ContextBudgeting]] — similar principle applied to LLM context windows
- [[FileSizeValidation]] — broader category of file validation for performance
