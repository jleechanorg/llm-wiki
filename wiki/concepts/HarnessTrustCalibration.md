---
title: "Harness Trust Calibration"
type: concept
tags: [harness, verification, regression, calibration]
date: 2026-06-24
---

## Definition
**Harness Trust Calibration** is the discipline of measuring how often a
harness assertion (skill status string, contract hash, gate verdict, contract
test result) is correct, and adjusting the level of independent verification
the agent applies accordingly. A skill that emits correct status strings 99%
of the time deserves less verification overhead than a skill that emitted
"mem0 unavailable" falsely for 2 months.

## Why it matters
LLM agents default to trusting harness output because instructions say so
("report `X unavailable` if missing"). That default is fine when the harness
is well-maintained; it becomes a silent regression vector when the harness
drifts. Calibration surfaces the drift: track per-skill assertion accuracy
and increase verification on offenders.

## Calibration signals
- **Skill emits "X unavailable" / "X failed" / "X missing"** → verify by running X with a fixture.
- **Contract hash gate (e.g., prompt_tool_contracts.json sha256) green** → not enough; the gate proves the file changed, not that behavior was preserved. See [[PromptLoadBearingClause]].
- **CI gate passes** → check `gh pr checks` exit code is 0 (not just "ran"); prefer `/green <PR>` which enforces 7-green criteria.
- **Helper returns success silently** (e.g., `sys.exit(0)` in all paths) → outcome is unverifiable without an external probe. Pair with [[ContinuousVerification]].

## Fix pattern
- **Per-skill accuracy log** — track how often each skill's negative status string is wrong. Surface to the agent.
- **Default-verification rule** — for skills in the "low accuracy" tier, always verify before reporting. For high-accuracy skills, optionally verify.
- **Co-evolve skills with their mechanisms** — when a mechanism changes (PR #7178: OpenAI embedder → Ollama embedder), update the skill probe in the SAME PR. Add to PR template as a "Skill-staleness check" item.

## Canonical incident
2026-06-24: `/learn` SKILL.md had a 100%-wrong probe for ~2 months. No
calibration signal surfaced it. The user only discovered it by running the
helper directly with a fixture.

## Connections
- [[SkillStaleness]] — sibling concept; staleness is the failure mode, calibration is the discipline
- [[ContinuousVerification]] — operationalize calibration via contract tests
- [[EvidenceBasedVerification]] — generalize: every harness assertion backed by direct observation
- [[PromptLoadBearingClause]] — same calibration lesson: contract hash green ≠ behavior safe
