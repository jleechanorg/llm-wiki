---
title: "Harness-Fix PRs Status 2026-04-15 — skeptic-gate GATE-5 Fail + Rebase Needed"
type: source
tags: [worldarchitect.ai, skeptic-gate, harness-fix, design-doc, GATE-5]
date: 2026-04-15
---

## Summary

PR #6276 merged at 16:26 UTC. Harness-fix PRs (#6289/#6292/#6285/#6287) were branched from pre-merge state and need rebase on new main. Two are CONFLICTING. All three non-conflicting PRs fail skeptic-gate on GATE-5 (unresolved author comments) at ~0s — fast-fail indicates stale GraphQL query picking up old review threads. Rebase on new main + re-trigger skeptic-gate expected to clear GATE-5.

## PR Status

| PR | Branch | Status | Mergeable | skeptic-gate | Action |
|----|--------|--------|-----------|-------------|--------|
| #6276 | feat/world-logic-clean-layer3 | **MERGED** | — | VERDICT: PASS | Done |
| #6292 | fix/green-gate-design-doc-blocker | OPEN | MERGEABLE | FAIL GATE-5 | rebase on new main, re-trigger |
| #6285 | fix/claude-md-design-doc-gate-rule | OPEN | MERGEABLE | FAIL GATE-5 | rebase on new main, re-trigger |
| #6289 | fix/br-4bk-design-doc-skill | OPEN | CONFLICTING | FAIL GATE-5 | rebase first, then re-trigger |
| #6287 | fix/resolve-signal-rename | OPEN | CONFLICTING | — | needs rebase on main |

## skeptic-gate GATE-5 Fail Analysis

**Symptom**: All three non-conflicting PRs fail GATE-5 at ~0s (fast-fail)
**Run history**:
- PR #6285: 24465754084 (failure), 24465739971, 24465629215, 24465616624
- PR #6292: 24465391499 (failure), 24464995307, 24464887881
- PR #6289: 24455501977, 24455496495, 24455489084

**Root cause**: GATE-5 uses GraphQL query for unresolved author review comments. Query picks up stale threads from before PR #6276 merged.

**Fast-fail interpretation**: When a PR has 0 unresolved comments, GATE-5 exits in <1s with PASS. When it fails in ~0s with FAIL, it means the query returned an error OR returned results when none were expected. The ~0s fail pattern = query error or unexpected results, not actual unresolved comments.

## New Main State

After PR #6276 merge, main has:
- `rewards_engine.py` (new file)
- `llm_parser.py` (single orchestration root)
- `design-doc-gate.yml` (8 CI grep gates)
- world_logic.py: 0 rewards_engine PUBLIC API imports
- `check_upper_bound()` function for line count gates

## Merge Order

1. **PR #6289** (CONFLICTING) → rebase on origin/main first
2. **PR #6292** → MERGEABLE, rebase on new main, re-trigger skeptic-gate
3. **PR #6285** → MERGEABLE, rebase on new main, re-trigger skeptic-gate
4. **PR #6287** (CONFLICTING) → rebase last

**Note**: After rebasing on new main, `design-doc-gate.yml` should be present and design doc grep gates should pass.

## PR Status

| PR | Branch | Status | Mergeable | skeptic-gate | Action |
|----|--------|--------|-----------|-------------|--------|
| #6276 | feat/world-logic-clean-layer3 | **MERGED** | — | VERDICT: PASS | Done |
| #6308 | feat/world-logic-clean-layer3 | OPEN | CONFLICTING | — | rev-v4ci09 commit pushed — needs PR review |
| #6285 | fix/claude-md-design-doc-gate-rule | OPEN | MERGEABLE | **in_progress** (24466469948) | rebased SHA `28822775af`, skeptic running |
| #6292 | fix/br-4bk-green-gate-design-doc | OPEN | MERGEABLE | pending | rebase succeeded, push + trigger pending |
| #6289 | fix/br-4bk-design-doc-skill | OPEN | CONFLICTING | — | still conflicting |
| #6287 | fix/resolve-signal-rename | OPEN | CONFLICTING | — | **rebase FAILED** — 6 conflicts, manual needed |

## Late Status Update

- **PR #6287 conflict**: branch renames `_resolve_level_up_signal` → `_is_level_up_ui_active`. Post-#6276 world_logic.py no longer has same targets. Rebase aborted — needs manual resolution.
- **skeptic-gate runs**: 24466636364 (queued), 24466596142 (pending), 24466584592 (queued), 24466469948 (in_progress for #6285)

## Final Status (evening)

| PR | Branch | Mergeable | Status | Next |
|----|--------|-----------|--------|------|
| #6292 | fix/br-4bk-green-gate-design-doc | MERGEABLE | BLOCKED | Admin-merge when PR Coverage completes |
| #6285 | fix/claude-md-design-doc-gate-rule | MERGEABLE | UNSTABLE | Wait for CI + skeptic |
| #6287 | fix/resolve-signal-rename | MERGEABLE | BLOCKED | CI running |
| #6308 | feat/world-logic-clean-layer3 | CONFLICTING | DIRTY | Conflict resolution needed |
| #6289 | fix/br-4bk-design-doc-skill | CONFLICTING | DIRTY | **Close as obsolete** — design-doc-as-contract.md deleted by #6276 |

**Key findings**:
- PR #6292: skeptic SUCCESS (run 4073), Green Gate pass, all CI pass except PR Coverage Report pending
- PR #6285: rebased SHA `28822775af`, CI running, skeptic queued 24467526122
- PR #6287: CI running (Design Doc Grep Gates, Green Gate)
- PR #6289: **obsolete** — branch modifies `design-doc-as-contract.md` which was deleted by PR #6276
- PR #6308: rev-v4ci09 commit — conflict in world_logic.py needs resolution

**mergeStateStatus meanings**: CLEAN = no conflicts + no blocking checks; BLOCKED = required checks pending; UNSTABLE = status checks failing; DIRTY = merge conflicts

## Connections
- [[PR6276]] — MERGED
- [[DesignDocGate]] — design-doc-gate.yml with 8 grep gates
- [[SkepticGate]] — Skeptic Gate PASS for #6285 (24468086251)
- [[rev-v4ci09]] — COMPLETE: _xp_increased deleted, PR #6308 OPEN