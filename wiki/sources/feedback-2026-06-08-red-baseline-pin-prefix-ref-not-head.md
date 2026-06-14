---
title: "RED-baseline harness must pin to prefix ref, not HEAD"
type: source
tags: [tdd, red-green, git, testing, worldarchitect-ai, fouc, ev-regression]
date: 2026-06-08
source_file: raw/feedback_2026-06-08_red_baseline_pin_prefix_ref_not_head.md
---

## Summary
A RED-baseline harness that serves the 'pre-fix' variant of files via 'git show HEAD:<file>' goes vacuous once the fix is committed — HEAD moves to the fix and the RED capture serves the FIXED files, failing the AC8 RED/GREEN pairing. Pin to origin/main (with HEAD~1 fallback and env override). Concrete case: mvp_site/tests/test_mobile_welcome_flash_fouc.py PRE_FIX_REF = os.environ.get('FOUC_PRE_FIX_REF', 'origin/main') (commit 41f5c03d4a, PR #7379, bead rev-ljk7h).

## Key Claims
- HEAD moves to the fix the moment you commit, so the RED test serves the fixed files and stops reproducing the bug — vacuous RED
- Solution: source pre-fix variant from a ref that stays pre-fix while the PR is open — origin/main (with HEAD~1 fallback and env override)
- All 4 captures then pass: RED reproduces, GREEN logged-in/logged-out/desktop clean

## Connections
- [[project_2026-06-08_mobile_welcome_flash_is_fouc_not_reload]]
- [[RedGreenBaseline]]
- [[TddEvidenceWorkflow]]
