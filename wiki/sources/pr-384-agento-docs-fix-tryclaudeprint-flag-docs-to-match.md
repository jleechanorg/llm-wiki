---
title: "PR #384: [agento] docs: fix tryClaudePrint flag docs to match implementation"
type: source
tags: []
date: 2026-04-05
source_file: raw/prs-worldai_claw/pr-384.md
sources: []
last_updated: 2026-04-05
---

## Summary
Fixes documentation mismatches flagged by CodeRabbit CR on PR #383:

- `tryCodexPrint` described as `codex --print --no-input` but implementation uses `codex exec -` via stdin
- `tryClaudePrint` described as `claude --print --no-input` but implementation uses `--dangerously-skip-permissions --print` via stdin-pipe
- All four doc lines updated to match actual `packages/cli/src/lib/llm-eval.ts` implementation

## Metadata
- **PR**: #384
- **Merged**: 2026-04-05
- **Author**: jleechan2015
- **Stats**: +4/-4 in 2 files
- **Labels**: none

## Connections
