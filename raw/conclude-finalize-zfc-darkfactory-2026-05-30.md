---
name: conclude-finalize-prompt-zfc-design-level-up-char-creation-path-b-replaces
description: Shared conclude prompt phase lets the model own canonical commit + cascade reconcile; staged deletion of the backend override; warn-only invariant only
metadata: 
  node_type: memory
  type: project
  bead: none
  originSessionId: a75c29a5-871d-4eac-a1a6-8a9ccc953834
---

Design + plan + Dark Factory run authored 2026-05-30 (branch `fix/conclude-finalize-prompt` from HEAD). Replaces PR #7175 (Path B). Do NOT merge until human MERGE APPROVED.

**Thesis:** God-mode reliably "fixes everything" because `god_mode_instruction.md:185-223` gives the model (a) free-form state_updates ownership, (b) a blanket reconcile/CASCADE mandate, (c) worked JSON examples, (d) a final output contract silencing competing wording. The organic level-up CONCLUDE turn instead relies on a backend force-override = the inverse of ZFC. Fix = a shared conclude PROMPT PHASE (not a backend lock) so the model owns the canonical level commit + derived-stat reconciliation.

**Research basis** (3 lanes / ~15 frameworks / 6+ models, unanimous): a backend force-override of a model-owned field is an anti-pattern that HIDES prompt bugs — fix the prompt at root cause; keep only a warn-only logged invariant (Guardrails AI `NOOP` / event-sourcing replay-audit), never a silent override. Constrained decoding is a poor fit for value correctness ("structure ≠ semantics"); strong fits are parse-then-reduce (LangGraph reducers) + validate-and-reask. Re-ask is streaming-incompatible and our streaming path is primary, so the proving-window guard is warn-only, NOT re-ask. No new framework dep (we own Pydantic + constants + backend_adjustment_specs registry).

**Key code facts:**
- `commit_expected_level_from_xp` (`rewards_engine.py:3191`) is ALREADY partially ZFC: step 1 preserves a model-set `player_character_data.level`; only step 2 (rewards_pending fallback) + step 3 (XP-table derivation) + the `level_up_in_progress=True` force-flips (`world_logic.py:2482/2610/2756`) are the override. **Staged deletion:** make the conclude prompt always hit step 1 (proven via real-LLM `/llm-testing`), THEN steps 2-3 + force-flips become dead code and are removed. Not a blind override — a fallback chain.
- Agent routing is legitimate state-based routing (NOT banned ZFC keyword routing): domain agent chosen by `level_up_in_progress`/`character_creation_in_progress`; the conclude SIGNAL (finish-choice id in `_level_up_exit_choices`, or FastEmbed `classify_level_up_exit_intent`/`classify_cc_exit_intent`) selects the PROMPT PHASE within the already-selected agent and forces the correct domain agent on finish. ALL LLM interaction stays through an agent — no agent-less prompt assembly. ("never on which agent / stays ZFC" was a wrong earlier framing.)
- Prompt composition: no `@`-include in `prompts/`; agents compose via `REQUIRED_PROMPT_ORDER` + `agent_prompts.py` PATH_MAP. True reuse = one `_conclude_core.md` referenced by both LevelUpAgent + CharacterCreationAgent conclude-phase orders.
- No derived-stat tables exist yet (`constants.py` has only `XP_TABLE_5E:638`); reducer must be built once and shared. `AdjustmentSpec` is a frozen dataclass (`backend_adjustment_types.py:91`); specs are declared but NOT yet consumed at runtime → the warn-only emitter is net-new. FastEmbed exit classifier already exists (`intent_classifier.py:1267`).

**Artifacts:** `docs/superpowers/specs/2026-05-30-conclude-end-prompt-design.md`, `docs/plans/2026-05-30-conclude-finalize-prompt.md` (TDD, /testing-layers), `spec/conclude-finalize.md` (14 ACs), `pipelines/factory/conclude_finalize.dot` (2 phases + 2 review nodes). Sealed holdout: `dark-factory-holdouts/holdouts/conclude-finalize/scenarios.yaml`.

Related: [[feedback_2026-05-30_dark_factory_holdout_orchestrator_vs_coder]], [[reference_2026-05-30_llm_testing_command]], [[feedback_2026-05-26_story_milestone_vs_mechanical_level]].
