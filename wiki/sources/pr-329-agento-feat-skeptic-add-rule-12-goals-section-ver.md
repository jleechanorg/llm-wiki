---
title: "PR #329: [agento] feat(skeptic): add Rule 12 goals section verification"
type: source
tags: []
date: 2026-03-31
source_file: raw/prs-worldai_claw/pr-329.md
sources: []
last_updated: 2026-03-31
---

## Summary
Adds Rule 12 to the skeptic prompt (buildSkepticPrompt in packages/cli/src/commands/skeptic/prompt.ts) that systematically verifies each bullet in the PR Goals section against the diff.

- Rule 12a-12e: Extract each Goals bullet, check for corresponding implementation in diff, FAIL if none
- 12b: verify diff evidence including code, config, workflow, or other non-doc changes
- 12d: for feature/bugfix goals, test-only changes don't count; goals explicitly about adding tests CAN be satisfied by te

## Metadata
- **PR**: #329
- **Merged**: 2026-03-31
- **Author**: jleechan2015
- **Stats**: +118/-3 in 2 files
- **Labels**: none

## Connections
