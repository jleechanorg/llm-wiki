---
name: rebase-on-origin-main-clears-presubmit-base-drift-failures
description: "Schema Coverage Guard and Smoke Mode Routing Contract failures on long-lived PR branches are often due to files added to main after the branch was forked — `git rebase origin/main` clears them, no source change needed"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 11b18814-6b01-49a8-a167-12c66b99835e
---

When a PR's `presubmit.yml` jobs (`Schema Coverage Guard`, `Smoke Mode Routing Contract`) fail with `FileNotFoundError: 'mvp_site/schemas/...'` or `bash: scripts/test_*.sh: No such file or directory`, and the same jobs pass on `origin/main`, the cause is almost always: **the branch was forked from `main` before the missing file was added**. The check is reading a file that exists on main but is absent on the branch.

**Fix:** `git rebase origin/main` (or cherry-pick just the missing files). No source code change required. Verified: dice-audit PR #7354 rebased from `cf4eb97d58` onto `origin/main` (ff979f9f9d), 14/14 commits applied cleanly, both failures cleared in the same push, `mergeStateStatus` flipped from `UNSTABLE` to `CLEAN`.

**Why:** The check is `python3 -c "import pathlib; pathlib.Path('mvp_site/schemas/X.txt').read_text()"` — the file must exist on the branch being checked out. Long-lived feature branches (especially 3+ days old) routinely miss additions to main. The `presubmit.yml` workflow has no `workflow_dispatch` trigger and doesn't re-run on Green Gate re-runs, so failures persist into the rollup even when the underlying issue is fixed by a rebase.

**How to apply:** Before assuming a presubmit failure is a real source code defect, `git ls-tree origin/main -- <missing-file-path>` to confirm the file exists on main. If yes, recommend rebase on `origin/main` over debugging the script.

**Triggered by:** PR #7354 feat/dice-audit-telemetry-reconciliation (2026-06-11). Missing files: `mvp_site/schemas/game_state_schema_coverage_waivers.txt` (added 2026-06-09 in commit 954b885) + `scripts/test_determine_smoke_mode.sh` (added 2026-06-10 in commit 25f6c5f). The [[project_2026-06-11_dice_audit_3pr_7green_push]] doc and [[feedback_2026-06-10_green_gate_first_run_after_push_false_negative]] complement this finding.
