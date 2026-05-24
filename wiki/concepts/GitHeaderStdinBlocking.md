---
title: "Git Header Stdin Blocking"
type: concept
tags: [git, automation, non-interactive-shell, bash, troubleshooting]
---

A technical issue where executing `git-header.sh` in non-interactive background tasks or automated runners hangs indefinitely because the hook script performs a standard read / `cat` on standard input (stdin).

## Root Cause

The `git-header.sh` script (e.g. `~/.claude/hooks/git-header.sh`) is designed to capture current branch state and print a contextual metadata footer. In interactive shells, it works seamlessly. However, in automated orchestrator workers, background tasks, or subagents, standard input remains open, and calling `cat` inside the script causes it to wait indefinitely for input, leading to 5-minute task timeouts or hanging runs.

## Resolution Pattern

Always execute the git-header command with stdin closed or explicitly redirected to `/dev/null`:

```bash
# Stdin closed via redirection
bash git-header.sh --with-api < /dev/null
```

This prevents the script from waiting on interactive input and allows it to exit immediately with correct branch state output.

## Related

- [[OrchestrationGaps]] — systemic automation gaps in worker pipelines
- [[AutomatedTestingReliability]] — preventing CI pipeline and test suite hangs
