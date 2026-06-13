---
title: "Level-Up Canonical Session Routing Fix (2→3 multi-level)"
type: source
tags: [project, level-up, routing, modal, agents, zfc, worldarchitect]
date: 2026-06-11
source_file: raw/project_2026-06-11_level_up_canonical_routing_fix.md
---

## Summary
The `multi_level_organic_progression` daily-cron RED "Expected to finish at level 3, got level 2" was traced to a routing state-machine drift, NOT a ZFC enforcement violation. The modal lock at `agents.py:3351-3358` only consulted the **legacy** `custom_campaign_state.level_up_*` flags, missing the canonical `level_up_session` state machine. The 3-change fix in commit `317189350c` routes to the correct agent (LevelUpAgent) by consulting the canonical session, preserving the top-level `level_up_session` through the modal envelope, and re-exporting `is_session_active()` from `rewards_engine`. 8 new tests pass; 419 total tests pass.

## Key Claims
- Root cause: routing picked `agent_mode='combat'` because the modal lock at `agents.py:3351-3358` did NOT fire on the canonical `level_up_session.status == 'in_progress'`
- The LLM correctly wrote `level: 3`; the bug was that the SAFETY NET (`block_unauthorized_level_mutations`) reverted the legitimate level write because routing chose the wrong agent
- Per schema, `level_up_session` is the authoritative current-state machine; `custom_campaign_state.level_up_*` are DEPRECATED derived outputs
- This is a **routing state-machine fix** — the LLM still owns the decision of WHAT value to write; the routing just needs to pick the right agent
- Modal envelope `_filter_level_up_non_finish_state_changes` must preserve the top-level `level_up_session` for cross-turn routing
- NOT a ZFC violation because the LLM correctly wrote `level: 3` — the fix routes to the agent that has authority to commit the change

## Key Quotes
> "Turn N+6 (2→3 modal entry): LLM emits `state_updates.level_up_session={status: in_progress, target_level: 3, current_level: 2}` AND `custom_campaign_state.level_up_in_progress=true`. Routing picked `agent_mode='combat'`. Modal envelope **stripped** the `level_up_session` field."

> "Turn N+7 (2→3 modal finish): LLM correctly wrote `state_updates.player_character_data.level=3` in `finalize_level_up` response. But routing STILL picked `agent_mode='combat'` ... The modal lock at `agents.py:3351-3358` did NOT fire."

> "This is a **routing state-machine fix** — consulting the canonical `level_up_session.status` to decide which agent to invoke. The LLM still owns the decision of WHAT value to write; the routing just needs to pick the right agent that has authority to commit it."

## Connections
- [[multi-level-organic-progression-real-root-cause]] — earlier investigation, wrong framing
- [[stale-level-up-complete-cleared-2to3]] — earlier (reverted) backend enforcement attempt that Stop hook caught as wrong-layer
- [[NFBaxQ3mIUe17UlAAGlE level 5/6 bug]] — LLM prompt defect, NOT backend override (different class of bug)
- [[LevelUpRouting]] — concept of routing state-machine for level-up
- [[CanonicalSessionState]] — `level_up_session` as authoritative state machine
- [[ZeroFrameworkCognition]] — ZFC principle: backend enforcement forbidden without explicit human approval
- [[agents.py]] — file with modal lock at line 3348-3362
- [[rewards_engine.py]] — file with `is_session_active()` re-export
- [[world_logic.py]] — file with `_filter_level_up_non_finish_state_changes` modal envelope
- [[PR_7434]] — the PR that contains this fix
