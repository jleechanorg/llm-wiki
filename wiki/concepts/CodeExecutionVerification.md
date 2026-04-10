---
title: "Code Execution Verification"
type: concept
tags: [code-execution, dice-integrity, validation]
sources: [code-execution-evidence-extraction-rng-verification-tests, dice-logging-functions-unit-tests]
last_updated: 2026-04-08
---

## Definition
The process of validating that code was actually executed by examining tool results for evidence of execution and checking for random number generation (RNG) usage within executed code.

## Verification Criteria

### Tool Execution Evidence
- Tool results must contain execution output
- Must show actual code running, not just being requested

### RNG Source Validation
- Code must use `random.randint()` or similar RNG functions
- Manual value insertion → fabrication violation
- Example flagged: `result = 15` (hardcoded) vs `result = random.randint(1, 20)` (valid)

## Logging
- Logs pre/post detection context for debugging
- Flags fabrication violations with specific error types
- Includes tool execution status and code analysis results

## Related Concepts
- [[DiceFabricationDetection]] — uses verification results
- [[ToolResultValidation]] — validating tool execution output
