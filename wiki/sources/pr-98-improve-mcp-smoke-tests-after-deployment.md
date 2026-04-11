---
title: "PR #98: Improve MCP smoke tests after deployment"
type: source
tags: [codex]
date: 2025-10-01
source_file: raw/prs-/pr-98.md
sources: []
last_updated: 2025-10-01
---

## Summary
- harden the MCP smoke test runner with retries, timeouts, and extra result validation
- extend the PR preview workflow to wait for preview health, manage smoke test status, and surface results in PR comments
- add an npm alias so the deployment workflow can invoke the smoke tests directly

## Metadata
- **PR**: #98
- **Merged**: 2025-10-01
- **Author**: jleechan2015
- **Stats**: +805/-177 in 8 files
- **Labels**: codex

## Connections
