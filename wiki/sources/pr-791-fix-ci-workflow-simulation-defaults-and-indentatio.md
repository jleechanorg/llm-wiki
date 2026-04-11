---
title: "PR #791: Fix CI workflow simulation defaults and indentation"
type: source
tags: [codex]
date: 2025-11-21
source_file: raw/prs-/pr-791.md
sources: []
last_updated: 2025-11-21
---

## Summary
- keep CI integration job using `CI_SIMULATION=true` so model calls stay stubbed
- restore indentation of the stub MCP heredoc to maintain valid YAML
- drop the unused matrix guard from the monitoring validation step

## Metadata
- **PR**: #791
- **Merged**: 2025-11-21
- **Author**: jleechan2015
- **Stats**: +233/-97 in 3 files
- **Labels**: codex

## Connections
