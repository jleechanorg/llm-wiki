---
title: "Design Doc Gate Verification"
type: concept
tags: [design-doc, gate-verification, TDD, CLEAN-layer, architecture]
date: 2026-04-15
---

## Summary

Design doc gate verification is the practice of treating a design document as a **checkable acceptance contract** — not just documentation, but a verifiable specification with executable exit gates (typically grep commands or test assertions).

## Pattern

The design doc specifies:
1. Entry gate: prerequisites that must be met before starting
2. Exit gates: measurable criteria (grep counts, test results, line counts) that must ALL pass before claiming a phase/layer complete
3. The verification is done by an independent paranoid verifier agent, not by the implementer

## Example: Layer 3 CLEAN Exit Gates

From `level-up-engine-single-responsibility-design-2026-04-14.md`:

```
GATE 1: grep -c 'project_level_up_ui\|is_level_up_active' world_logic.py
         → Expected: 0 (ZERO public API calls)

GATE 2: grep -c 'def get_xp_for_level\|def get_level_from_xp' constants.py
         → Expected: 0 (DELETE duplicates)

GATE 3: sed -n '123,140p' agents.py  | wc -l
         → Expected: ≤3 lines (delegate, not inline)

GATE 4: grep -r 'def _is_state_flag_true' mvp_site/
         → Expected: 1 file (rewards_engine.py only)
```

## Why This Pattern Works

1. **Removes ambiguity**: "design says it should be clean" → "grep count = 0"
2. **Independent verification**: verifier checks gates, not implementer
3. **Prevents drift**: implementer cannot claim "done" when gates fail
4. **Evidence trail**: gate results prove compliance at merge time

## Connections

- [[DesignDocAsContract]] — skill for treating design docs as checkable contracts
- [[Harness5LayerModel]] — L1 constraint (design doc) + L4 verification
- [[LevelUpCodeArchitecture]] — v4 architecture this pattern is applied to
- [[PRWatchdog]] — cron job for monitoring PR review state

## Anti-Pattern: "Pragmatic Layer N"

When an implementation claims "pragmatic Layer 3" while gates fail, the design doc verification has been abandoned. The proper response is either:
1. Update the design doc gates to match what was actually implemented, OR
2. Implement to the stated gates
3. Never change interpretation mid-stream without updating the design doc

## Git Commit Pattern for Gate Verification

When claiming a layer/phase complete, the commit message MUST list each gate and its result:

```
feat(layer3): complete Layer 3 CLEAN

GATE 1: grep -c 'project_level_up_ui' world_logic.py = 0 ✓
GATE 2: grep -c 'def get_xp_for_level' constants.py = 0 ✓
GATE 3: _is_stale_level_up_pending = 3 lines ✓
GATE 4: grep -r '_is_state_flag_true' = 1 file ✓
CI: 7/7 PASS ✓
```