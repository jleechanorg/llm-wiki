---
title: "Level-up-session verified migration state (2026-06-13)"
type: source
tags: [levelup, migration, verified-state, worldarchitect, codex-cold-review, divergence-bug, immediate-commit, design-decision]
date: 2026-06-13
source_file: raw/project_2026-06-13_levelup_session_verified_migration_state.md
---

## Summary
Verified code audit of the level-up-session migration on `origin/main` @ `18aadc3c` (2026-06-13) that corrects three false carried-forward findings (file was not deleted, rev-74a8m was wrong, three PRs already resolved). Identifies the **two-writer split** (reducer vs `world_logic._build_level_up_session_update`) as the mechanical origin of divergence and supersedes the pending state machine with an **immediate-commit + session-as-record** northstar.

## Key Claims
- `level_up_session.py` EXISTS (916 lines), imported by `god_mode_level_up.py:30`, `rewards_engine.py:38`, `world_logic.py:112` — NOT deleted in #7447
- The "zero callers" claim for `.status` was a symbol-grep artifact; `.status` is the live routing signal via `_is_session_active`
- PR1 (reducer) only 2/8 writers wired; PR2 (finish-gate) not landed (clamp deliberately removed per comment 2944-2964); PR3 (preflight) not landed; PR4 (god-mode split) landed; PR5 (status read) partial; PR6 (cleanup) not landed
- **Two-writer split** (`world_logic._build_level_up_session_update` at `world_logic.py:2409` stamping `source="server"`) — not the abstract "move step" — is the mechanical origin of divergence
- New v2 design: immediate-commit + session-as-record; `player_character_data.level` is SOLE read-authority; `player_character_data + level_up_session` written in the SAME atomic op from the SAME response
- Inviolable rule kills divergence: session is the consolidated transaction record (from→to, applied changes, offered_choices, selections, source, review_open — NO 6-status machine)

## Key Quotes
> "Inviolable rule that kills divergence: player_character_data + level_up_session written in the SAME atomic op from the SAME response (never separately); player_character_data.level is the SOLE read-authority."

> "The MOVE STEP (pending→canonical) was the bug; deleting it eliminates finish-limbo/stuck-modal/divergence/atomic-pair at root."

> "M-B had an ERROR ('_build_level_up_session_update must run on both paths' = extend the 2nd writer to streaming = spreads divergence); CORRECTED to DELETE it + fold into reducer."

## Connections
- [[LevelUpSessionStateMachine]] — superseded by immediate-commit design
- [[TwoWriterDivergence]] — mechanical origin of split-brain
- [[CodexColdReview]] — `/fs dark-factory spec_gen` verdict FAIL on testability but design validated SOUND
- [[AtomicFirestoreWrite]] — sole-writer rule for player_character_data + level_up_session
- [[AOBeads]] — rev-74a8m false finding, br bead jleechan-cv3 referenced
