---
title: "PR #99: test: TDD regression tests for chain_anchor.ts anchor() config validation (WC-vsr)"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-worldai_claw/pr-99.md
sources: []
last_updated: 2026-03-26
---

## Summary
`chain_anchor.ts` `anchor()` previously had a bug where it could report success even when no RPC URL or contract address was configured (WC-vsr). The fix was applied in commit `0906f14`, but no tests existed to guard against regression.

## Metadata
- **PR**: #99
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +140/-0 in 1 files
- **Labels**: none

## Connections
