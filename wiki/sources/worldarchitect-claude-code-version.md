---
title: "Claude Code Version Stability Report — v2.1.77 to v2.1.92"
type: source
tags: [claude-code, version-upgrade, stability, Claude-Code]
date: 2026-04-05
source_file: /Users/jleechan/Downloads/claude-code-version-stability-2026-04-05.md
---

## Summary

A comprehensive stability report covering Claude Code versions v2.1.77 through v2.1.92, with upgrade recommendations. The compaction threshold bug is platform-wide (not version-specific). Recommended upgrade target is v2.1.85 (all good fixes, no regressions). Critical regressions exist in v2.1.86 (agent work destruction), v2.1.87 (broken hotfix), and v2.1.90 (--continue data loss). PreCompact/PostCompact hooks remain unimplemented across all versions.

## Version Summary

| Version | Rating | Key Issues |
|---------|--------|-----------|
| v2.1.77 | GREEN | Stable baseline; known compaction threshold bug (platform-wide) |
| v2.1.78 | YELLOW | Permission regression for `.claude/` writes (fixed in v2.1.80) |
| v2.1.79 | GREEN | Mostly fixes; low risk |
| v2.1.80 | YELLOW | acceptEdits Write regression (fixed) |
| v2.1.81 | GREEN | Added `--bare` flag; solid release |
| v2.1.83 | GREEN | Major quality; CwdChanged/FileChanged hooks, transcript search |
| v2.1.84 | GREEN | PowerShell tool, TaskCreated hook, idle-return prompt |
| v2.1.85 | GREEN | Conditional hook `if` field, fixed `/compact` on large convos |
| **v2.1.86** | **RED** | **Critical: agent destroys user work (#40808), Write/Edit/Read failing on files outside project root** |
| **v2.1.87** | **RED** | **Broken hotfix: spacebar fails, 401 after login, broken upgrade path** |
| v2.1.88 | YELLOW | MCP tool results invisible; excessive token consumption |
| v2.1.89 | YELLOW | Autocompact thrash fix, PermissionDenied hook, large changeset (50+ items) |
| **v2.1.90** | **RED** | **`--continue -p` data loss regression (#43013, #42376)** |
| v2.1.91 | YELLOW | Fixed --resume transcript chain breaks; pgrep crash on macOS |
| v2.1.92 | YELLOW | Many fixes; remote-control regression, arrow key issues, intermittent freezes |

## Upgrade Recommendation

**Best target: v2.1.85** — includes all good fixes from v2.1.78-v2.1.84, conditional hook filtering, `/compact` fix, no regressions from v2.1.86+.

If v2.1.89+ features needed (autocompact thrash fix, PermissionDenied hook, `defer`): use v2.1.89 with awareness of Linux terminal content disappearing issue.

**Avoid: v2.1.86** (critical agent behavior regression), **v2.1.87** (broken hotfix), **v2.1.90** (--continue data loss, unfixed as of v2.1.92).

## Open Issues (PreCompact/PostCompact Hooks)

- #17237 (oldest), #33088, #36749, #38018, #40492, #43733, #43946
- Available hooks: PreToolUse, PostToolUse, StopFailure (v2.1.78+), SessionEnd, CwdChanged/FileChanged (v2.1.83+), TaskCreated (v2.1.84+), PermissionDenied (v2.1.89+)
- **No compaction hooks implemented** — all feature requests remain open

## CLAUDE.md Permission Dialog (Persistent Issue)

The `.claude/` directory has special built-in protection overriding user permission settings. This is architectural (security) and **not fixed in any version**. v2.1.78 regression (#35895, #35908) was fixed in v2.1.80. v2.1.86 regression partially addressed but #37516 (Edit permission rules have no effect) remains open.

## Connections

- [[ClaudeCode]] — version upgrade impacts Claude Code CLI behavior
- [[ContextCompaction]] — compaction hooks are the primary unmet need

## Contradictions

- None identified
