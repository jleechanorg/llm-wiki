---
title: "Dual-Mode Testing"
type: concept
tags: [testing, integration, decorator]
sources: ["real-mode-testing-framework-integration-validation"]
last_updated: 2026-04-08
---

Testing pattern where the same test executes in both mock and real modes. Validates that code behaves consistently across both modes and that mocks accurately represent real behavior.

## Implementation
- **DualModeTestMixin**: Base class enabling dual-mode execution
- **@dual_mode_test decorator**: Marks tests to run in both modes
- **@real_mode_only decorator**: Marks tests to run only in real mode
- **@skip_in_real_mode decorator**: Skips tests in real mode only

## Benefits
- Catches mock/real divergence early
- Provides confidence in mock fidelity
- Enables comprehensive test coverage
