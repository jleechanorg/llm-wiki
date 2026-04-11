---
title: "PR #6184: fix(skeptic-gate): check only header section for VERDICT to prevent false PASS"
type: source
tags: []
date: 2026-04-10
source_file: raw/prs-worldarchitect-ai/pr-6184.md
sources: []
last_updated: 2026-04-10
---

## Summary
- Skeptic gate was reporting false PASS for PRs where Codex quota was exhausted
- Root cause: Codex session log echoes the full prompt, which contains `VERDICT: PASS — [one sentence...]` as a template example. The `grep -qi "VERDICT: PASS"` on the full comment body matched this template text
- Fix: extract only lines before `--- Full skeptic output ---` (the header section) before checking for VERDICT

## Metadata
- **PR**: #6184
- **Merged**: 2026-04-10
- **Author**: jleechan2015
- **Stats**: +8/-3 in 1 files
- **Labels**: none

## Connections
