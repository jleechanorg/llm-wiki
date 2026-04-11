---
title: "PR #6192: fix(frontend): show rewards_box when xp_gained=0"
type: source
tags: [worldarchitect-ai, rewards-box, frontend, regression, pr-6192]
date: 2026-04-11
source_file: mvp_site/frontend_v1/app.js
---

## Summary
Adds TDD regression tests to prevent re-introduction of bead rev-qcax bug. Bug: `if (fullData.rewards_box && fullData.rewards_box.xp_gained > 0)` in `app.js` line 924 hid the rewards box when `xp_gained == 0` (loot-only drops, gold awards, level-up scenarios without XP). The fix (`if (fullData.rewards_box)`) was already applied in PR #6161; this PR adds regression coverage.

## Key Claims
- The buggy `xp_gained > 0` guard was removed in PR #6161 (commit a872098d7c)
- This PR adds static-analysis regression tests only — no production code changes
- Guards against loot-only drops, gold-only awards, zero-XP level-up scenarios being hidden

## Files Changed
- `.beads/issues.jsonl` (+1, -0)
- `mvp_site/tests/frontend/test_rewards_box_xp_zero.js` (+77, -0)
- `mvp_site/tests/test_rewards_box_xp_zero_condition.py` (+84, -0)

## Test Coverage
- Verifies buggy `xp_gained > 0` guard is absent from `app.js`
- Verifies correct `if (fullData.rewards_box)` truthiness check is present
- Verifies `rb.xp_gained` is still read for display (regression guard)
- Verifies `rewards-box` CSS class is still referenced

## Connections
- Related PR #6161 — where the actual fix was already shipped
- Bead: rev-qcax
