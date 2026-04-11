---
title: "PR #5798: fix: expose ai_orch run defaults in top-level help"
type: source
tags: []
date: 2026-02-28
source_file: raw/prs-worldarchitect-ai/pr-5798.md
sources: []
last_updated: 2026-02-28
---

## Summary
- Add  support to ai_orch run parser (mutually exclusive with --no-worktree) and default to worktree mode.
- Add top-level help expansion when using usage: ai_orch [-h] [--version] {run,dispatcher,live,list,attach,kill} ...

AI Orchestration CLI (unified runtime + task dispatcher)

positional arguments:
  {run,dispatcher,live,list,attach,kill}
                        Commands
    run                 Run unified orchestration (orchestrate_unified
                        interface)
    dispatcher

## Metadata
- **PR**: #5798
- **Merged**: 2026-02-28
- **Author**: jleechan2015
- **Stats**: +529/-112 in 7 files
- **Labels**: none

## Connections
