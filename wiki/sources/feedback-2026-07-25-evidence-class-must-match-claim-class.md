---
title: "Evidence Class Must Match Claim Class"
type: source
tags: [evidence, evidence-review, waitlist-gate, user-story, worldarchitect-ai]
date: 2026-07-25
source_file: raw/feedback_2026-07-25_evidence_class_must_match_claim_class.md
---

## Summary
During a 2026-07-25 session, a visual/user-story spec for worldarchitect.ai was audited four separate times by adversarial reviewers and scored WITH-GAPS every time — but all four rounds only reviewed the *documents*. When the documented claims were finally checked against 2,141 scenes of real campaign transcripts, four of them turned out to be flatly false. The root cause: 73 of 109 stories had acceptance criteria that are inherently BEHAVIORAL (require observing change across a sequence — streaming, transitions, cross-scene state deltas) rather than STATIC (settleable from a single frame or document read), and no round of review had produced any behavioral-class evidence at all.

## Key Claims
- Four adversarial document-review passes all converged on the same WITH-GAPS verdict without ever detecting that some of the underlying claims were untrue.
- Checking against real transcripts found: a "Gold never updates" claim was false (Gold actually took 6 distinct values, 75→7495 GP); a "~every 10 scenes" checkpoint-cadence claim was actually 489/490; an injury-behavior claim was contradicted by 0/400 and 1/697 sampled HP losses; and a disclaimer claiming a time contradiction was "not observed" was false — it is observed at scenes 458 and 466.
- Document review cannot structurally catch a well-formed, internally consistent claim that is simply untrue about the product, because the document is self-consistent on its own terms.
- The cheap check that would have caught this earlier: count how many acceptance criteria are behavioral vs static, then explicitly ask whether ANY behavioral-class evidence exists — not just repeat the same document review.

## Key Quotes
> "Document review structurally cannot catch a well-formed claim that is simply untrue about the product."

> "The docset had proven a third of itself and asserted the rest."

## Connections
- [[evidence-review-unscorable-axes-2026-06-05]] — same family of "evidence review passed but didn't prove the real claim" failure
- [[feedback-2026-06-05-evidence-review-unscorable-axes]]
- [[jleechanclaw-evidence-review-gate]] — the repo's gate machinery this failure mode evaded
- [[worldarchitect-ai]] — the product under audit
- [[verify-different-layer-than-claim-layer-2026-07-25]] — same session's generalized cross-layer verification lesson
