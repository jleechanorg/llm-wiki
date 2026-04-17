---
title: "Matched Corpus PRs — br-v84 (n=3 per cell)"
type: plan
last_updated: 2026-04-17
supersedes: "earlier br-4zl plan (n=1 per cell)"
---

## Why n=3 per cell

The router prerequisite gate (`scripts/validate_router_prereqs.py`) counts
ranking reversals across technique pairs. At n=1 per (PR, technique) cell, a
single run can flip the ranking purely from scoring noise — all three
techniques currently cluster within ~3 points of each other against a rubric
ceiling near 87.

Running **3 samples per cell** lets us aggregate to a cell mean before
counting reversals. Reversals are then driven by technique signal, not
per-run variance. Total evaluation cost: **5 PRs × 3 techniques × 3 runs =
45 evaluation runs.**

This supersedes the older n=1 plan that only covered ET vs PRM.

---

## Schema (nested)

`technique_bandit/bandit_state.json` must be migrated from flat to nested:

```json
"rubric_scores": {
  "6265": {
    "SR":  [{"commit_sha": "...", "run_session": "...", "total": 85, "breakdown": {...}},
             {"commit_sha": "...", "run_session": "...", "total": 83, "breakdown": {...}},
             {"commit_sha": "...", "run_session": "...", "total": 86, "breakdown": {...}}],
    "ET":  [{...}, {...}, {...}],
    "PRM": [{...}, {...}, {...}]
  }
}
```

`scripts/validate_router_prereqs.py::build_matched_table` aggregates each cell
to its mean of `total` before counting reversals. Legacy flat entries are
still accepted so existing Phase 3 data is not invalidated.

---

## Selected 5 PRs for Matched Corpus

Selection constraints:
- Merged to `main` (baseline exists)
- Diff < 500 lines (fits generation context without heavy context stripping)
- Type diversity across bug fix / refactor / feature / small-fix
- Mix of production-origin and agent-origin PRs

| # | PR   | Category                  | Delta       | Reason |
|---|------|---------------------------|-------------|--------|
| 1 | 6265 | bug fix (rewards)         | +168/-22    | Streaming passthrough normalization — already has PRM score; different domain |
| 2 | 6261 | refactor                  | +216/-13    | Centralized numeric extraction — pure architectural change |
| 3 | 6245 | bug fix (level-up)        | +88/-131    | Production-origin (no agent label) — real regression fix |
| 4 | 6243 | bug fix (state semantics) | +72/-6      | Small sample — tests variance on narrow changes |
| 5 | 6269 | feature port              | +88/-28     | CR fallback port — different pattern (interface addition) |

### Diversity achieved
- 3 bug fixes (#6265 rewards, #6245 level-up, #6243 state)
- 1 refactor (#6261)
- 1 feature port (#6269)
- Diff sizes: 78 LOC (#6243) to 229 LOC (#6261)
- Code areas: rewards, numeric extraction, level-up, game_state, skeptic gates

---

## Run Plan (45 evaluation runs)

For each of the 5 PRs and each technique in {SR, ET, PRM}:

1. Reset worktree to parent of PR's merge commit.
2. Run autor generation under the technique (`autor_runner.py --technique <T> --pr <N>`).
3. Open the resulting PR via `scripts/autor_pr.py::open_draft_autor_pr` — this forces draft + `[autor]` label + technique tag.
4. Score the diff against the 6-dim rubric; write:
   - `research-wiki/scores/<tech>_<pr>_<run_session>.json`
   - `wiki/syntheses/et_logs/<tech>_<pr>_<run_session>.log`
5. Append the row to `rubric_scores[<pr>][<tech>]` with `run_session`, `commit_sha`, `breakdown`, `total`.
6. Close the PR via `scripts/autor_pr.py::close_after_score` (refuses without score JSON).
7. Repeat until every cell has exactly 3 rows (n=3).

After all 45 runs:
- Run `scripts/validate_autor_pr_lifecycle.py` — expect PASS (no MERGED, no orphaned OPEN).
- Run `scripts/validate_router_prereqs.py` — required PASS to unblock br-ahf (router work).

---

## Oracle-Router Effect-Size Check (gate 2)

Passing the reversal gate is necessary but not sufficient. Before opening any
router PR, compute:

```
oracle_score = mean over PRs of max(cell_mean[SR], cell_mean[ET], cell_mean[PRM])
baseline_score = max over techniques of (mean over PRs of cell_mean[tech])
uplift = oracle_score - baseline_score
```

Router work proceeds only if `uplift ≥ 2.0` rubric points. If uplift is
smaller, close br-ahf with a null-result synthesis — do not rationalize a
router that beats the best fixed technique by < 2 points at the rubric
ceiling.

---

## Failure handling

If after 45 runs the gate still fails:
- **< 2 reversals**: technique ranking is genuinely stable across this PR
  set. Do NOT extend to n=5 hoping for reversals — that is p-hacking. Close
  br-v84 and br-ahf with a null-result synthesis; the bandit answer is
  "pick the top-mean technique, no router needed."
- **Gate passes but uplift < 2.0**: same outcome — null-result close of
  br-ahf.
- **Gate passes and uplift ≥ 2.0**: unblock br-ahf and proceed.

---

## Artifacts produced

- 45 score JSONs under `research-wiki/scores/`
- 45 run logs under `wiki/syntheses/et_logs/`
- 15 closed autor PRs (5 PRs × 3 techniques, each with n=3 merged into the
  same closed PR via amended commits or 3 separate draft PRs per cell —
  implementation detail for the dumb agent)
- Updated `technique_bandit/bandit_state.json` with nested schema
- Bandit-state drift note reconciled (SR missing entry restored as part of
  first SR run)
