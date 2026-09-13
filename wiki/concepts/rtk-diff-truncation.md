---
title: "rtk PreToolUse hook silently rewrites/compacts git and gh commands"
type: concept
tags: [tooling, claude-code, git, gh, hooks]
date: 2026-09-12
---

## Summary

`rtk` ("Rust Token Killer", Homebrew-core, installed 0.38.0 on this Mac) is wired into Claude Code via a `PreToolUse` hook (`~/.claude/settings.json` → `~/.claude/hooks/rtk-hook-guard.sh` → `rtk hook claude "$@"`). Any Bash tool call whose leading token is a bare `git`, `gh`, `grep`, or ~25 other CLI names gets silently rewritten to `rtk <subcommand>` before it runs, and `rtk` then compacts/truncates the real output — with no `diff --git`/`index`/`---`/`+++` headers on diffs, a mid-output "... (more changes truncated)" line, and an easy-to-miss `[full diff: rtk git diff --no-compact]` footer.

## Key Claims

- It is harness-level (a Claude Code hook config), not a shell alias/function/git-config wrapper.
- Confirmed rewritten: `git diff`, `git show`, `git log -p`, `gh pr diff`, `grep` — anything invoked by bare command name.
- Three confirmed bypasses: (1) absolute path (`/usr/bin/git ...`, `/usr/bin/grep ...`) — the hook pattern-matches the literal leading token, not the resolved binary; (2) the undocumented `--no-compact` flag; (3) `CLAUDEM_MODE=1` / `CLAUDEW_MODE=1` env var, which the guard script checks and skips entirely (already exposed via the `claudem()` shell function).
- Fully user-owned and removable: installed by `rtk init`, removable via `rtk init --uninstall` or deleting the hook entry from `settings.json` — not a binary patch or upstream report.
- A first, older (2026-06-12) sighting only noted "rtk shell wrapper mangles heredocs" without diagnosing the mechanism; this session's research (2026-09-11/12) is the first full root-cause.

## Key Quotes

> "gh pr diff 9835 --patch returned a 552-line compacted summary; the real diff via /usr/bin/git diff <merge-base> pr9835-review was 3127 lines across 233 files."

## Connections

- [[twodot-diff-pollutes-review-packets]] — a second, independent diff-integrity trap discovered in the same review session
- [[web-advice]] — review workflow whose evidence packets this bug can silently corrupt
- Bead: `rev-mdl72`
