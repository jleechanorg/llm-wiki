---
title: "ZFC Loop Current-Head Comment Gate — 2026-04-21"
type: source
tags: [zfc, loop, supervision, pr-gates]
date: 2026-04-21
source_file: raw/2026-04-21-zfc-loop-current-head-comment-gate.md
---

## Summary

The level-up ZFC loop supervision failed closed too weakly on PR `#6431`: the standard GitHub check surface looked green, but a real-E2E smoke failure comment still existed on the PR head SHA. The worker lane did not reconcile that contradiction before disappearing. The durable rule is that current-head `/smoke`, `/er`, and bot-failure comments outrank green-check optimism and block worker parking.

## Key Claims

- A PR can look green in `statusCheckRollup` while still carrying unresolved current-head gate debt in issue comments.
- PR `#6431` had a real smoke failure at issue comment `4291382771` tied to head SHA `c1a865d68c38aef2b02a252f8d4bfb7c0fefedcd`.
- Worker lifecycle accounting must treat unresolved current-head comment-gate debt as active work, not review-only or done.
- The supervision loop must update its own roadmap/memory/wiki artifacts when this class of mistake is found.

## Key Quotes

> “The smoke comment is real for `#6431`. It is not a stale main-line artifact. It explicitly names PR head `c1a865d68c38aef2b02a252f8d4bfb7c0fefedcd`.” — loop investigation, 2026-04-21

> “The worker did go wrong, in the sense that it failed to finish reconciliation of a real current-head smoke failure on `#6431`.” — loop diagnosis, 2026-04-21

## Connections

- [[Level-Up ZFC Loop Postmortem]] — earlier postmortem on loop supervision gaps
- [[Stage-0-Execution-Drift]] — another case where apparent progress diverged from roadmap truth
- [[ZFC Level-Up Model Computes Design]] — canonical roadmap context for the affected PR stack
