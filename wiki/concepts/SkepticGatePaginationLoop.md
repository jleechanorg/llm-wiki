---
title: "Skeptic Gate Pagination Loop Bug"
type: concept
tags: [CI, skeptic, pagination, bug, green-gate]
last_updated: 2026-04-11
---

Skeptic-gate Gate-5 had unbounded pagination loops — PRs with >100 review threads could loop forever.

## Root Cause

Copilot kept adding pagination without bounding it.

## 6 Commits to Fix

1. `bbc783a3` — bound loops
2. `0442f040` — add MAX_PAGES=50 guard
3. `0b561b7e` — add cursor validity guard
4. `30189c66` — paginate threads for >100 threads
5. `d872c056` — fail closed when PR author lookup fails
6. `940a398b` — skip GQL loop when lookup fails

## Pattern

Pattern: copilot fighting same atomicity bug across 6+ consecutive commits without bounding the loop from the start.

## Also Found

green-gate pagination bug `930ed371d6` — `--jq` incompatible with `--paginate` on multi-page review results.

## Connections

- [[SkepticGate]] — skeptic-gate workflow
- [[GreenGate]] — green-gate CI
- [[EvidenceGate]] — evidence-gate workflow
