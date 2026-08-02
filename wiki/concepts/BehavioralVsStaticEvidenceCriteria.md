---
title: "Behavioral vs Static Evidence Criteria"
type: concept
tags: [evidence, evidence-review, testing, methodology]
date: 2026-07-25
---

## Definition
A distinction for classifying acceptance criteria (in a user-story spec, test plan, or evidence bundle) by what kind of proof can settle them:

- **Static criteria** — settleable from a single artifact: one screenshot, one document read, one log line. Example: "the button label says Continue."
- **Behavioral criteria** — require observing a change across a sequence: streaming behavior, state transitions, cross-scene/cross-turn consistency, timing. Example: "Gold updates as the campaign progresses," "the checkpoint cadence holds across many scenes," "no time-contradiction appears across the session."

## Why it matters
A docset or review process can look thorough (multiple adversarial rounds, high pass rates) while only ever having produced STATIC-class evidence. If a large fraction of the claims are actually BEHAVIORAL, the process has proven only the static subset and asserted the rest without ever gathering the evidence that would settle it — and repeated re-review of the same documents cannot fix this, because the documents are internally consistent regardless of whether they're true.

## Incident
2026-07-25, worldarchitect.ai user-story audit: four adversarial review rounds scored a spec WITH-GAPS each time. Checking the underlying claims against 2,141 scenes of real campaign transcripts found four claims that were simply false (a "Gold never updates" gap, a checkpoint-cadence claim, an injury-behavior claim, and a false "not observed" disclaimer about a time contradiction that IS observed at scenes 458/466). Measured: 73 of 109 stories in the spec had BEHAVIORAL acceptance criteria; the docset had no behavioral-class evidence at all for most of them.

## How to apply
Before trusting any evidence docset: count criteria by class (behavioral vs static). If a criterion is behavioral, require evidence of an actual observed sequence/change (real transcripts, video, streaming logs) — a document review or single-frame screenshot cannot substitute. See [[feedback-2026-07-25-evidence-class-must-match-claim-class]].

## Related
- [[BehavioralEquivalenceAudit]] — related but distinct: auditing whether two implementations behave equivalently, not whether a claim about behavior is even measurable
- [[evidence-review-unscorable-axes-2026-06-05]]
- worldarchitect.ai repo rule: "Unit-only proof is NOT sufficient" (`~/.claude/CLAUDE.md`) — the same failure shape applied to document/spec review instead of test layers
