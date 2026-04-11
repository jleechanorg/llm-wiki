---
title: "PR #470: [P2] feat(agent-orchestrator): canonical AO config symlink (orch-2u9d)"
type: source
tags: []
date: 2026-04-02
source_file: raw/prs-worldai_claw/pr-470.md
sources: []
last_updated: 2026-04-02
---

## Summary
Implements beads **orch-2u9d**: `~/agent-orchestrator.yaml` must symlink to the canonical harness file `~/.openclaw/agent-orchestrator.yaml`, not to an arbitrary worktree `REPO_ROOT`, so the AO CLI and pollers always read the live config.

## Metadata
- **PR**: #470
- **Merged**: 2026-04-02
- **Author**: jleechan2015
- **Stats**: +62/-24 in 3 files
- **Labels**: none

## Connections
