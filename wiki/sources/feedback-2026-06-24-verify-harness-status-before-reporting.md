---
title: "\"X unavailable\" status strings are hypotheses, not facts (2026-06-24)"
type: source
tags: [harness, verification, skills, worldarchitect, mem0, regression]
date: 2026-06-24
source_file: ../../raw/feedback_2026-06-24_verify_harness_status_before_reporting.md
---

## Summary
The `/learn` SKILL.md probe checked `OPENAI_API_KEY` / `MEM0_API_KEY` and
falsely reported "mem0 unavailable" for ~2 months after the Ollama+Groq switch
in PR #7178 (May 2026). Mem0 itself worked perfectly — direct invocation with
a Stop-hook fixture persisted to Qdrant (`hermes_mem0`, user_id=jleechan,
count=508) and markdown. The skill's negative status string was a hypothesis,
not a fact. Fix: treat any "X unavailable" / "X failed" status a skill emits as
a hypothesis to verify by running the mechanism directly with a fixture, not
by trusting the literal status string.

## Key Claims
- Skill status strings ("X unavailable", "X failed") are **hypotheses**, not facts — skills get stale; helpers get rewritten; env-var gates referenced in SKILL.md can be from a previous config era.
- The mem0 probe in `/learn` SKILL.md predated the Ollama+Groq switch (PR #7178 / bead `rev-1cmaj`); it falsely reported "unavailable" until fixed 2026-06-24.
- Real mem0 availability gates: (1) `python3 -c "from mem0 import Memory"` resolves, (2) helper script exists at `~/.hermes/.claude/hooks/mem0_save.py` (or repo-local fallback), (3) `mem0_config.py:mem0_hooks_enabled()` returns True.
- General CLAUDE.md rule now in `~/.claude/CLAUDE.md` "Verify before reporting": run the underlying mechanism with a fixture before reporting "X unavailable" to the user.
- The fix has two layers: rewrite SKILL.md probe to use helper's own gate, AND add a CLAUDE.md rule that any negative status string must be verified.

## Key Quotes
> "Skills get stale; helpers get rewritten; env-var gates referenced in SKILL.md can be from a previous config era. Before reporting `X unavailable` to the user, invoke X directly with a fixture and observe the outcome." — general CLAUDE.md rule

> "Helper script > skill text. Reality > skill text." — reusable pattern

## Connections
- [[PromptLoadBearingClause]] — same root cause: trusting the harness (contract hash green / SKILL.md status string) instead of verifying reality
- [[EvidenceBasedVerification]] — generalize: every harness assertion should be backed by direct mechanism observation
- [[SkillStaleness]] — skills encode assumptions about their target mechanisms; mechanisms drift; probe gates must be co-evolved
- [[HarnessTrustCalibration]] — measure how often a skill's negative output is wrong; calibrate trust accordingly
- [[ContinuousVerification]] — skills that emit status strings should ship contract tests that assert the mechanism matches the status
