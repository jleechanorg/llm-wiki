---
title: "world_logic.py:3594-3612 server synthesis path violates CLAUDE.md narrow-scope approval from PR #7064"
type: source
tags: [world-logic, level-up, server-synthesis, policy-violation, narrow-scope-drift, claude-md]
date: 2026-06-13
source_file: /Users/jleechan/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/project_2026-06-13_synthesis_path_scope_drift.md
---

## Summary
The server-side choice synthesis branch at `mvp_site/world_logic.py:3594-3612` injects a `finish_level_up_return_to_game` choice with `server_generated=True` and is a direct CLAUDE.md policy violation. PR #7064 only approved the narrow scope at `world_logic.py:3508-3525`; the synthesis path at 3594-3612 drifted 86+ lines below the approved boundary, and the code itself self-admits the policy violation. Bead `rev-sls86` (delete synthesis) is the fix.

## Key Claims
- CLAUDE.md forbids server-generated planning blocks by default; narrow exceptions must be registered in `mvp_site/backend_adjustment_specs.py` with category=CORRECTION, populated root_cause_status, evidence_refs, allowed_when, log_reason_code.
- The code's own comment at lines 3598-3600 self-admits: *"Per CLAUDE.md the synthesis path itself is policy-banned; this marker is the minimum-viable disclosure pending the deeper fix."*
- REPRO confirmed via twin entry reproduction on campaign mppfHseT9cy44Ywro4oJ with source offender k2sluTQNY8uGF9pOjthS (6 twin entries with identical `server_synth_reason`).
- The fix is a small PR: delete the `if _lu_modal_active:` synthesis branch at 3594-3612 entirely; the post-#7441 prompt already emits `finish_level_up_return_to_game` reliably.
- Do not ship any "prompt fix" that also leaves the synthesis path in place — synthesis is what makes the phantom level_up_session state user-visible.

## Key Quotes
> "The server-side choice synthesis at `mvp_site/world_logic.py:3594-3612` injects a `finish_level_up_return_to_game` choice with `server_generated=True, server_synth_reason='modal_finish_repair_level_up'`."

> "PR #7064 (2026-05-25, modal-sealing review) approved `server_generated=True` ONLY at `world_logic.py:3508-3525` for the canonical `finish_level_up_return_to_game` choice (W1 in the review). The current synthesis path is at `3594-3612` — 86+ lines below the approved scope."

## Connections
- [[LevelUpModalRouting]] — the synthesis path is the root cause of phantom level-up agent appearance
- [[PR7064]] — the narrow-scope approval that this code has drifted outside
- [[BackendAdjustmentSpecs]] — required registry for any server-generated planning block exception
- [[RevSls86]] — the bead for deleting the synthesis path
- [[LevelUpPolling]] — related modal-routing context that does not touch synthesis
