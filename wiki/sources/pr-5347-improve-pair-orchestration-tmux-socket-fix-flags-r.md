---
title: "PR #5347: Improve /pair orchestration: tmux socket fix, flags, resilience"
type: source
tags: []
date: 2026-02-12
source_file: raw/prs-worldarchitect-ai/pr-5347.md
sources: []
last_updated: 2026-02-12
---

## Summary
- **Fix critical tmux socket mismatch** - Monitor can now find agent sessions on custom orchestration sockets
- **Add --model and --no-worktree flags** - Passthrough to orchestrate_unified.py for both agents
- **Change default verifier from codex to claude** - Codex fails with vpython/rate-limit issues
- **Add agent startup crash detection** - Read crash logs instead of silent failure

**Key themes:**
- Resilience improvements based on real pair session failures
- All changes are backwards-compa

## Metadata
- **PR**: #5347
- **Merged**: 2026-02-12
- **Author**: jleechan2015
- **Stats**: +618/-54 in 5 files
- **Labels**: none

## Connections
