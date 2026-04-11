---
title: "PR #6076: [agento] ci(skeptic): align Skeptic Gate and cron with agent-orchestrator"
type: source
tags: []
date: 2026-04-02
source_file: raw/prs-worldarchitect-ai/pr-6076.md
sources: []
last_updated: 2026-04-02
---

## Summary
- Replace `.github/workflows/skeptic-gate.yml` and `skeptic-cron.yml` with canonical AO templates
- Skeptic Gate: `workflow_dispatch`, `cancel-in-progress: false`, 6-green pre-check, `statuses:read` permissions, `set +e` polling, exit-code error detection
- Skeptic Cron: `workflow_dispatch`, docs-only skip, 6-green filter, SHA-marked trigger comments, `--admin` merge, TOCTOU protection, pagination-aware GraphQL

Closes #6069

🤖 Generated with [Claude Code](https://claude.com/claude-code)

<!-- C

## Metadata
- **PR**: #6076
- **Merged**: 2026-04-02
- **Author**: jleechan2015
- **Stats**: +456/-250 in 2 files
- **Labels**: none

## Connections
