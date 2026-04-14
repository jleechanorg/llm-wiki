---
title: "Verify Retry Loop"
type: concept
tags: [pairv2, feature-pattern, automation]
sources: []
last_updated: 2026-04-13
---

## Description

The verify-retry loop pattern creates a self-correcting workflow where verifier FAIL triggers a retry cycle with feedback injection. When the verifier returns FAIL and cycles remain, the workflow loops back to implementation with the verifier's failure reasoning injected into the coder's next prompt.

## Why It Matters

In the original linear graph (implement → wait → verify → finalize), verifier FAIL went straight to finalize, losing the opportunity for self-correction. This pattern enables agents to learn from verification failures without human intervention.

## Key Technical Details

- **Routing function**: `_route_after_verify(state) -> str` routes based on verdict and remaining cycles
- **Feedback extraction**: `_extract_verifier_feedback(state) -> str` extracts reasoning from verification_report.json
- **Constants**: `PAIRV2_MAX_IMPL_CYCLES = 3`, `PAIRV2_RETRY_WORKSPACE_CLEAN = False`
- **Scope**: `.claude/pair/pair_execute_v2.py`

## Related Beads

- BD-pairv2-verify-retry-loop
