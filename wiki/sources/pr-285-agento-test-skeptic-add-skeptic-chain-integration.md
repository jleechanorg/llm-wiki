---
title: "PR #285: [agento] test(skeptic): add skeptic-chain-integration test validating full skeptic chain"
type: source
tags: []
date: 2026-03-29
source_file: raw/prs-worldai_claw/pr-285.md
sources: []
last_updated: 2026-03-29
---

## Summary
- Adds `packages/core/src/__tests__/skeptic-chain-integration.test.ts` validating the full skeptic chain from `runSkepticReview` through `ao skeptic verify` to VERDICT comment posting and GHA jq filter matching
- 7 tests covering: PASS/FAIL/SKIPPED verdict parsing, subprocess args, postVerdict body format, and skeptic-gate.yml JQ filter correctness

## Metadata
- **PR**: #285
- **Merged**: 2026-03-29
- **Author**: jleechan2015
- **Stats**: +588/-0 in 2 files
- **Labels**: none

## Connections
