---
title: "Hook Robustness Patterns"
type: concept
tags: [claude-code, hooks, best-practices, system-safety]
sources: [tdd-tests-claude-settings-hook-validation]
last_updated: 2026-04-08
---

Robust hook patterns are configuration practices that prevent system lockouts caused by environment variable dependencies. Key patterns include:

1. **Bash Wrapper Pattern**: Use `bash -c` with git resolution instead of direct `$ROOT` variable usage
2. **Skip Auto-Generated Files**: Don't validate auto-generated per-session settings files
3. **Direct Execution Detection**: Flag fragile patterns like `python3 $ROOT` or `bash $ROOT`

These patterns were formalized in [[PR1410]] to prevent system lockouts when `$ROOT` or other environment variables are undefined.
