---
title: "PR #154: [agento] fix(party): disband single-member party when leader removes themselves"
type: source
tags: []
date: 2026-03-30
source_file: raw/prs-worldai_claw/pr-154.md
sources: []
last_updated: 2026-03-30
---

## Summary
When a party has only 1 member (the leader) and `removePlayer` is called, the party is now automatically disbanded instead of returning `false`. Leaders with other members are still protected from being removed.

## Metadata
- **PR**: #154
- **Merged**: 2026-03-30
- **Author**: jleechan2015
- **Stats**: +77/-12 in 2 files
- **Labels**: none

## Connections
