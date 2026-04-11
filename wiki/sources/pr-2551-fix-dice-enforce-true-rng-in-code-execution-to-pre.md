---
title: "PR #2551: fix(dice): Enforce true RNG in code_execution to prevent fabricated dice rolls"
type: source
tags: []
date: 2025-12-24
source_file: raw/prs-worldarchitect-ai/pr-2551.md
sources: []
last_updated: 2025-12-24
---

## Summary
- Fix Gemini code_execution dice uniformity by **seeding RNG in the system prompt** (`random.seed(time.time_ns())`) so each execution has fresh entropy.
- Add a real-server chi-square test script in `testing_mcp/` to verify 20-roll and 100-roll distributions without seeding in the script.
- Keep RNG seeding strictly in **mvp_site game code** (not tests), so production behavior is corrected.

## Metadata
- **PR**: #2551
- **Merged**: 2025-12-24
- **Author**: jleechan2015
- **Stats**: +1547/-50 in 18 files
- **Labels**: none

## Connections
