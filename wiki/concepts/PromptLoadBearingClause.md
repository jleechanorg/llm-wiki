---
title: "Prompt Load-Bearing Clause"
type: concept
tags: [zfc, prompt-engineering, code-review, regression]
date: 2026-06-24
---

## Definition
A **load-bearing clause** is any line in an LLM prompt file (`mvp_site/prompts/**`)
that the model reads at runtime as part of its operating instructions and that
changes model output if removed. Under [[ZFCNorthStar]] (Zero-Framework Cognition),
prompt files ARE the model's instruction contract — not developer documentation —
so the distinction between "a doc comment" and "a behavioral instruction" inside a
prompt file is unreliable. The safe default is: **treat every prompt line as
load-bearing until proven otherwise.**

## Why it matters
Lines in a prompt that *read like* internal documentation of backend behavior are
frequently the only place the model is told to emit (or suppress) a specific
affordance. Removing such a line silently changes runtime behavior with no code
diff to flag it.

## Review rules
1. **Removal = regression until proven otherwise.** Never approve prompt-line
   deletions as "docs cleanup," "non-behavioral," or "backend doc removal."
2. **Require real-LLM regression proof** for prompt deletions — the exact scenario
   the clause governed must be shown still working via a real run (Gate 8 real-mode
   smoke / `/es`), not unit/mock tests.
3. **Watch for orphaned references** — removing a clause can strand a dependent
   numbered step or list item that pointed at it.
4. **Modal-entry / level-up clauses are HIGH severity** — dropping an exception
   clause can silently re-lock a modal (user-facing regression).
5. **Hash gate ≠ behavior gate.** The prompt-contract gate
   (`prompt_tool_contracts.json` version+sha256) proves the file changed; it does
   NOT prove behavior was preserved. See [[PromptVersioning]], [[Schema-PromptDrift]].

## Canonical incident
PR #7870 (a prompt "cleanup" sweep) removed 3 load-bearing clauses — including a
level-up modal-lock exception — that were approved on review as behavior-preserving.
PR #7903 ("restore 3 load-bearing behavioral rules from #7870 sweep", merge
`5be3aad61a`) restored all 3, verified by real-mode Gate 8 smoke + Green Gate PASS.

## Connections
- [[ZFCNorthStar]] — prompt-as-contract is a direct ZFC consequence
- [[PromptComplianceDrift]] — removed clauses are a drift vector
- [[PromptVersioning]] — version bump caught the file change, not the regression
- [[Schema-PromptDrift]] — hash/schema sync ≠ behavioral preservation
- [[PromptEngineering]] — prompt deletions are code-level behavior edits
