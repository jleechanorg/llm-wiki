# Conclude/Finalize Prompt ZFC Design + Dark Factory Setup (2026-05-30)

**Source type:** session learning (/learn)  **Repo:** worldarchitect.ai  **Bead:** rev-di0g2

## Summary
Design + Dark Factory pipeline for a unified conclude/finalize prompt (level-up + character-creation) that lets the model own the canonical commit + cascade derived-stat reconciliation, replacing PR #7175's backend override (Path B). Plus durable infra learnings.

## Key learnings
1. **Dark Factory holdout guarantee is about the CODER, not the orchestrator** — the runner's `claude --print` codergen subprocess is the blind party; the orchestrator may author `holdouts/<feature>/scenarios.yaml` (dark-factory SKILL.md:106-114). Evaluator schema: `python_call` / `python_call_signature` / `python_module_attr`, exact-repr match, module imported from impl_root.
2. **@prompts false-PASS** — `runner/handlers.py:550 _path_attr` joins a relative prompt path to `ctx.workdir` (target repo), not the runner tree; codergen degrades to a stub but scores success. Fix: absolute prompt paths in the `.dot`; verify with an `--backend echo --max-steps 3` smoke.
3. **ZFC conclude thesis** — god-mode reliability = model-owned commit + blanket reconcile mandate + worked JSON + output contract; backend force-override of a model-owned field is an anti-pattern that hides prompt bugs (3 research lanes / 6+ models unanimous). Keep only a warn-only logged invariant; re-ask is streaming-incompatible.
4. **`commit_expected_level_from_xp` (rewards_engine.py:3191) is already step-1 ZFC** — preserves a model-set level; only steps 2-3 + `level_up_in_progress` force-flips (world_logic.py:2482/2610/2756) are the override → staged deletion after real-LLM proof.
5. **Agent routing by flow-state flags is legitimate**, not banned ZFC keyword routing; the conclude signal selects the prompt PHASE within the already-selected domain agent.
6. **secondo "Not authenticated"** = wrapper didn't export `VITE_AI_UNIVERSE_FIREBASE_*` for silent idToken refresh; fixed.
7. **New `/llm-testing`** real-LLM zero-mock command+skill; wired into `/testing-layers` + `/4layer`.

Related: [[DarkFactory]] [[ZeroFrameworkCognition]] [[jeffrey-oracle]] (not affected)
