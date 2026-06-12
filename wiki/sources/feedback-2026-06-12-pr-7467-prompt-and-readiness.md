---
title: "PR 7467 review — generic prompt fixes + live PR head + readiness gates"
type: source
date: 2026-06-12
tags: [prompt-engineering, merge-readiness, multi-writer-pr, feedback, pr-7467, worldarchitect]
bead_ids: [rev-4nu0j, rev-1ver0]
sources: [feedback-2026-06-12-generic-prompt-fixes, feedback-2026-06-12-live-pr-head-staleness, feedback-2026-06-12-pr-readiness-minimum-gates]
last_updated: 2026-06-12
---

# PR 7467 review — three intertwined lessons

PR [#7467](https://github.com/jleechanorg/worldarchitect.ai/pull/7467) ("Fix level-up modal canonical session routing") review surfaced three related lessons. All three are captured as Claude auto-memory; this source page indexes them and the relationship graph.

## The three lessons

### 1. Generic prompt fixes, not class-specific enumerations

**Anti-pattern (committed `7610402bc3`, 2026-06-12):** When Codex leveling review flagged a missing `Sanctuary` from a Level 3 Oath of Devotion prepared-spell loadout, the fix enumerated hardcoded spell lists for all three Paladin oaths (Devotion, Ancients, Vengeance L1+L2). User feedback: "shouldnt be overly specific to paladin / needs to be generic."

**Correct pattern:** A single rule — "When recommending a subclass's prepared-spell/feature loadout, include ALL subclass-granted always-known/always-prepared features, surfaced by name in the `Recommended package:` paragraph. The specific spells/features are defined in the SRD or the player's chosen subclass; consult that source. Omitting granted features is a HARD INVARIANT violation." — covers Paladin oaths, Cleric domains, Warlock patrons, Druid circles, Sorcerer origins, Ranger conclaves, Artificer specialists, and any future subclass.

**Why:** ZFC says the LLM owns the choice/benefit selection. The prompt should give the LLM the **rule** + a **reference to source of truth**, not a hardcoded list. Hardcoded lists drift from actual rules (errata, edition changes) and don't generalize.

Memory: `feedback_2026-06-12_generic_prompt_fixes.md`
Bead: `rev-4nu0j` (rework `7610402bc3`)

### 2. Live PR head tracking — `git fetch && git rev-parse origin/<branch>` before any "PR is at SHA X" claim

**Anti-pattern (PR #7467 review session, 2026-06-12):** Local `git log` showed head `e619e882` (the .dot chart commit). I treated local as the live PR. The user corrected: "Live PR head is now `212b0133`, not `e619e882`, and not the tested `31aaceb8` or evidence-listed `a558732`." Between `31aaceb8` (test time) and the user's view, three commits had landed: the .dot chart, my over-fit prompt fix, AND a production routing/auth change in `mvp_site/agents.py` and `mvp_site/rewards_engine.py` (`212b0133`).

**Correct pattern:** Before any "the PR is at SHA X" or "the test ran on head X" claim:
1. `git fetch origin`
2. `git rev-parse origin/<branch>` — this is the live head
3. The "live head" ≠ local HEAD on multi-writer PRs
4. Re-test at the live head when the user references "current head" or "live head"

**Why:** Multi-writer PRs accumulate commits from any agent or human. Local is just one writer's view; the live PR reflects all writers.

Memory: `feedback_2026-06-12_live_pr_head_staleness.md`

### 3. PR readiness minimum gates (6 gates, not "looks good")

The user's "Minimum before merge" list is the canonical PR-readiness gate for this repo. Six required gates, ALL must pass before any "ready" claim:

| # | Gate | How to verify |
|---|---|---|
| 1 | Live head SHA matches PR body evidence | `git fetch origin && git rev-parse origin/<branch>` must equal the SHA cited in the PR body |
| 2 | CI green at current head | `gh pr checks <N>` shows all checks complete + passing, not "queued/running" |
| 3 | All review threads resolved | `gh pr view <N> --json comments` — every thread body shows "✅ Addressed" or explicit dismissal |
| 4 | CodeRabbit enabled + reviewDecision APPROVED | `gh pr view <N> --json reviewDecision` — must be `APPROVED`, not `""` or `REVIEW_REQUIRED` |
| 5 | Real-LLM test re-run at live head passes | Re-run the relevant `testing_mcp/` test at the live head SHA |
| 6 | Skeptic verdict matches live head | Latest `/skeptic` `VERDICT: PASS` must cite the live head SHA, not an older one |

PR #7467 fails gates 1, 2, 3, 4, 5 currently:
- Body cites `a558732`; live is `212b0133` (gate 1 fail)
- CI checks are queued/running (gate 2 fail)
- 5 unresolved review threads (gate 3 fail)
- CodeRabbit skipped, reviewDecision empty (gate 4 fail)
- Real-LLM test last ran on stale `31aaceb8` (gate 5 fail)

Memory: `feedback_2026-06-12_pr_readiness_minimum_gates.md`
Bead: `rev-1ver0` (PR 7467 readiness audit)

## Relationship graph

```
Test fails on prompt content
  → Lesson 1: fix generic rule, not class list
  → Bead rev-4nu0j: rework 7610402bc3

User says "PR is at live head 212b0133"
  → Lesson 2: git fetch before claiming SHA
  → Local 31aaceb8 ≠ origin 212b0133 on multi-writer PR
  → Memory feedback_2026-06-12_live_pr_head_staleness.md

User says "Minimum before merge: ..."
  → Lesson 3: 6 readiness gates
  → Bead rev-1ver0: audit all 6 gates at live head
  → Memory feedback_2026-06-12_pr_readiness_minimum_gates.md

All three reinforce:
  - Verify the live state, not the local state
  - Generic fixes, not over-fit
  - Hard gates, not soft signals
```

## References

- PR: [#7467](https://github.com/jleechanorg/worldarchitect.ai/pull/7467)
- Local commit (over-fit, needs rework): [`7610402bc3`](https://github.com/jleechanorg/worldarchitect.ai/commit/7610402bc3) — "Fix: enumerate Paladin oath-granted always-prepared spells for L3 Sacred Oath"
- Live head (per user): [`212b0133`](https://github.com/jleechanorg/worldarchitect.ai/commit/212b0133b23d858d5260e640cf02555a07f59816) — "Level-Up: Resolve routing preemption and finish release auth"
- Test ran on (stale): local `31aaceb8` — Codex review flagged content issue
- PR body evidence SHA (stale): `a558732`
- Beads: `rev-4nu0j` (rework), `rev-1ver0` (readiness audit)
- Memory files: `feedback_2026-06-12_generic_prompt_fixes.md`, `feedback_2026-06-12_live_pr_head_staleness.md`, `feedback_2026-06-12_pr_readiness_minimum_gates.md`
- Roadmap log: `~/roadmap/learnings-2026-06.md` (entry 2026-06-12 — PR #7467 review)

## Related concepts

- [[Prompt Engineering]] — generic-rule vs hardcoded-list discipline
- [[Merge Readiness Contract]] — pre-existing 5-gate contract; this is the 6-gate superset
- [[E2E Testing]] — the real-LLM test re-run at live head is a Layer 2 E2E check
- [[CodeRabbit]] — reviewDecision states: APPROVED / CHANGES_REQUESTED / REVIEW_REQUIRED / ""
- [[CI Gates]] — checks reading from `statusCheckRollup` mixed `StatusContext`/CheckRun shape
