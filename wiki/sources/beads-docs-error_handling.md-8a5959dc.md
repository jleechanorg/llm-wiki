---
title: "Error Handling Guidelines"
type: source
tags: [beads, error-handling, patterns, go, best-practices]
sources: []
date: 2026-04-07
source_file: beads-docs-error_handling.md
last_updated: 2026-04-07
---

## Summary
Documents three distinct error handling patterns used throughout the beads codebase: Exit Immediately (`os.Exit(1)`) for fatal errors, Warn and Continue (`fmt.Fprintf` + continue) for optional operations, and Silent Ignore (`_ = operation()`) for cleanup/best-effort operations. Includes decision tree and anti-patterns to avoid.

## Key Claims
- **Three Patterns**: Exit Immediately (Pattern A), Warn and Continue (Pattern B), Silent Ignore (Pattern C) — understanding when to use each is critical for consistent behavior
- **Pattern A - Fatal Errors**: Uses `os.Exit(1)` for user input validation, critical preconditions, unrecoverable system errors; writes "Error:" prefix to stderr with exit code 1
- **Pattern B - Optional Operations**: Uses `fmt.Fprintf` with "Warning:" prefix for metadata operations, cleanup, auxiliary features; command continues execution
- **Pattern C - Silent Ignore**: Uses `_ = operation()` for resource cleanup, idempotent operations, best-effort operations with no user-visible impact
- **Decision Tree**: Flowchart provided for choosing the appropriate pattern based on error type and recovery possibility
- **Anti-Patterns**: Inconsistent pattern mixing for same operation types must be avoided

## Key Quotes
> "Did an error occur?" → Determine if fatal (Pattern A), optional (Pattern B), or cleanup (Pattern C)

## Connections
- [[Beads]] — the codebase this document applies to
- [[Beads CLI Command Reference]] — error handling patterns used throughout CLI commands

## Contradictions