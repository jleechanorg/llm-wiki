---
title: "LevelUpBugEvidence"
type: concept
tags: [worldarchitect-ai, level-up, dice, rewards-box, bug-chain, evidence-map]
sources: []
last_updated: 2026-04-11
---

## Summary

This page maps all known evidence sources related to the level-up bug chain: beads, memory files, roadmap entries, and existing wiki pages. It identifies gaps where wiki coverage is missing.

## Bead Tracking

| Bead | Status | Finding |
|------|--------|---------|
| `jleechan-gw0u` | MERGED | PR #6195 critical rewards sentinel regression fix |
| `jleechan-xz0b` | OPEN | dice rolls missing for non-debug users (frontend debug gate) |
| `jleechan-orke` | OPEN | system message/warning emission path (separate from rewards) |
| `rev-ozgr` | MERGED | currency rewards setting-aware (PR #6150) |
| `rev-ldfd` | MERGED | level-up polling must project from canonical `rewards_pending` |
| `rev-xxsx` | MERGED | flash-lite model excluded from MODELS_WITH_CODE_EXECUTION → dice falls back |
| `rev-qcax` | MERGED | frontend `app.js:924` hides rewards box when `xp_gained=0` |

## Memory Files

| File | Content |
|------|---------|
| `project_2026-04-11_levelup_bug_chain.md` | 8+ PR chain (#6161→#6195→#6204), 3 root causes: structure drift, atomicity violations, debug-gating; sentinel contract |
| `project_2026-04-11_levelup_pr_chain.md` | 5 open PRs, #6195 critical blocker, merge order |
| `reference_2026-04-11_levelup_wiki_pages.md` | 15 concept + 5 entity + 96 source pages for level-up/dice system |
| `feedback_2026-04-11_system_msgs_not_rewards.md` | System messages are separate from rewards_box pipeline |

## Roadmap Entries (learnings-2026-04.md)

| Date | Finding |
|------|---------|
| 2026-04-11 | Level-up bug wiki: 4 new pages added |
| 2026-04-11 | PR #6179 merged (debug gate), but frontend still debug-gated for non-debug users |
| 2026-04-11 | 7 atomicity bugs in world_logic.py + green-gate `--jq`/`--paginate` pagination bug |
| 2026-04-09 | Level-up polling must project from canonical `game_state.rewards_pending`, not story-entry snapshots |
| 2026-04-09 | PR #6170 flash-lite excluded from MODELS_WITH_CODE_EXECUTION → dice silently falls back |
| 2026-04-08 | `app.js:924` `if (fullData.rewards_box && fullData.rewards_box.xp_gained > 0)` hides rewards when xp=0 |

## Existing Wiki Coverage

### Core Bug Chain Pages (complete)
- [[LevelUpBug.md]] — 8+ PR chain: #6161→#6179→#6193→#6195→#6196→#6204→#6165
- [[RewardsBoxAtomicity.md]] — 6 atomicity violations in rewards_box/planning_block
- [[DiceRollDebugRegression.md]] — 3-week regression window, backend payload emission hypothesis
- [[StructureDriftPattern.md]] — 5 fields nested inside rewards_box block, checkpoint PR #2162 root cause

### Supporting Concept Pages
- [[LevelUpStateManagement.md]] — stale flags: `level_up_in_progress`, `rewards_pending`
- [[LevelUpActiveStateLogic.md]] — REV-0g1y routing vs injection inconsistency
- [[LevelUpModalRouting.md]] — state machine routing with explicit False blocking
- [[LevelUpDetection.md]] — XP threshold trigger logic
- [[DiceRollingProtocol.md]] — code execution with random.randint(), DC before roll
- [[DiceRollsNormalization.md]] — legacy dice_rolls → mechanics.rolls migration
- [[RewardsBox.md]] — rewards_box JSON structure
- [[RewardsProcessedFlag.md]] — deferred rewards processing

### Entity Pages
- [[RewardsBoxBuilder.md]] — normalize_rewards_box_for_ui with has_visible_content sentinel
- [[LevelUpAgent.md]] — modal routing agent (REV-439p, REV-0g1y)

### Source Pages (PR coverage)
All key PRs have source pages: #6161, #6179, #6193, #6194, #6195, #6196, #6197, #6204, #6165

## Missing from Wiki

These findings from beads/memory/roadmap have NO wiki page yet:

| Finding | Status | Gap |
|---------|--------|-----|
| Level-up polling from canonical `rewards_pending` (rev-ldfd) | Not in wiki | Missing [[LevelUpPolling]] concept page |
| Flash-lite model excluded from MODELS_WITH_CODE_EXECUTION (rev-xxsx) | Not in wiki | Missing [[DiceProviderFallback]] concept page |
| Frontend `app.js:924` rewards gate `xp_gained > 0` (rev-qcax) | Not in wiki | Missing [[FrontendRewardsBoxGate]] concept page |
| Green-gate `--jq`/`--paginate` pagination bug (930ed371d6) | Not in wiki | Mentioned in PR #6161 bug hunt source, not a standalone page |
| System messages are separate from rewards_box (jleechan-orke) | Not in wiki | Missing [[SystemMessageEmissionPath]] concept page |

## Key Sentinel Contract

```python
normalize_rewards_box_for_ui({})  # returns None when no visible content
normalize_rewards_box_for_ui({"progress_percent": 50})  # returns normalized dict
```
If empty dict returns non-None → `_process_rewards_followup` silently skips all reward processing.

## Key Code Locations

- `mvp_site/world_logic.py:1387` — `_resolve_level_up_signal()`
- `mvp_site/world_logic.py:1457` — `_check_and_set_level_up_pending()`
- `mvp_site/world_logic.py:7071-7078` — stale planning_block bug
- `mvp_site/world_logic.py:7385-7400` — polling path atomicity bugs
- `mvp_site/world_logic.py:2759-2807` — false-positive level-up scrubbing
- `mvp_site/agents.py:1285` — LevelUpAgent
- `mvp_site/action_resolution_utils.py` — dice roll extraction
- `mvp_site/frontend_v1/app.js:924` — frontend rewards_box condition
- `mvp_site/constants.py` — MODELS_WITH_CODE_EXECUTION set

## Connections

- [[LevelUpBug]] — core bug chain page
- [[RewardsBoxAtomicity]] — atomicity invariant
- [[StructureDriftPattern]] — root cause of field nesting
- [[LevelUpStateManagement]] — stale flag bugs
- [[DiceRollDebugRegression]] — dice regression investigation
