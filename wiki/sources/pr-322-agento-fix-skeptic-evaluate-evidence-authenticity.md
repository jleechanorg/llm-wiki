---
title: "PR #322: [agento] fix(skeptic): evaluate evidence authenticity by default — remove N/A escape hatch (bd-7x6y)"
type: source
tags: []
date: 2026-03-31
source_file: raw/prs-worldai_claw/pr-322.md
sources: []
last_updated: 2026-03-31
---

## Summary
`packages/cli/src/commands/skeptic/prompt.ts` rule 10 previously said:

> "Evidence review is required only when config requires it; default is N/A."

This meant skeptic **never evaluated evidence quality** unless `evidenceRequired=true` in config (off by default). PRs with fabricated or placeholder evidence passed skeptic without scrutiny.

## Metadata
- **PR**: #322
- **Merged**: 2026-03-31
- **Author**: jleechan2015
- **Stats**: +68/-2 in 2 files
- **Labels**: none

## Connections
