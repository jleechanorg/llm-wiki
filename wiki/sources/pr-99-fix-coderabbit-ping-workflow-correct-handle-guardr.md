---
title: "PR #99: fix: CodeRabbit ping workflow — correct handle, guardrails, docs"
type: source
tags: []
date: 2026-03-12
source_file: raw/prs-worldai_claw/pr-99.md
sources: []
last_updated: 2026-03-12
---

## Summary
- **CodeRabbit re-review ping:** Use exact handle `@coderabbitai all good?` (no hyphen; `@coderabbit` / `@coderabbit-ai` do not notify the bot).
- **Guardrails:** Post only after pushing fixes for CodeRabbit comments; do not ping on a timer to avoid spam/duplicates.
- **Docs:** `docs/coderabbit-ping-workflow.md` documents correct behavior and diagnosis.
- **Commands:** `.claude/commands/coderabbit.md` and `cr.md` added with correct text and guardrails.

## Metadata
- **PR**: #99
- **Merged**: 2026-03-12
- **Author**: jleechan2015
- **Stats**: +590/-0 in 8 files
- **Labels**: none

## Connections
