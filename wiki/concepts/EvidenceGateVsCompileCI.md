---
title: "Evidence Gate vs Compile CI"
type: concept
tags: [CI, evidence-gate, compile, green-gate, skeptic]
last_updated: 2026-04-10
---

Red CI on many PRs while Test/Lint pass is often Evidence Gate (missing ## Evidence) or Skeptic 6-green gates — not broken builds.

## Two Conflicting Gate Names

Two workflows register the same check name "Skeptic Gate":
- skeptic-gate.yml (runs on PR open/update)
- skeptic-cron.yml (runs on schedule)

## Evidence Gate

PR body must contain `## Evidence` section. If absent, Evidence Gate fails.

## Fixes Needed

1. Add default PR template with ## Evidence section stub
2. Track bd-kkiq for rename/repair of duplicate gate name
3. Evidence Gate is PR-body CI, not unit tests — it's a structural check

## Connections

- [[EvidenceTheater]] — workers never produce real evidence
- [[SkepticGate]] — skeptic gate
- [[GreenGate]] — green gate CI
