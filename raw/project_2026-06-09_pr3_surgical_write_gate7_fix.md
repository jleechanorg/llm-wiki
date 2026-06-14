---
name: pr-3-surgical-write-gate7-fix
description: PR
metadata: 
  node_type: memory
  type: project
  originSessionId: 54224e21-8040-4407-a0e1-209703cd5b39
---

# PR #7370 (PR 3) — surgical level_up_session write to fix Skeptic Gate 7

**Date**: 2026-06-09
**Branch**: `feat/level-up-session-pr3`
**Head SHA**: `eb5f8701b33beab8ad3936cf4ce968dd221960bb`
**Pushed**: yes

## The fix

Skeptic Gate 7 (carried by CodeRabbit CHANGES_REQUESTED on `rewards_engine.py`
inline comment + the skeptic's bot consultation) flagged that the prior
implementation in `mvp_site/rewards_engine.py:canonicalize_rewards`:

```python
game_state_dict.clear()
game_state_dict.update(new_state)
```

preserves the root `dict` reference but **destroys reference identity for
every nested object** (e.g. `player_character_data` if any caller captured
a reference to it before canonicalization).

**Fix** (commit `eb5f8701b3`): surgical key write — write only
`level_up_session` (the only key the reducer output needs to land).

```python
new_session = new_state.get("level_up_session")
if isinstance(new_session, dict):
    game_state_dict["level_up_session"] = new_session
```

Also collapsed the suppression-gate nested-if into the outer guard
condition (ruff SIM102). 45 tests pass (test_level_up_session_atomic_persistence
+ test_level_up_session_state_machine_end2end + test_level_up_session).

## PR body updates

- Asciicast URL converted from Gist HTML page to raw direct file:
  `https://gist.githubusercontent.com/jleechan2015/c4fa950150e8873ec6ba4361ef7f4790/raw/level_up_atomicity_deterministic.cast`
- Evidence SHA refreshed from stale `263ff6e2d2` to current
  `eb5f8701b33beab8ad3936cf4ce968dd221960bb` with a note explaining the
  Gate 7 surgical-write refresh.
- `/skeptic` re-trigger posted.

## Skeptic worker fleet-wide down (Gate 7 not running)

`gh pr checks` reports all 4 PR chain PRs (PR 3, 4, 5.5, 6) with
Green Gate FAILing on step 8 "Poll for VERDICT" — external AO worker
consuming skeptic-cron's trigger is down. Re-triggered `/skeptic` on
all 4 PRs at 2026-06-09T02:25Z but verdicts may not return without
worker restart. See memory `project_2026-05-05_skeptic_worker_down_fleetwide_gate7.md`.

**Why**: Skeptic verdict on `ab1709d948` (Bugbot-fix head) at 2026-06-09T02:16Z
was FAIL on Gate 7 specifically because of the `clear()/update()` pattern.
Surgical fix removes the only technical blocker the existing skeptic
identified; the other FAIL gates (3, 5, 6, 8, 8a, 8c) are policy/evidence
gates, not correctness gates.

**How to apply**: When addressing CodeRabbit CHANGES_REQUESTED on a
rewards_engine.py change, check if the diff uses `clear()+update()` on
`game_state_dict` — replace with targeted key write.
