---
title: "Verify-Fail-Retry Loop"
type: concept
tags: [pairv2, retry, self-correction]
sources: []
last_updated: 2026-02-24
---

## Definition

The Verify-Fail-Retry Loop is a cyclic execution pattern in pair programming where a verifier's FAIL verdict routes back to the coder for another implementation attempt, injecting the verifier's specific failure reasoning into the coder's next prompt. The loop continues until the verifier returns PASS or implementation cycles are exhausted.

## Architecture

### Graph Structure

```
generate_left_contract → generate_right_contract → left_contract
  → implement → wait_for_implementation_ready → verify
      ↓ PASS → finalize
      ↓ FAIL + cycles remaining → implement (with feedback)
      ↓ FAIL + cycles exhausted → finalize
```

### Feedback Injection

When verifier returns FAIL, the system:
1. Reads `verification_report.json` from the verify node output
2. Extracts `reasoning`, `issues`, and `test_results` fields
3. Formats as structured feedback block injected into coder's next prompt:

```
## VERIFIER FEEDBACK (attempt {impl_cycle + 1}/{max_impl_cycles})

Your previous implementation was reviewed and REJECTED. Fix these issues:

{extracted_feedback}

The workspace at {shared_workspace} already has your prior work.
Do NOT start from scratch. Run tests first, then fix the specific issues above.
```

## State Keys

- `impl_cycle` — implementation attempt counter (distinct from contract cycle)
- `max_impl_cycles` — max retries before giving up (default 3)
- `verifier_feedback` — extracted feedback from last verification

## Constants

- `PAIRV2_MAX_IMPL_CYCLES = 3` — max implementation retries per contract scope
- `PAIRV2_RETRY_WORKSPACE_CLEAN = False` — workspace preserved across retries

## Sources

- BD-pairv2-verify-retry-loop: full implementation of conditional edge verify→implement
