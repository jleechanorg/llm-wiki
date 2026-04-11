---
title: "PR #403: [agento] feat: prepend [agento] on gh pr create via hook updatedInput (bd-pfx)"
type: source
tags: []
date: 2026-04-11
source_file: raw/prs-worldai_claw/pr-403.md
sources: []
last_updated: 2026-04-11
---

## Summary
PR #403 implements bead `bd-pfx`: AO agent hooks should prepend `[agento]` to `gh pr create` titles instead of denying the command and forcing a retry. Reviewers found three concrete gaps in the original rewrite path: it failed open when safe parsing was not available, it mis-parsed `-t=<title>`, and it round-tripped commands through `shlex.join()`, which normalized shell text and could change quoting semantics.

## Metadata
- **PR**: #403
- **Merged**: 2026-04-11
- **Author**: jleechan2015
- **Stats**: +321/-53 in 3 files
- **Labels**: none

## Connections
