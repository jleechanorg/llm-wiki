---
title: "Prompt-cleanup PRs silently drop load-bearing LLM-instruction clauses (#7870 → #7903)"
type: source
tags: [zfc, prompt-engineering, code-review, worldarchitect, regression]
date: 2026-06-24
source_file: ../../raw/feedback_2026-06-24_prompt_cleanup_drops_load_bearing_clauses.md
---

## Summary
A WorldArchitect.AI "cleanup" PR (#7870) removed lines from `mvp_site/prompts/**`
that looked like backend/developer documentation. The review (mine) approved it as
behavior-preserving. Follow-up PR #7903 proved 3 of those removed lines were
load-bearing LLM-instruction clauses — including a HIGH-severity level-up
modal-lock exception — and restored all 3. Core lesson: under ZFC, prompt files
ARE the model's runtime instruction contract, so any prompt-line deletion is a
behavioral change requiring real-LLM regression proof, never reviewable as
"docs cleanup."

## Key Claims
- Every removed line in `mvp_site/prompts/**` is a behavioral contract change, not a doc edit. Default review stance: REMOVAL = REGRESSION until proven otherwise.
- Prompt deletions require real-LLM regression proof (Gate 8 real-mode smoke / `/es` real run), not unit/mock tests.
- The prompt-contract hash gate (`prompt_tool_contracts.json` version+sha256) proves the file changed — it does NOT prove behavior was preserved. Hash-match green ≠ behavior safe.
- Removing a clause can strand a dependent list item / numbered step that referenced it (orphaned-reference pattern).
- Level-up / modal-entry clauses are HIGH severity: dropping an exception clause silently re-locks the modal.

## Key Quotes
> "Under ZFC, prompt files ARE the LLM's instruction contract — the model reads them at runtime as its operating spec." — root cause of the review miss

> "The gate proves the file changed, it does NOT prove the behavior was preserved." — on prompt-contract hash gating

## Connections
- [[ZFCNorthStar]] — prompt-as-contract is a direct ZFC consequence (model owns decisions; prompt is the instruction surface)
- [[PromptComplianceDrift]] — removed clauses are a drift vector: model output silently changes when its instructions change
- [[PromptVersioning]] — version+sha256 contract bump caught the file change but not the behavioral regression
- [[Schema-PromptDrift]] — hash/schema sync ≠ behavioral preservation
- [[PromptEngineering]] — prompt deletions are LLM-behavior edits, reviewed as code not docs
- [[PromptLoadBearingClause]] — the concept this source establishes
