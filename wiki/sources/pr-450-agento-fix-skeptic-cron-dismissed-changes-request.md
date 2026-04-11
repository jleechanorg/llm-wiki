---
title: "PR #450: [agento] fix(skeptic-cron): dismissed CHANGES_REQUESTED no longer satisfies CR gate"
type: source
tags: []
date: 2026-03-30
source_file: raw/prs-worldai_claw/pr-450.md
sources: []
last_updated: 2026-03-30
---

## Summary
A dismissed CodeRabbit `CHANGES_REQUESTED` review does not mean the issues were resolved — it means the review was hidden. The previous CR gate logic only checked the latest review state, so a `DISMISSED` or `COMMENTED` review after a dismissed `CHANGES_REQUESTED` could incorrectly pass the gate without a fresh `APPROVED`.

Fixes [orch-n0l](https://github.com/jleechanorg/jleechanclaw/issues?q=is%3Aissue+orch-n0l).

## Metadata
- **PR**: #450
- **Merged**: 2026-03-30
- **Author**: jleechan2015
- **Stats**: +21/-8 in 1 files
- **Labels**: none

## Connections
