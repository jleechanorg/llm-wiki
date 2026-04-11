---
title: "PR #2306: Handle temporal warnings when retries disabled"
type: source
tags: [codex]
date: 2025-12-03
source_file: raw/prs-worldarchitect-ai/pr-2306.md
sources: []
last_updated: 2025-12-03
---

## Summary
- return temporal correction prompt string directly to satisfy linting
- skip legacy temporal warning text when retries are disabled, since anomalies are surfaced via `god_mode_response`

## Metadata
- **PR**: #2306
- **Merged**: 2025-12-03
- **Author**: jleechan2015
- **Stats**: +61/-17 in 1 files
- **Labels**: codex

## Connections
