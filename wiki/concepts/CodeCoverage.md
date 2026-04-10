---
title: "Code Coverage"
type: concept
tags: [testing, quality-metrics, python]
sources: [worldarchitect-ai-code-coverage-report-mvp-site]
last_updated: 2026-04-08
---

Software testing metric measuring the percentage of code statements executed during automated tests. Coverage tools track which lines, branches, functions, or paths are exercised by test suites. In the mvp_site coverage report, all 56 Python files showed 0% coverage, indicating no tests were executed against the codebase at capture time.

## Coverage Types
- **Statement coverage**: Which statements are executed
- **Branch coverage**: Which conditional paths are taken
- **Function coverage**: Which functions are called
- **Path coverage**: Which execution paths are traversed

## Related
- [[TestingFramework]] — testing infrastructure present but not integrated
- [[Pytest]] — test runner not executing against mvp_site
