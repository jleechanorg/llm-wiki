---
title: "ErrorDetection"
type: concept
tags: ["error-detection", "debugging", "testing", "bugs"]
sources: []
last_updated: 2026-04-14
---

Error Detection is the first step in [[SelfDebugging]] — identifying that a bug or error has occurred. Without accurate error detection, debugging cannot begin.

## Key Properties
- **First step**: Detection must happen before diagnosis and repair
- **Types**: Runtime errors (crashes), logic errors (wrong output), type errors, assertion failures
- **Automated**: Execution feedback, test failures, and linting all serve as error detectors
- **Input for [[CodeRepair]]**: Error detection output (error messages, stack traces) feeds into the repair step

## Connections
- [[SelfDebugging]] — error detection is step 1 of the debugging pipeline
- [[CodeRepair]] — error detection outputs guide code repair
- [[Fuzzing]] — fuzzing is a systematic approach to automated error detection
- [[AdversarialTesting]] — adversarial testing systematically seeks to trigger error detection

## See Also
- [[SelfDebugging]]
- [[CodeRepair]]
