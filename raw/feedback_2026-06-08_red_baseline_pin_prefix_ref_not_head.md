---
name: red-baseline-pin-prefix-ref-not-head
description: "RED/GREEN baseline tests that source pre-fix files from `git HEAD` go vacuous once the fix commits — pin to origin/main"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c7284441-d453-452d-a263-c2cb4b131665
---

A RED-baseline harness that serves the "pre-fix" variant of files via `git show HEAD:<file>` reproduces the bug ONLY until the fix is committed — after commit, `HEAD` == the fix, so the RED capture serves the FIXED files and stops reproducing the flash. The RED test then fails (vacuous RED), violating the AC8 RED/GREEN pairing.

**Why:** the baseline ref must predate the fix; `HEAD` moves to the fix the moment you commit.

**How to apply:** source the pre-fix variant from a ref that stays pre-fix while the PR is open — `origin/main` (with a `HEAD~1` fallback and an env override). Concrete case: `mvp_site/tests/test_mobile_welcome_flash_fouc.py` `PRE_FIX_REF = os.environ.get("FOUC_PRE_FIX_REF", "origin/main")` (commit 41f5c03d4a, PR #7379, bead rev-ljk7h). All 4 captures then pass: RED reproduces, GREEN logged-in/logged-out/desktop clean.

Related: [[project_2026-06-08_mobile_welcome_flash_is_fouc_not_reload]]
