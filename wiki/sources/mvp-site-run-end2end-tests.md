---
title: "Run End2end Tests"
type: source
tags: [testing, e2e, integration, test-runner]
sources: [mvp-site-run-end2end-tests]
last_updated: 2025-01-15
---

## Summary

End-to-end test runner for the Real-Mode Testing Framework. Executes e2e integration tests with real Firestore, Gemini, and MCP services using pytest.

## Key Claims

- **E2E runner**: Runs integration tests in real mode with actual services
- **Test filtering**: Supports unit, integration, expensive, mock_only, real_only markers
- **Real service usage**: Uses RealServiceProvider for Firestore and Gemini APIs
- **CLI arguments**: --campaign-limit, --no-cleanup for flexible test execution
- **Test isolation**: Tracks and cleans up test collections after runs

## Usage

```bash
python run_end2end_tests.py [--campaign-limit N] [--no-cleanup] [pytest_args...]
```

## Markers Supported

| Marker | Behavior |
|--------|----------|
| unit | Skip in e2e runs |
| integration | Include in e2e runs |
| expensive | Filter if EXPENSIVE_TESTS=false |
| mock_only | Skip in real mode |
| real_only | Run only in real mode |

## Connections

- [[mvp-site-pytest-integration]] - Pytest configuration
- [[mvp-site-real-provider]] - Real service provider
- [[mvp-site-fixtures]] - Core fixtures
