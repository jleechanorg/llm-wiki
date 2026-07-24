---
title: "ReversibleFacadePattern"
type: concept
tags: [architecture, skill-design, default-tool, rollback]
sources: ["aside-browser-default-switch-2026-06-27"]
last_updated: 2026-06-27
---

## Summary
A design pattern for changing the default tool in a skill ecosystem without breaking agents that depend on the prior tool. The new tool becomes primary; the old tool is preserved as an explicit named fallback. A single rollback script snapshots state before mutating, applies the change, and exposes the inverse operation so the switch can be undone in one command.

## Properties
- **Primary + named fallback(s)**: the new tool is the recommended default, but the old tool stays fully functional and is referenced by name in policy files (so agents know to fall back when the primary is unavailable).
- **Line-targeted edits**: all policy files are patched with stable, unique strings — no full-file overwrites. This makes `git diff` readable and rollback trivial.
- **Snapshot before mutate**: the rollback script captures the original state (e.g., `~/.claude.json` mcpServers block, the existing SOUL.md browser COMMIT block) into a timestamped JSON file before applying any change.
- **Single command to revert**: `bash ~/.hermes/scripts/rollback-<change>.sh` returns everything to the pre-change state without manual cleanup.

## Notable Instances
- [[Aside browser default switch (2026-06-27)]] — primary tool = [[AsideBrowser]], fallbacks = [[PlaywrightMCP]] + [[SuperpowersChrome]] + [[Chrome]]. Rollback at `~/.hermes/scripts/rollback-aside-default.sh`.

## When to Use
- Introducing a new default tool across `~/.hermes/`, `~/.claude/`, `~/.codex/`, or `~/.agents/` skill directories.
- Changing a commit-block policy that touches 50+ skills (the pattern of "primary + named fallback + snapshot + rollback" prevents the change from cascading).
- Any time the user asks for "make X the default" or "switch from Y to Z" across the agent toolchain.

## When NOT to Use
- For one-off tool changes that don't touch policy files (just add the new tool, no facade needed).
- For backwards-incompatible API renames (the facade doesn't help — agents calling the old API would still break).