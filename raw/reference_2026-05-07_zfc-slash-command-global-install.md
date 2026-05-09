---
name: /zfc slash command — global install and PR
description: General ZFC review command created, PR #6832 filed, skill + commands installed globally in ~/.claude and ~/.codex
type: reference
bead: rev-9lz8v
originSessionId: 6d2e0a6b-9bac-404b-82a4-9153ca92a676
---
## Context

Session on 2026-05-07. User asked for a general `/zfc` slash command pointing to the `zero-framework-cognition` skill that already existed on `origin/main` (commit `e4b79f88a`).

## What was discovered

The general ZFC skill file (`.claude/skills/zero-framework-cognition/SKILL.md`) already existed on `origin/main` — it was committed in `e4b79f88a`. No PR was needed for the skill itself. Only the slash command entry point was missing.

## What was built

1. **`.claude/commands/zfc.md`** — new `/zfc` slash command:
   - Loads `zero-framework-cognition/SKILL.md`
   - 6-step review: scope detection, banned-pattern scan, field ownership check, fix recommendations, PASS/WARN/FAIL verdict
   - PR [#6832](https://github.com/jleechanorg/worldarchitect.ai/pull/6832) on branch `feat/add-zfc-general-skill` (worktree `~/worktree_zfc-skill`)

2. **Global install** to `~/.claude/` and `~/.codex/`:
   - `~/.claude/commands/zfc.md`
   - `~/.claude/commands/zfclevel.md`
   - `~/.claude/skills/zero-framework-cognition/SKILL.md`
   - `~/.codex/commands/zfc.md`
   - `~/.codex/commands/zfclevel.md`
   - `~/.codex/skills/zero-framework-cognition/SKILL.md`

3. **Pointer lines** added to:
   - `~/.claude/CLAUDE.md` (under ZFC section)
   - `~/.codex/AGENTS.md` (under ZFC section)

## Reusable pattern

When a skill exists but has no slash command: create `<name>.md` in `.claude/commands/` with the standard header, a Purpose, a Skill Reference line, and numbered Execution Steps. Then copy both the command and the skill to `~/.claude/` and `~/.codex/` for global availability. Add pointer lines in `CLAUDE.md` and `AGENTS.md`.

## References

- PR [#6832](https://github.com/jleechanorg/worldarchitect.ai/pull/6832)
- Skill: `.claude/skills/zero-framework-cognition/SKILL.md`
- Command: `.claude/commands/zfc.md`
- Original skill source: branch `origin/zfc-audit`, commit `e4b79f88a`
