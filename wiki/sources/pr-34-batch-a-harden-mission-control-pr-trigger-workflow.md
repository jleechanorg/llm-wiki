---
title: "PR #34: Batch A: harden Mission Control PR trigger workflow"
type: source
tags: []
date: 2026-03-04
source_file: raw/prs-worldai_claw/pr-34.md
sources: []
last_updated: 2026-03-04
---

## Summary
- add concrete GitHub Actions workflow for `@jleechanclaw` PR comment triggers at `.github/workflows/agent-pr-fix-trigger.yml`
- enforce trusted-actor gate (`OWNER`/`MEMBER`/`COLLABORATOR`) and PR-only guard before self-hosted execution
- harden payload creation and API invocation with `jq` JSON construction, no `xargs`, and `curl --fail-with-body`
- codify Batch A policy decisions in `docs/mcp-mail-openclaw-mission-control-design.md` (source-of-truth defaults, CodeRabbit quorum fallback, eviden

## Metadata
- **PR**: #34
- **Merged**: 2026-03-04
- **Author**: jleechan2015
- **Stats**: +480/-0 in 4 files
- **Labels**: none

## Connections
