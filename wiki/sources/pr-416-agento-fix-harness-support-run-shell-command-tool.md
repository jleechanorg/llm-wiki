---
title: "PR #416: [agento] fix(harness): support run_shell_command tool name (Gemini CLI)"
type: source
tags: []
date: 2026-04-11
source_file: raw/prs-worldai_claw/pr-416.md
sources: []
last_updated: 2026-04-11
---

## Summary
PR https://github.com/jleechanorg/agent-orchestrator/pull/416 extends the metadata-updater hook so Gemini CLI shell calls are treated the same as Claude shell calls. Review on the original change uncovered two regressions in the same hook: the `PreToolUse` `gh pr merge` deny path became unreachable, and plain `git checkout <branch>` stopped updating branch metadata. This update keeps the Gemini compatibility goal while restoring the harness behavior that `origin/main` already enforced.

Supersed

## Metadata
- **PR**: #416
- **Merged**: 2026-04-11
- **Author**: jleechan2015
- **Stats**: +2/-2 in 1 files
- **Labels**: none

## Connections
