---
title: "PR #65: fix: Add CodeRabbit ping commands (Add Claude command definitions for CodeRabbit review workflows all good?, post-only-after-push)"
type: source
tags: []
date: 2026-03-25
source_file: raw/prs-worldai_claw/pr-65.md
sources: []
last_updated: 2026-03-25
---

## Summary
- Add `.claude/commands/coderabbit.md` and `cr.md` so agents can trigger CodeRabbit re-review with the correct handle and guardrails.
- **Exact comment:** `@coderabbitai all good?` (GitHub handle is coderabbitai, no hyphen).
- **Guardrail:** Run only after pushing fixes for CodeRabbit comments; do not run on a timer (avoids spam/duplicates).

## Metadata
- **PR**: #65
- **Merged**: 2026-03-25
- **Author**: jleechan2015
- **Stats**: +65/-0 in 2 files
- **Labels**: none

## Connections
