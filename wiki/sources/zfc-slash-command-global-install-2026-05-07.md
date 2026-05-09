---
title: /zfc slash command — global install and PR
date: 2026-05-07
type: reference
bead: rev-9lz8v
tags: [zfc, slash-command, global-install, claude, codex]
---

## Summary

The general Zero-Framework Cognition skill (`.claude/skills/zero-framework-cognition/SKILL.md`) already existed on `origin/main` (committed `e4b79f88a`) but had no slash command entry point. A `/zfc` command was created and PR [#6832](https://github.com/jleechanorg/worldarchitect.ai/pull/6832) was filed. The command and skill were then installed globally to `~/.claude/` and `~/.codex/` with pointer lines in `CLAUDE.md` and `AGENTS.md`.

## Pattern: skill-exists-but-no-command

When a skill file exists without a slash command, the fix is:
1. Create `.claude/commands/<name>.md` with standard frontmatter + Purpose + Skill Reference + numbered Execution Steps
2. Copy command + skill to `~/.claude/commands/`, `~/.claude/skills/`, `~/.codex/commands/`, `~/.codex/skills/`
3. Add pointer lines under the relevant section in `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md`

## Files created/updated

- `.claude/commands/zfc.md` (repo + global)
- `~/.claude/skills/zero-framework-cognition/SKILL.md`
- `~/.codex/skills/zero-framework-cognition/SKILL.md`
- `~/.claude/CLAUDE.md` (pointer added)
- `~/.codex/AGENTS.md` (pointer added)

## References

- PR [#6832](https://github.com/jleechanorg/worldarchitect.ai/pull/6832)
- Bead: rev-9lz8v
- Skill source: branch `origin/zfc-audit`, commit `e4b79f88a`
