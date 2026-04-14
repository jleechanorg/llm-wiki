---
title: "Independent Verification"
type: concept
tags: [independence, model-family, dispatcher, verdict-json, evidence-review, stage2]
last_updated: 2026-03-16
sources: [jleechanclaw-evidence-review-schema]
---

## Summary
Independent verification in the two-stage evidence pipeline means a stage-2 reviewer from a different AI model family than the coding agent examines the evidence bundle and renders a verdict. The independence guarantee is enforced by the dispatcher (not the reviewer) writing `model_family_differs_from_stage1` and `independence_verified` into `verdict.json`.

## The Independence Problem

A coding agent that can self-review and self-attest creates a rubber-stamp problem. Stage 1 self-review is useful for the agent to catch its own mistakes before claiming done, but stage 2 must be genuinely independent to provide meaningful assurance.

## How Independence Is Enforced

The dispatcher (the orchestration code that runs the stage-2 reviewer) is the independence enforcer, not the reviewer itself:

1. **Dispatcher picks the reviewer** based on model family priority (Codex first, then Gemini, then Claude as fallback)
2. **Dispatcher compares model families** — knows which model ran stage 1, picks a different one for stage 2
3. **Dispatcher writes the attestation fields** in `verdict.json`:
   - `independence_verified: true` — set because the dispatcher verified the reviewer's identity
   - `model_family_differs_from_stage1: true` — set because the dispatcher compared families

A compromised or colluding stage-2 reviewer cannot forge these fields because it only produces `independent_review.md` text. The dispatcher parses that text and controls what goes into `verdict.json`.

## Model Family Priority Chain

| Stage 1 model | Stage 2 priority |
|---|---|
| Claude (Anthropic) | Codex (OpenAI) → Gemini (Google) |
| Codex (OpenAI) | Gemini (Google) → Claude (Anthropic) |
| Gemini (Google) | Claude (Anthropic) → Codex (OpenAI) |

Codex is preferred for stage 2 when stage 1 used Claude (different family, strong coding capability).

## What Stage 2 Checks

For each claim in `claims.md`:
- Does an artifact in `artifacts/` support this claim?
- Are there circular citations (claim cites itself)?
- Are there empty/missing artifacts?
- Are there statistical weaknesses (cherry-picked numbers)?
- Are there unverified assertions?

## What Stage 2 Cannot Do
- Stage 2 reviewer cannot see the coding agent's session or context
- Stage 2 reviewer works only from the evidence bundle (claims + artifacts)
- Stage 2 reviewer writes `independent_review.md` — the dispatcher parses this and writes `verdict.json`

## Why Not Just Stage 2?

Stage 1 self-review is valuable because:
- Catches agent's own mistakes before claiming done
- Reduces back-and-forth cycles
- Agent fixes issues in the same session (max 3 iterations)
- Stage 2 independent review is the gatekeeper, but stage 1 is the first filter

Without stage 1, every failure would go to stage 2, creating unnecessary independent review overhead for fixable issues.

## Related Concepts
- [[TwoStageEvidencePipeline]]
- [[MergeReadinessContract]]
- [[AutonomousAgentLoop]]