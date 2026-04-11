---
title: "PR #5942: [agento] fix: CodeRabbit ping — Standardize bot naming and update progress bar rendering handle and post-only-after-push guardrail"
type: source
tags: []
date: 2026-03-14
source_file: raw/prs-worldarchitect-ai/pr-5942.md
sources: []
last_updated: 2026-03-14
---

## Summary
- **Comment-validation / PR monitor:** Use `@coderabbitai` (no hyphen). `@coderabbit-ai` does not notify the CodeRabbit bot.
- **`.claude/commands`:** `/coderabbit` and `/cr` post `@coderabbitai all good?` with guardrail: only run after pushing fixes for CodeRabbit comments; no timer-based ping.
- **Test:** `test_comment_validation` asserts `@coderabbitai` in body.

## Metadata
- **PR**: #5942
- **Merged**: 2026-03-14
- **Author**: jleechan2015
- **Stats**: +48/-394 in 8 files
- **Labels**: none

## Connections
