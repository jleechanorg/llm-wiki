---
title: "Skill Staleness"
type: concept
tags: [harness, verification, regression]
date: 2026-06-24
---

## Definition
A **skill** (`SKILL.md`, command prompt, or any markdown instruction set loaded
into a LLM agent) is **stale** when its embedded status-string logic, env-var
gates, or example commands no longer match the behavior of the mechanism they
document. Skills are written once and read many times; mechanisms drift
(constants renamed, providers swapped, dependencies upgraded). The skill text
becomes a hypothesis generator, not a ground-truth source.

## Why it matters
Agents are trained to follow instructions. When a skill says "report `X
unavailable` if `Y` env var is missing," the agent emits that string and the
downstream user treats it as ground truth. If the mechanism stopped checking
`Y` six months ago, the agent has been silently misreporting for the entire
gap. The failure is invisible because no test catches it — the skill text and
the agent output agree, both wrong.

## Detection pattern
1. Skill emits a negative status string ("X unavailable because Y is missing").
2. Agent dutifully reports it.
3. **User or next agent trusts the string without running X directly.**
4. Reality: X works fine; the probe is stale.

## Fix pattern
- **Probe = mechanism's own gate, not what the mechanism USED TO gate on.**
- **Mandatory verification step**: invoke X directly with a fixture and
  observe the outcome before reporting "X unavailable."
- **Contract test**: skill ships a test that runs the mechanism with the
  fixture the skill expects, and asserts the status string matches.
- **CLAUDE.md rule**: treat any "X unavailable" / "X failed" string a skill
  emits as a hypothesis, not a fact.

## Canonical incident
2026-06-24: `/learn` SKILL.md probed `OPENAI_API_KEY` / `MEM0_API_KEY` and
falsely reported "mem0 unavailable" for ~2 months after PR #7178 switched mem0
to local Ollama embedder + Groq LLM. Direct invocation with a Stop-hook
fixture proved mem0 worked (508 points in Qdrant `hermes_mem0`). The skill's
probe was the bug; the helper was fine.

## Connections
- [[HarnessTrustCalibration]] — measure skill-claim accuracy; calibrate trust
- [[ContinuousVerification]] — pair skills with contract tests
- [[EvidenceBasedVerification]] — generalize: every harness assertion needs direct observation
- [[PromptLoadBearingClause]] — sibling failure: trusting contract hash green instead of verifying behavior
