---
title: "br CLI is the Correct Bead Access Pattern — Never Read .beads/*.jsonl"
date: 2026-05-14
type: feedback
bead: rev-1ivmd
related_bead: rev-wgtju
---

## Summary

`br` CLI commands (`show`, `search`, `list`) query `beads.db` (SQLite) directly. Reading `.beads/issues.jsonl` or `.beads/beads.left.jsonl` raw is never necessary and causes context thrashing in wafer/GLM-5.1 sessions.

## Key Findings

| File | Size | Risk |
|------|------|------|
| `.beads/issues.jsonl` | 1.0MB | High — confirmed GLM-5.1 thrash trigger |
| `.beads/beads.left.jsonl` | **5.0MB** | Critical — 5× larger, git-tracked legacy |
| `.beads/beads.db` | 5.7MB | Safe — SQLite, use via `br` CLI |

## Correct Access Pattern

```bash
br show rev-wgtju             # single bead detail
br search "context thrash"    # full-text search
br list --status open --json  # filtered JSON list
br stats --json               # summary counts
```

Never:
```bash
# FORBIDDEN
Read .beads/issues.jsonl
Read .beads/beads.left.jsonl
grep rev-wgtju .beads/issues.jsonl
```

## Why Compaction Is Blocked

- `br sync --flush-only` re-exports the full `beads.db` (all 1,208 records) back to `issues.jsonl`
- 508 closed beads (41% of file, 430KB) could be archived but there is no `br` config for partial export
- A custom `compact_beads.sh` script could filter closed beads to `issues_closed.jsonl` but is not yet implemented

## CLAUDE.md Fix Applied

`~/.claude/CLAUDE.md` — "Known large files" section updated:
- Added `beads.left.jsonl` (5.0MB)
- Added "Bead lookups — always use `br` CLI, never read JSONL" section

## Related Concepts

- [[Compaction]] — autocompact thrash loop mechanism
- [[ClaudeCodeCompaction]] — client-side compaction behavior

## References

- Root cause proof: `beads-issues-jsonl-read-without-offset-wafer-thrash.md`
- Root cause bead: `rev-wgtju`
- Session JSONL: `~/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/c508ff6e-e323-4bd8-be06-6e3e58a53894.jsonl`
