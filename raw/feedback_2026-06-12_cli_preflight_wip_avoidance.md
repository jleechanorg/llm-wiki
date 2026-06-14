---
name: cli-preflight-pattern-wip-avoidance-discipline
description: "When a workstream is in-flight on runner/__main__.py + runner/handlers.py, scope a separate workstream to NEW files (runner/preflight.py) and bash wrappers only. File-disjoint lanes for parallel subagents."
metadata: 
  node_type: memory
  type: feedback
  bead: jleechan-xgx
  originSessionId: ed6f27c4-4378-42f4-bec7-7e711334e555
---

When `runner/__main__.py` + `runner/handlers.py` are being modified by an in-flight workstream (e.g. the `claudeaf` backend addition), **scope a separate workstream to NEW files only** and bash wrappers (`bin/dark-factory`, `bin/df-healer`).

The CLI preflight module ships to `runner/preflight.py` (new) + `tests/test_preflight.py` (new) + bash wrapper wiring. The preflight returns a structured JSON `{"status": "pass|warn|fail", "checks": [...], "fallback_recommendation": "codex"}` and the bash wrappers gate entry BEFORE exec'ing Python so the user sees a JSON diagnostic, not a traceback. Exit code 2 on fail, exit 0 with stderr warning on warn.

**Why:** `git diff --name-only HEAD` is the source of truth for "is this file in flight?" — not vibes, not memory. The `claudeaf` WIP added `claudeaf` to backend choices in `__main__.py` and dispatch logic in `handlers.py`; stomping on those mid-edit creates a merge collision that takes hours to unwind. The fix: a NEW `runner/preflight.py` module that has zero overlap with the WIP'd files. The preflight module is invoked from the bash wrapper BEFORE the runner Python code runs, so the WIP'd `__main__.py` doesn't need to be touched at all.

**How to apply:** Before fanning out subagents on a multi-workstream day, run `git diff --name-only HEAD` to enumerate files in flight. For each new workstream, file-overlap check via `git diff --name-only <base>...<branch>` (or pairwise `git merge-tree --write-tree`) to compute exact file set per lane. Lanes sharing ANY mutable file are NOT independent. When the WIP'd file is the natural home for new behavior, route the new behavior to a NEW file that the WIP'd file imports/uses, and modify the bash entrypoint instead.

**Related:** [[project_2026-06-12_thermo_simplify_cross_validation]] (file-disjoint lanes pattern), [[feedback_2026-06-09_priority_queue_dispatch]] (handler-side backend dispatch), [[project_2026-06-08_claudew_delete_agy_reviewer_gate]] (agy reviewer-gate pattern with `backend_missing` metadata).
