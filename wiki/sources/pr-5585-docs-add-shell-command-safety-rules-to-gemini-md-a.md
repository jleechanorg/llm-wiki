---
title: "PR #5585: docs: add shell command safety rules to GEMINI.md + Antigravity workflow"
type: source
tags: []
date: 2026-02-17
source_file: raw/prs-worldarchitect-ai/pr-5585.md
sources: []
last_updated: 2026-02-17
---

## Summary
Adds comprehensive shell command safety rules for **all** `git` and `gh` commands to prevent terminal hangs and enforce safe execution patterns.

### Problem
Commands like `gh pr comment --body '...'` and `git commit -m '...'` with multi-line strings cause terminal EOF detection failures, hanging commands indefinitely. This has been a recurring issue across multiple agent sessions (Gemini, Claude, and Antigravity).

### Changes

**`GEMINI.md`** — New "Shell Command Safety — Global Policy" sectio

## Metadata
- **PR**: #5585
- **Merged**: 2026-02-17
- **Author**: jleechan2015
- **Stats**: +78/-2 in 2 files
- **Labels**: none

## Connections
