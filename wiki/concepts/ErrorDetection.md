---
title: "ErrorDetection"
type: concept
tags: ["error-detection", "debugging", "testing", "bugs"]
sources: []
last_updated: 2026-04-14
---

Error Detection is the first step in [SelfDebugging](SelfDebugging.md) — identifying that a bug or error has occurred. Without accurate error detection, debugging cannot begin.

## Key Properties
- **First step**: Detection must happen before diagnosis and repair
- **Types**: Runtime errors (crashes), logic errors (wrong output), type errors, assertion failures
- **Automated**: Execution feedback, test failures, and linting all serve as error detectors
- **Input for [CodeRepair](CodeRepair.md)**: Error detection output (error messages, stack traces) feeds into the repair step

## Connections
- [SelfDebugging](SelfDebugging.md) — error detection is step 1 of the debugging pipeline
- [CodeRepair](CodeRepair.md) — error detection outputs guide code repair
- [Fuzzing](Fuzzing.md) — fuzzing is a systematic approach to automated error detection
- [AdversarialTesting](AdversarialTesting.md) — adversarial testing systematically seeks to trigger error detection

## See Also
- [SelfDebugging](SelfDebugging.md)
- [CodeRepair](CodeRepair.md)
