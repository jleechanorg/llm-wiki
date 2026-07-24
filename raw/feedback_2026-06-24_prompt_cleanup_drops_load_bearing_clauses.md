---
name: prompt-cleanup-prs-silently-drop-load-bearing-llm-instruction-clauses-7870
description: "In ZFC, every removed line in mvp_site/prompts/** is a behavioral contract change, not a doc edit; review must require real-LLM regression proof, never wave off as \"docs cleanup\""
metadata: 
  node_type: memory
  type: feedback
  bead: rev-f9ev9
  originSessionId: 119226a9-d30b-4b43-93af-9857792505eb
---

**Context (2026-06-24):** Reviewed PR [#7870](https://github.com/jleechanorg/worldarchitect.ai/pull/7870) (prompt "cleanup" sweep removing what looked like backend/developer documentation from `mvp_site/prompts/**`). I declared "behavioral preservation holds" and explicitly waved off the removal of a level-up modal-entry exception clause as "fine." #7870 was then merged.

**What was actually wrong:** Follow-up PR [#7903](https://github.com/jleechanorg/worldarchitect.ai/pull/7903) (merge commit `5be3aad61a`, "restore 3 load-bearing behavioral rules from #7870 sweep") proved **3 of the removed lines were load-bearing LLM-instruction clauses**, not docs:
- **Finding A** — `planning_protocol.md`: a dangling "Requires both `text` and `description`" bullet became orphaned; restored as a numbered "3. Choice Schema (Required)" rule.
- **Finding B (HIGH)** — `planning_protocol.md`: the level-up re-entry exception (`if level_up_pending=true and mechanics already selected → present finish_level_up_return_to_game to close the modal and avoid a lock`). Dropping it re-introduces a **modal lock** — a real user-facing regression.
- **Finding C** — `game_state_instruction.md`: item 7 documenting that omitting required faction suggestions force-routes to FactionManagementAgent next turn.

**Root cause of MY review miss:** I treated `mvp_site/prompts/**` edits as documentation diffs. Under **ZFC, prompt files ARE the LLM's instruction contract** — the model reads them at runtime as its operating spec. A clause that reads like "internal documentation of backend behavior" is frequently the *only* place the model is told to emit (or not emit) a specific affordance. Removing it changes model output.

**FIX / RULE (apply on every prompt-touching PR review):**
1. **Every removed line in `mvp_site/prompts/**` is a behavioral change.** Default stance: REMOVAL = REGRESSION until proven otherwise. Never approve prompt deletions as "docs cleanup," "non-behavioral," or "backend doc removal."
2. **Require real-LLM regression proof** for prompt deletions — the exact scenario the removed clause governed must be shown still working (Gate 8 real-mode smoke / `/es` real run), not unit/mock tests.
3. **Watch for orphaned/dangling references** — removing a clause can strand a list item or numbered step that pointed at it (Finding A pattern).
4. **Level-up / modal-entry clauses are HIGH severity** — they gate modal locks; dropping an exception clause silently re-locks the modal (Finding B).
5. This pairs with the existing prompt contract gate (`mvp_site/schemas/prompt_tool_contracts.json` version+sha256): the gate proves the *file changed*, it does NOT prove the *behavior was preserved*. Hash-match green ≠ behavior safe.

**Verification:** #7903 merged as HEAD of main; all 3 clauses restored; real-mode Gate 8 smoke PASS (run 28114213000, SHA f635c9a4 exact match), fresh skeptic PASS, `=== GREEN GATE: PASS ===` (run 28114932914). Contract hashes re-synced (game_state 1.1.42→1.1.43, planning_protocol 1.1.11→1.1.12).

**Reusable pattern:** ZFC prompt files = runtime instruction contract. A prompt-line deletion is never a documentation edit — it is an LLM-behavior change requiring real-LLM regression evidence. See [[feedback_2026-06-23_prompt_strip_pattern_merge_collision]] (removing a strip pattern is a latent collision class) and [[feedback_2026-06-22_prompt_loader_strip_point_reachability]] (prompt clause placed past a strip point = dead code).
