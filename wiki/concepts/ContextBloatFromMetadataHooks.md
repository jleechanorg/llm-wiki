---
title: "Context Bloat from Metadata Hooks"
type: concept
tags: [context, hooks, metadata, performance, error-suppression]
sources: []
last_updated: 2026-04-11
---

## Description
A metadata-updater hook script emits 2 error lines per Bash tool call, even when the hook is non-essential. This burns 10-15% of context on every session with no way to disable it.

## Symptoms
- Every Bash invocation generates 2 error lines in output
- Error lines are non-critical (hook metadata not essential)
- CLAUDE.md context bloat worsens the problem (40K chars triggers perf warning)
- No --quiet flag to suppress hook output

## Root Cause
`metadata-updater.sh` hook writes error messages to stderr for every Bash invocation. The hook is informational (not required for correctness), but its error output accumulates across the session.

## Fix
1. Redirect hook errors to /dev/null or a log file, not stderr
2. Add `--silent` flag to suppress hook output
3. Gate hook execution behind an env var: `METADATA_HOOK_ENABLED=1`
4. Fix the root cause of hook errors (usually missing state files)

## Connections
- [[Context-Bloat]] — broader context pressure problem
- [[Hooks]] — hook system that triggers this
- [[ContextMCP]] — context management tools
