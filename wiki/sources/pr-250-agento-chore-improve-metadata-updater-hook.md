---
title: "PR #250: [agento] chore: improve metadata-updater hook"
type: source
tags: []
date: 2026-03-28
source_file: raw/prs-worldai_claw/pr-250.md
sources: []
last_updated: 2026-03-28
---

## Summary
Improves the `metadata-updater.sh` PostToolUse/PreToolUse hook with:

- **Env assignment stripping**: Commands prefixed with `FOO=bar gh pr create` are now correctly detected (previously only `cd`-prefixed commands were stripped)
- **`[agento]` prefix guardrail**: PreToolUse now enforces PR titles start with `[agento]` using python3 shlex parsing (correctly handles `--body="--title=foo"` edge case)
- **Restructured merge guardrail**: Moved before the PostToolUse-only gate so PreToolUse denials f

## Metadata
- **PR**: #250
- **Merged**: 2026-03-28
- **Author**: jleechan2015
- **Stats**: +256/-82 in 8 files
- **Labels**: none

## Connections
