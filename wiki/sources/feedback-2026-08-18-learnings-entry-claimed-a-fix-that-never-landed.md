---
title: "A learnings entry claimed a fix that never landed (2026-08-18)"
type: source
tags: [durable-records, verification, evidence, worldarchitect, telemetry, false-fixed-claim]
date: 2026-08-18
sources:
  - "~/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-08-18_learnings_entry_claimed_a_fix_that_never_landed.md"
source_file: raw/feedback_2026-08-18_learnings_entry_claimed_a_fix_that_never_landed.md
last_updated: 2026-08-18
---

## Summary

On 2026-08-18 a session recorded in `~/roadmap/learnings-2026-08.md` that
worldarchitect.ai's mature-campaign prompt bloat had been fixed, claiming a 65%
token reduction (~317k → ~110k) and citing PR #9060 as merged. Verification the
same day showed the claim was false: PR #9060 shipped only the debug-mode cache
hit-rate *display*, while the actual deduplication fix was absent from
`origin/main` and its tracking bead/issue remained open. The failure mode is
specific and repeatable — two different PRs from the same workstream, one that
shipped and one that fixes, conflated in the durable record.

## Key Claims

- A durable "Fixed" claim was written for work that never reached the default
  branch; the cited PR shipped an adjacent display feature, not the fix.
- Verification method that caught it: grep `origin/main` for the fix
  *mechanism* (`god_mode.description` filtering, `story_history[0]` excision),
  not the PR title — both were absent.
- Corroborating signal: the tracking bead `rev-fl4z6` and issue #9061 were both
  still OPEN, contradicting the "Fixed" claim.
- Damage model: the learnings file is what the next agent reads to decide what
  is already done. A false "Fixed" is worse than no entry, because it causes the
  real work to be skipped and remaining symptoms to be misattributed.
- Correction was applied by appending a marker while preserving the original
  text verbatim, per the never-rewrite-historical-logs rule.

## Key Quotes

> "Fixed via prompt serialization filtering ... slashing tokens by 65%
> (~317k -> ~110k) and restoring >75% implicit cache hit rates" — the original
> learnings claim, contradicted by `origin/main`

> "A merged PR in the same workstream is not proof the fix landed." — the
> reusable rule extracted from the incident

## Connections

- [[DurableRecordIntegrity]] — the class of defect: a persisted claim that
  outlives and outranks the evidence contradicting it
- [[VerifyBeforeReporting]] — the general rule this instantiates for the
  specific case of "Fixed" claims
- [[capture_provenance]] — why the original text was preserved rather than
  rewritten when correcting
- [[CampaignBibleDuplication]] — the underlying prompt-bloat problem that was
  falsely reported as solved
- [[GeminiImplicitCachePrefixMeasurement]] — the measurement context in which
  the false claim was made
- [[AdversarialVerifyPipeline]] — the verification posture that catches this
  class before it is written
