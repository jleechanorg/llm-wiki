---
title: "Mock Validation"
type: concept
tags: [testing, mock-validation, capture-analysis, quality-assurance]
sources: []
last_updated: 2026-04-08
---

## Definition
The process of comparing captured real service interactions against mock response files to assess mock accuracy, identify discrepancies, and generate improved baselines.

## Validation Workflow
```bash
# 1. Run tests with capture
export TEST_MODE=capture
python test_suite.py

# 2. Analyze performance
python -m mvp_site.testing_framework.capture_cli analyze

# 3. Compare with mocks
python -m mvp_site.testing_framework.capture_cli compare capture.json mocks.json

# 4. Generate improved mocks
python -m mvp_site.testing_framework.capture_cli baseline capture.json new_mocks.json
```

## Metrics
- **Accuracy Score**: Percentage of mock responses matching real responses
- **Error Detection**: Identifies mocks that fail when real services succeed
- **Missing Mocks**: Detects operations with no corresponding mock
- **Performance Analysis**: Tracks slowest/fastest operations

## Related Concepts
- [[DataCaptureFramework]] — provides capture infrastructure
- [[CaptureAnalyzer]] — performs the comparison analysis
- [[MockBaselineGeneration]] — creating mocks from real data
