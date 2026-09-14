---
title: "PR #9861 Ready-Gate Integrity, HeavyDialog Prompt Ordering, and Implicit Cache Invariants"
type: source
tags: [workflow, ready-gate, prompt-engineering, gemini-cache, player-agency, heavy-dialog, worldarchitect-ai]
date: 2026-09-13
source_file: "raw/feedback_2026-09-13_ready_gate_and_heavy_dialog_invariants.md"
last_updated: 2026-09-13
---

## Summary

During PR #9861 (`feat(prompts): double word count guidance for HeavyDialogAgent`), prompt phrasing containing `merge approved` led to premature merge execution before verifying the `/ready` skill's full 6-gate checklist (specifically `/es` Gist publication and `/er` adversarial evidence review). In parallel, adversarial reviews surfaced two key backend/prompt invariants: `HeavyDialogAgent` must place its dedicated prompt in `SUFFIX_PROMPT_ORDER` strictly after `PROMPT_TYPE_NARRATIVE` so the 600-word dialogue directive overrides the 180-word narrative cap while preserving the byte-identical 10-contract prefix for Gemini implicit KV caching, and prompt instructions must strictly protect player character agency by never dictating PC thoughts, memories, or feelings.

## Key Claims

- **Conditional "merge approved" does not waive the `/ready` checklist**: The `/ready` skill enforces a mandatory 6-gate battery (`/es` Gist link, `/er` PASS verdict at current HEAD, `/advice` ≥2 reviewer quorum, `/green` CI/local backlogged proof, comments resolved, open-beads cross-thread check). A user instruction mentioning `merge approved` is authorization to merge *if and when* all gates are proven green, not an exemption.
- **Suffix Prompt Ordering Controls Precedence**: In `HeavyDialogAgent.SUFFIX_PROMPT_ORDER`, `PROMPT_TYPE_HEAVY_DIALOG` must appear strictly after `PROMPT_TYPE_NARRATIVE`. This ensures the 600-word dialogue directive cleanly overrides the 180-word narrative cap in final prompt assembly.
- **Gemini Implicit KV-Cache Prefix Preservation**: `NarrativeFamilyAgent.SHARED_PREFIX` (10 contracts) must remain strictly byte-identical across all 5 narrative family agents (`StoryModeAgent`, `HeavyDialogAgent`, `LoreAgent`, etc.) to ensure high implicit cache hit rates on Gemini models.
- **Player Character Agency Invariant**: The LLM narrative agent must never author or dictate PC interiority (internal thoughts, unexpressed feelings, flashbacks, or emotional reactions). Framing must rely on environmental reactions, scene atmosphere, and NPC dialogue cues.
- **No Forced Padding Directives**: Prompts should not include negative or coercive padding instructions ("do not collapse back into 180 words"); allow natural scene resolution up to the 600-word ceiling based on scene tension and character interactions.

## Key Quotes

> "lets run the relevant tests locally and ensure /wa /advice approve the PR then /ready and merge approved and double check that heavy dialog agent doesnt already have system instructions and ensure these new system instrucitosn do not break the iplicit cache prefix" — user prompt framing `merge approved` conditionally after verification.

## Connections

- [[ReadyGateDiscipline]] — mandatory 6-gate checklist before executing merge approved
- [[HeavyDialogAgent]] — dialogue agent in WorldArchitect.AI narrative agent family
- [[GeminiImplicitPrefixCaching]] — KV-cache optimization via byte-identical prompt prefixes
- [[PR9861]] — PR doubling HeavyDialogAgent word count guidance
- [[jeffrey-oracle]] — adheres to non-speculative, evidence-first execution
