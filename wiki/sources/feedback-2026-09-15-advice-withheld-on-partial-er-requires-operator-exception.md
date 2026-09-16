---
title: "Advice Withheld on Partial ER Requires Operator Exception"
type: source
tags: [evidence-standards, advice, draft-first-pr, worldarchitect-ai]
date: 2026-09-15
source_file: raw/feedback_2026-09-15_advice_withheld_on_partial_er_requires_operator_exception.md
---

## Summary
In PR #9406 (worldarchitect.ai), four independent code reviewers (Gemini, ChatGPT, Codex, Opus) approved the changes and CI was 100% green. However, because original pre-edit failing output for backend RED had been lost during environment recovery, retrospective RED execution could not prove original pre-fix chronology. Per evidence standards, ER remained PARTIAL, requiring `/advice` to fail closed as WITHHELD. Merging was only authorized when the operator issued an explicit `MERGE APPROVED` with the documented PARTIAL-evidence exception.

## Key Claims
- Retrospective execution of RED reproducer tests does not establish original pre-fix chronology; ER must remain PARTIAL rather than being relabeled PASS.
- A 4-reviewer code approval quorum does not override missing evidence: `/advice` must fail closed as WITHHELD when ER is PARTIAL.
- Merging under a PARTIAL evidence state is strictly forbidden by default and requires explicit operator MERGE APPROVED with a documented exception.

## Key Quotes
> "Formal advice remains WITHHELD because ER/ES remains PARTIAL: original pre-edit failing output absent after scoped recovery. Retrospective RED does not replace original chronology." — Approval Bead Comment

## Connections
- [[EvidenceStandards]] — Strict chronological reproducer output requirements
- [[AdviceGateSynthesis]] — Fail-closed synthesis when evidence prerequisites fail
- [[DraftFirstPR]] — Merge boundaries and operator approval invariants
- [[WorldArchitectAI]] — Repository governance and PR lifecycle
