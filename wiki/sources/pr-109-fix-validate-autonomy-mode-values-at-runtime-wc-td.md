---
title: "PR #109: fix: validate autonomy_mode values at runtime (WC-tdl)"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-worldai_claw/pr-109.md
sources: []
last_updated: 2026-03-26
---

## Summary
`coerceAutonomyMode()` silently accepted any string input and defaulted to `BALANCED`, meaning typos, garbage data, or invalid mode strings propagated through the companion system without any error signal.

## Metadata
- **PR**: #109
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +119/-2 in 4 files
- **Labels**: none

## Connections
