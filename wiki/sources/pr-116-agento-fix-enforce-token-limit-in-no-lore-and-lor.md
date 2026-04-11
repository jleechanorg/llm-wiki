---
title: "PR #116: [agento] fix: enforce token limit in no-lore and lore fallback paths (worldai_claw-5e4)"
type: source
tags: []
date: 2026-03-27
source_file: raw/prs-worldai_claw/pr-116.md
sources: []
last_updated: 2026-03-27
---

## Summary
buildSystemInstructionWithLimit() had two fallback paths that returned raw SYSTEM_INSTRUCTION (4337+ tokens) when trimToTokenLimit() produced output missing coupled state/planning markers — even when the token limit was as low as 100.

## Metadata
- **PR**: #116
- **Merged**: 2026-03-27
- **Author**: jleechan2015
- **Stats**: +629/-875 in 6 files
- **Labels**: none

## Connections
