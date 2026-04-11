---
title: "Postmortem — 2026-03-19 — Smartclaw Routing / Delegation Failures"
type: source
tags: [smartclaw, delegation, routing, postmortem, incident, worldarchitect]
sources: []
source_file: "raw/smartclaw-routing-delegation-failures-postmortem.md"
last_updated: 2026-04-07
---

## Summary
A delegation flow intended for `jleechanorg/smartclaw` initially produced work in the wrong repo context (`jleechanorg/worldarchitect.ai`), then required corrective rerouting and tighter prompt constraints.

## Key Claims
- **Initial context mismatch**: Delegation prompt lacked explicit source/target repo contract, causing work to be done in wrong repository
- **No pre-PR validation**: No mandatory repo identity checks were enforced before first PR creation
- **Session contamination**: Session context became stale and anchored to wrong PR context
- **Corrective measures**: Added explicit SOURCE_REPO/TARGET_REPO headers, mandatory pre-PR checks, and fresh session resets

## Key Quotes
> "No cross-repo delegation without explicit SOURCE/TARGET contract."

> "No 'done' report without proof bundle: edited file paths, remote commit URL, PR URL."

> "Any repo mismatch triggers immediate stop + correction before continuing."

## Connections
- [[Smartclaw]] — target repository for the delegation
- [[Worldarchitect.ai]] — the repo where incorrect work was initially performed
- [[Jleechanclaw]] — source repository for delegation workflow
- [[Delegation Flow]] — the broken workflow pattern that was fixed

## Contradictions
- None identified
