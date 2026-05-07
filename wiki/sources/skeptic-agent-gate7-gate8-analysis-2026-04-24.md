---
title: "Skeptic Agent Gate 7 + Gate 8 Analysis — 2026-04-24"
type: source
tags: [skeptic, agent-orchestrator, gate, verification, llm-evaluation]
date: 2026-04-24
source_file: skeptic-prompt.ts-2026-04-24
---

## Summary

The skeptic agent IS designed to validate PR description/goals/tenets against code and evidence/tests. Goals has the strongest explicit enforcement (Rule 12). Gate 8 covers tenets/scope but without a dedicated deterministic parser. Key implementation lives in `skeptic/prompt.ts` with Rule 11 (design alignment) and Rule 12 (goals verification).

## Key Claims

- **Gate 7 (prompt.ts:172)**: Technical review of "behavior, tests, and merge readiness" — the LLM-enforced technical gate
- **Gate 8 (prompt.ts:174)**: "PR description goals, scope, tenets, diff, and evidence must agree" — the alignment gate
- **Rule 12 (prompt.ts:190)**: Deterministic Goals-section parser — extracts ## Goals bullets, fails if any goal has NO corresponding diff evidence. Tests-only goals for feature/bugfix are NOT satisfied (tests prove behavior, not create it)
- **skeptic-gate-8 marker (prompt.ts:211)**: Machine-readable marker required for "PR description goals/tenets/scope vs code/evidence alignment"
- **Rule 11 (prompt.ts:139)**: Design alignment — verifies code diff aligns with design doc and PR description claims (11a-11f)
- **skeptico.ts:268**: Builds prompt from PR metadata + diff + reviews + design doc + merge gate state, then sends to LLM
- **skeptic-structured-output.test.ts:259**: Tests locking in the Goals-section prompt behavior

## Key Quotes

> "Gate 7: Technical review of behavior, tests, and merge readiness" — skeptic prompt.ts:172

> "Gate 8: PR description goals, scope, tenets, diff, and evidence must agree" — skeptic prompt.ts:174

> "If the PR description contains a '## Goals' or '## Goal' section with bullet or numbered items: 12a. Extract each bullet/numbered item from the Goals section; 12b. For each goal bullet, verify there is diff evidence; 12c. FAIL if any goal bullet has NO corresponding implementation in the diff" — skeptic prompt.ts:160-164

> "For feature/bugfix goals, a goal with only test changes is NOT implemented (tests prove behavior, not create it). Goals explicitly about adding or updating tests CAN be satisfied by test changes." — skeptic prompt.ts:165

> "A goal about documentation only requires doc changes — no code changes needed" — skeptic prompt.ts:166

## Implementation Gap

**"Tenets" and "Scope" get Gate 8 wording but NO dedicated deterministic parser** equivalent to Rule 12's Goals extraction. If a PR has a `## Tenets` section with no corresponding diff evidence, it is NOT deterministically caught the way missing ## Goals bullets are.

The gap: Gate 8 calls out tenets/scope alignment but Rule 12 only explicitly handles Goals. A tenets-only PR would pass Rule 12 (skip, since no Goals section) even if tenets were completely absent from the diff.

## How to Verify

```bash
# Source files:
grep -n "Gate 7\|Gate 8\|Rule 12\|skeptic-gate-8\|Goals-section" \
  ~/projects/agent-orchestrator-skeptic-wt/packages/cli/src/commands/skeptic/prompt.ts

# Test locking Goals behavior:
grep -n "Goals" \
  ~/projects/agent-orchestrator-skeptic-wt/packages/cli/src/__tests__/skeptic/skeptic-structured-output.test.ts
```

## Connections

- [[agent-orchestrator]] — parent project
- [[skeptic-agent]] — the agent being analyzed
- [[self-critique-verification-loop]] — technique for description→code→test tracing (relevant enhancement)
- [[product-judge]] — evaluator separation principle (relevant enhancement)
- [[canonical-code-scorer]] — type safety enforcement (relevant enhancement for Gate 4/Bugbot)
