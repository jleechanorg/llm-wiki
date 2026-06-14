---
name: world-logic-3594-3612-synthesis-path-is-outside-pr-7064-narrow-scope-approval-2026-06-13
description: The server-side choice synthesis in mvp_site/world_logic.py:3594-3612 is a direct CLAUDE.md policy violation — PR 7064 only approved the narrow scope at world_logic.py:3508-3525. Rev-sls86 (delete synthesis) is the fix.
metadata: 
  node_type: memory
  type: project
  originSessionId: d1aebe53-e51d-44c5-b70a-9457f99fbcc2
---

**Finding (2026-06-13 /repro on campaign mppfHseT9cy44Ywro4oJ):**

The server-side choice synthesis at `mvp_site/world_logic.py:3594-3612` injects a `finish_level_up_return_to_game` choice with `server_generated=True, server_synth_reason="modal_finish_repair_level_up"`. This is what surfaces the "levelup agent appears for no reason" symptom — the LLM emits a phantom `level_up_session` (current_level=target_level=20, source=model, source_story_id="unknown") and the synthesis path then synthesizes a finish choice against the phantom state.

**Why this is policy-banned (not just a code smell):**

CLAUDE.md states: "Server CANNOT inject/synthesize choices by default. Narrow exceptions allowed only if registered in `mvp_site/backend_adjustment_specs.py` with `category=CORRECTION`, populated `root_cause_status`, `evidence_refs`, `allowed_when`, and `log_reason_code`. Any `server_generated=True` planning_block that is not covered by a registered, active spec is a bug. Registry-listing does not waive the long-term goal of removing the synthesis through prompt-first fixes."

The code's own self-admission at lines 3598-3600: *"Per CLAUDE.md the synthesis path itself is policy-banned; this marker is the minimum-viable disclosure pending the deeper fix (delete synthesis, force prompt to emit the choice)."*

**The narrow-scope drift:**

PR #7064 (2026-05-25, modal-sealing review) approved `server_generated=True` ONLY at `world_logic.py:3508-3525` for the canonical `finish_level_up_return_to_game` choice (W1 in the review). The current synthesis path is at `3594-3612` — 86+ lines below the approved scope. **The narrow-scope approval has drifted; this is no longer a narrow exception, it is a different synthesis path entirely.**

**Evidence (twin REPRO confirmed):**

- Source offender: `k2sluTQNY8uGF9pOjthS` (campaign mppfHseT9cy44Ywro4oJ, owner vnLp2G3m21PJL6kxcuAqmWSOtm73, 750 story entries)
- Twin: 6 entries with identical `server_synth_reason` after copy+align+replay
- Evidence bundle: `/tmp/worldarchitect.ai/feat_god-mode-level-override/repro-7364-redrive-2/`
- Verdict: `REPRO` (not `RELATED` or `NON-REPRO`)

**How to apply:**

- DO NOT ship any "prompt fix" that ALSO leaves the synthesis path in place. The synthesis path is what makes the phantom state user-visible.
- When you see `server_generated=True` in any planning_block, check the `server_synth_reason` and the line range. If it's outside 3508-3525 in `world_logic.py`, it is a policy violation and must be reported immediately.
- The fix is a small PR: delete the `if _lu_modal_active:` synthesis branch at 3594-3612 entirely. The prompt (post-#7441) already emits `finish_level_up_return_to_game` reliably.
- For deeper work, also tighten the prompt to forbid `state_updates.custom_campaign_state.level_up_pending=True` unless `target_level > player_character_data.level` is a real signal (CLAUDE.md level-up signal contract).

**Beads:**
- `rev-sls86` — Delete world_logic.py:3594-3612 server synthesis path (P1, OPEN)
- `rev-7k8yw` — Fix phantom level_up_session creation (P1, OPEN, blocked-by rev-sls86)
- `rev-tcssz` — Issue 7364 (the original symptom bead, related)

**Related memories:**
- `project_2026-06-12_levelup_8of8_fleet_closeout.md` — the merge train that does NOT address the synthesis
- `project_2026-06-11_level_up_canonical_routing_fix.md` — canonical session routing; does not touch synthesis
- `project_2026-06-12_pr_readiness_minimum_gates.md` — 6 gates before any "ready" claim; the synthesis-path finding is what made me re-check the 6 gates
