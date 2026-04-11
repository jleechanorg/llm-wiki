---
title: "PR #5873: fix(statusline): two-line status with context bar and clickable PR URL"
type: source
tags: []
date: 2026-03-08
source_file: raw/prs-worldarchitect-ai/pr-5873.md
sources: []
last_updated: 2026-03-08
---

## Summary
- Line 1: git info \`[Dir | Local | Remote | PR:#N]\` truncated to terminal width to prevent wrap
- Line 2: always-shown context progress bar (\`ctx ██████░░░░ 60%\`) with green/yellow/orange/red color coding
- Line 3: plain PR URL for native terminal hyperlink detection (OSC 8 stripped by statusline renderer)
- Simplify \`statusLine.command\` to \`exec\` directly (removes fragile python3 stdin buffering)

## Metadata
- **PR**: #5873
- **Merged**: 2026-03-08
- **Author**: jleechan2015
- **Stats**: +34/-19 in 2 files
- **Labels**: none

## Connections
