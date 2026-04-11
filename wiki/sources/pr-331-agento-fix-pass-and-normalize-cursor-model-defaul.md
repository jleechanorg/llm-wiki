---
title: "PR #331: [agento] fix: pass and normalize Cursor model defaults"
type: source
tags: []
date: 2026-04-03
source_file: raw/prs-worldai_claw/pr-331.md
sources: []
last_updated: 2026-04-03
---

## Summary
- Cursor AO sessions were discarding `agentConfig.model` because the Cursor plugin removed the model field before launch.
- The result was non-deterministic behavior when old values like `claude-sonnet-4-6` were present in AO config.
- This patch restores explicit model passing and normalizes unsupported values to a safe Cursor default.

## Metadata
- **PR**: #331
- **Merged**: 2026-04-03
- **Author**: jleechan2015
- **Stats**: +159/-26 in 8 files
- **Labels**: none

## Connections
