---
title: "Pytest Configuration"
type: source
tags: [pytest, testing, configuration, ci-cd]
source_file: "raw/pytest.ini"
sources: []
last_updated: 2026-04-08
---

## Summary
Pytest configuration defining test discovery patterns, execution options, and parallelization settings for the WorldArchitect.AI testing framework. Enables optimized test runs with cache optimization and multi-worker parallel execution.

## Key Claims
- **Cache Optimization** — `--cache-optimizer` flag enables intelligent test caching to speed up repeated test runs
- **Parallel Execution** — `--num-workers=4` runs tests across 4 worker processes for faster completion
- **Test Discovery** — `test_*.py` file pattern and `test_*` function pattern for standard pytest discovery

## Configuration Details
| Setting | Value | Purpose |
|---------|-------|--------|
| addopts | --cache-optimizer --num-workers=4 | Default pytest flags |
| python_files | test_*.py | Test file naming pattern |
| python_functions | test_* | Test function naming pattern |

## Connections
- [[PytestIntegrationForRealModeTestingFramework]] — part of dual-mode testing infrastructure
- [[RealModeTestingFrameworkMigration]] — uses this configuration for test execution

## Contradictions
- None
