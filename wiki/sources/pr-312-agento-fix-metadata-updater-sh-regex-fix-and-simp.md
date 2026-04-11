---
title: "PR #312: [agento] fix: metadata-updater.sh regex fix and simplification"
type: source
tags: []
date: 2026-03-30
source_file: raw/prs-worldai_claw/pr-312.md
sources: []
last_updated: 2026-03-30
---

## Summary
The `metadata-updater.sh` PostToolUse hook had accumulated over-engineered branch detection logic. Three specific improvements are needed:

1. **Env-assignment regex** was using `[^[:space:]]*` which greedily consumes the `=` character, causing `FOO=bar gh pr create` to not strip correctly.
2. **Sed escaping** unnecessarily escaped `|` which is not a BRE special char (delimiter is `/`, not `|`).
3. **Branch verification via `git rev-parse`** added latency and complexity for marginal safety — the

## Metadata
- **PR**: #312
- **Merged**: 2026-03-30
- **Author**: jleechan2015
- **Stats**: +6/-6 in 1 files
- **Labels**: none

## Connections
