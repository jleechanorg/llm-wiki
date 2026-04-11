---
title: "PR #35: chore(beads): create bd-q9n + bd-pdt epics, close rate limit fixes"
type: source
tags: []
date: 2026-03-20
source_file: raw/prs-worldai_claw/pr-35.md
sources: []
last_updated: 2026-03-20
---

## Summary
GitHub GraphQL API rate limit (5000/hr) was fully exhausted. Root causes: PR poller making ~85 REST calls/cycle on 21 capped PRs, plus 15 agent sessions burning GraphQL. Fixed by closing stale PRs and optimizing the poller (in jleechanclaw repo).

Also created bd-pdt epic tracking 12 runtime gaps between jleechanclaw orchestration and AO.

## Metadata
- **PR**: #35
- **Merged**: 2026-03-20
- **Author**: jleechan2015
- **Stats**: +18/-0 in 1 files
- **Labels**: none

## Connections
