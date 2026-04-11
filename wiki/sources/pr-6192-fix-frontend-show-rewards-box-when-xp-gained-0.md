---
title: "PR #6192: fix(frontend): show rewards_box when xp_gained=0"
type: source
tags: []
date: 2026-04-11
source_file: raw/prs-worldarchitect-ai/pr-6192.md
sources: []
last_updated: 2026-04-11
---

## Summary
- Adds TDD regression tests to prevent re-introduction of bead **rev-qcax** bug
- Bug: `if (fullData.rewards_box && fullData.rewards_box.xp_gained > 0)` in `app.js` line 924 hid the rewards box when `xp_gained == 0` (loot-only drops, gold awards, level-up scenarios without XP)
- The fix (`if (fullData.rewards_box)`) was already applied in PR #6161 (commit `a872098d7c`); this PR adds regression coverage so the fix cannot silently regress

## Metadata
- **PR**: #6192
- **Merged**: 2026-04-11
- **Author**: jleechan2015
- **Stats**: +162/-0 in 3 files
- **Labels**: none

## Connections
