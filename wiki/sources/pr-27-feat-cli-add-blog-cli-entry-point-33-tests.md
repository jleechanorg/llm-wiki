---
title: "PR #27: feat(cli): add blog-cli entry point + 33 tests"
type: source
tags: []
date: 2026-03-29
source_file: raw/prs-/pr-27.md
sources: []
last_updated: 2026-03-29
---

## Summary
The living blog design doc (`docs/plans/2026-03-27-living-blog-refactor-design.md`) describes a `blog-cli` command router as the primary CLI surface for AO workers. Previously, the only CLI was `src/novel/cli.ts` which calls the novel engine directly. This PR implements `src/cli/main.ts` — a typed, testable entry point that covers all 5 commands from the design doc.

## Metadata
- **PR**: #27
- **Merged**: 2026-03-29
- **Author**: jleechan2015
- **Stats**: +752/-0 in 3 files
- **Labels**: none

## Connections
