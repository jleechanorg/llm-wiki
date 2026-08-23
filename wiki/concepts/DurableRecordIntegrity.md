---
title: "Durable Record Integrity"
type: concept
tags: [verification, evidence, memory, learnings, anti-pattern]
date: 2026-08-18
last_updated: 2026-08-18
---

## Definition

The property that persisted knowledge artifacts — learnings logs, agent memory
files, roadmap docs, bead descriptions, PR bodies — accurately reflect the state
of the world at the time a later reader consults them. Durable records outrank
the evidence that contradicts them, because the reader typically sees the record
and not the evidence.

## Why it is a distinct failure class

A wrong durable record is not the same as a wrong answer in conversation. A
conversational error is corrected in the next turn; a durable error is read
weeks later by an agent with no context, treated as settled, and used to skip
work or misattribute symptoms. The blast radius grows with time rather than
shrinking.

## Observed failure modes

- **False "Fixed"** — a fix is recorded as landed when only an adjacent PR from
  the same workstream shipped. See
  [[feedback-2026-08-18-learnings-entry-claimed-a-fix-that-never-landed]].
- **Fabricated statistics** — numbers written into a PR body or evidence bundle
  that were never queried.
- **Stale-by-design** — a record that was true when written and is silently
  false now, with no expiry or re-verification hook.

## Verification rules

1. Before writing "Fixed", "Deployed", "Enabled", or "Complete" into any durable
   artifact, verify against the authoritative layer — grep the default branch for
   the mechanism, not the PR title; confirm the tracking bead/issue is closed.
2. Before building on someone else's durable "Fixed", apply the same check.
3. When correcting a durable record, append a correction and preserve the
   original text verbatim — see [[capture_provenance]]. Do not rewrite history.
4. Prefer recording the *verification command and its output* alongside the
   claim, so a later reader can re-run it.

## Related

- [[VerifyBeforeReporting]]
- [[capture_provenance]]
- [[AdversarialVerifyPipeline]]
