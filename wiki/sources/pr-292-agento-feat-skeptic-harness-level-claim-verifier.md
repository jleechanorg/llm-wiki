---
title: "PR #292: [agento] feat(skeptic): harness-level claim-verifier for skeptic gate assertions"
type: source
tags: []
date: 2026-03-29
source_file: raw/prs-worldai_claw/pr-292.md
sources: []
last_updated: 2026-03-29
---

## Summary
bd-upxh: Deterministic claim verifier enforcing **run-level + comment-level evidence** before agents may report 'working' status.

- **Fail-closed**: ambiguous → INSUFFICIENT/FAIL, never PASS
- **Decision matrix**: PASS only when both `runLevel.result === "pass"` AND `commentLevel.result === "pass"`
- **blocksWorking flag**: any outcome other than PASS blocks 'working' status

## Metadata
- **PR**: #292
- **Merged**: 2026-03-29
- **Author**: jleechan2015
- **Stats**: +1050/-3 in 10 files
- **Labels**: none

## Connections
