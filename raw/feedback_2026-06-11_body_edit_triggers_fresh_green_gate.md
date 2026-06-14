---
name: body-edit-triggers-fresh-green-gate
description: "gh pr edit --body-file on a PR with stalled Green Gate re-triggers Green Gate on the same head SHA (no force-push needed); use to fix Gate 0 / Gate 6 gaps post-push"
metadata:
  type: feedback
---

When a PR's Green Gate is stalled on Gate 0 (Design Doc grep) or Gate 6 (evidence URL), and you don't want to force-push a new SHA, you can edit the body to fix the gates and the `pull_request` event will trigger a fresh Green Gate run on the SAME head SHA.

**Verified on 2026-06-11** with these 7 PRs:
- #7352 (dd42e637) — added ## Design Decision + ## Tenets + Gate 6 gist → Green Gate re-triggered at 23:35Z, in_progress by 23:47Z, step 3 (gates 1-6) PASSED
- #7357 (b39d58bb) — added Gate 6 gist
- #7424 (ef997821) — added Gate 6 gist
- #7372 (f3ff321e) — added Gate 6 gist
- #7387 (70ac228d) — added ## Design Decision + ## Tenets
- #7379 (81f7d77e) — replaced `## DESIGN DOC: N/A` with `## Design Decision` + ## Tenets
- #7358 (1c5d1d2d) — added ## Design Decision + ## Tenets

**Why:** Avoids the first-run-after-push false-negative pattern + a stale `headRefOid` cache for followers, while still re-running the gate on the exact SHA you intend to merge.

**How to apply:**
1. Identify gate failure cause (read Green Gate log for the prior in_progress run)
2. Edit body with `gh pr edit N --body-file /tmp/pr-N-body-new.md`
3. Watch `gh api "repos/.../actions/runs?head_sha=..."` for a new run started after the edit time
4. The new run uses the same head SHA so no force-push approval needed

**Caveat:** Multiple body edits in a short window create multiple cancelled "first runs" — the *second* (non-cancelled) run is the real verdict. Only one in-flight Green Gate per head is useful.
