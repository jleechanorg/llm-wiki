---
title: "Harness-Fix PRs + PR #6276 Status 2026-04-16 Late — 0 Runners Block All CI"
type: source
tags: [worldarchitect.ai, PR6276, harness-fix, code-rabbit, CI-blocked]
date: 2026-04-16
---

## Summary

PR #6276 (`feat/world-logic-clean-layer3`) merged 2026-04-15 at 16:26 UTC. The 4 harness-fix PRs remain blocked from 7-green by a combination of CR reviews and a critical infrastructure issue: **0 self-hosted runners** for `jleechanorg/worldarchitect.ai` — all CI runs (green-gate + skeptic-gate) are queued indefinitely with no executor available.

## PR #6276 Post-Merge State

| Dimension | Status |
|-----------|--------|
| mergeStateStatus | MERGED |
| Additions/deletions | +4818 / -2752 |
| world_logic.py line count | ~8,896 (target ~1,500) |
| rev-v4ci01 | **TOMBSTONED** — strip to 1500 lines unachievable |
| rev-v4ci05 | **Complete** — 0/3 behavioral equivalence pairs equivalent |
| Design doc equivalence claim | **WRONG** — 0/3 pairs equivalent |

Design doc claimed 5 world_logic functions map to rewards_engine equivalents. **rev-v4ci05 behavioral equivalence audit proved this FALSE.** Two different philosophies: `rewards_engine` (XP-threshold/causal) vs `world_logic` (flag-driven/stateful).

## 4 Harness-Fix PRs State

| PR | Branch | CR State | mergeStateStatus | CI | Primary Blocker |
|----|--------|----------|------------------|----|-----------------|
| #6287 | fix/resolve-signal-rename | DISMISSED x5 | UNSTABLE | PENDING (0 runners) | CR not re-reviewing; no runners |
| #6289 | fix/br-4bk-design-doc-skill | CHANGES_REQUESTED x2 | BLOCKED | PENDING (0 runners) | CR: fresh-signal bypass + isinstance guards |
| #6308 | feat/world-logic-clean-layer3 | CHANGES_REQUESTED x5 | BLOCKED | PENDING (0 runners) | CR: 20+ comments; skeptic concurrency fix in diff |
| #6328 | feat/design-doc-as-contract-skill | None | UNSTABLE | QUEUED stuck >1h | No CR; no runners |

## Critical Infrastructure Issue: Zero Runners

```bash
gh api repos/jleechanorg/worldarchitect.ai/actions/runners
# Returns: {"total_count":0,"runners":[]}
```

All CI blocked. Stuck runs (all PENDING/QUEUED):

| PR | green-gate Run | Status |
|----|---------------|--------|
| #6287 | 24483121971 | pending |
| #6289 | 24483330789 | pending |
| #6308 | 24483000293 | pending |
| #6328 | 24482116086 | queued (stuck >1h) |

## CR CHANGES_REQUESTED Details

### PR #6289 — 2 CR reviews (9 actionable comments total)

**Review 1 (22:20 UTC) — 7 comments:**
1. `world_logic.py 7063-7092`: `_inject_levelup_narrative_if_needed()` uses stale rewards_box — **FIXED** by commit 15d339fdf5
2. design-doc-as-contract.md grep paths need `mvp_site/` prefix
3. design-doc-gate.yml grep needs AST-based check
4. agents.py hasattr→isinstance for Mock avoidance
5. rewards_engine.py should_show_rewards_box duplicates level-up logic
6. rewards_engine.py normalize_child_mapping helper for Mock unwrapping
7. world_logic.py custom_campaign_state needs isinstance guard

**Review 2 (23:22 UTC) — 2 comments:**
1. `world_logic.py 1316-1318`: custom_campaign_state `.get()` needs isinstance guard (Major) — applies to 1341-1342, 1832-1839, 2370-2371, 4181-4184, 7075-7082, 7805-7806
2. `world_logic.py 1748-1756`: Remove "fresh signal bypass" — explicit-false stale guards should ALWAYS block (not bypassed by fresh XP signals)

### PR #6308 — 5 CHANGES_REQUESTED reviews (20+ comments)

Key themes: test skip comments, stale flag handling, skeptic-gate concurrency fix (in diff), CR not re-reviewing after fixes.

## Skeptic-Gate Concurrency Bug

Both `green-gate.yml` and `skeptic-gate.yml` use `group: green-gate-$PR_NUM` — the same concurrency group. When green-gate starts, it cancels in-progress skeptic-gate runs for the same PR. **Fix in PR #6308** (change to `skeptic-gate-$PR_NUM`) but PR #6308 itself is BLOCKED by CR.

## Connections
- [[LevelUpV4Architecture]] — PR #6276 core architecture
- [[BehavioralEquivalenceAudit]] — rev-v4ci05 finding: 0/3 pairs equivalent
- [[SkepticGate]] — concurrency bug, blocked by CR
- [[CodeRabbitIntegration]] — DISMISSED/CHANGES_REQUESTED patterns
