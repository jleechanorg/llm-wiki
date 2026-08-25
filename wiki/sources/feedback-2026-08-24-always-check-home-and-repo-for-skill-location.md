---
title: "Always check ~ and repo for skill location"
type: source
tags: [learning, best-practice, agent-harness]
date: 2026-08-24
source_file: raw/feedback_2026-08-24_always_check_home_and_repo_for_skill_location.md
---

## Summary

While researching where the `/research` command's underlying skill actually lives for the jleechan-skills reference repo's README, a check of only the repo's `.claude/skills/` tree wrongly suggested the skill had no standard-location home. The real canonical copy was at `~/.claude/skills/research/SKILL.md` (global, home directory) — the repo just lacked its own mirror at the conventional `.claude/skills/research/` path that every other referenced skill uses.

## Key Claims

- A skill/command's real content can be canonical-only in `~/.claude/` (global) with no repo-local mirror, or canonical-only in a repo with no global copy — either state is normal, not a sign the skill doesn't exist.
- Checking only one of the two locations before concluding "X is missing" produces a false negative.
- This generalizes beyond `/research` — any coding-agent skill lookup should check both scopes before asserting absence.

## Key Quotes

> "where does it live? it should be in ~. Remember to always check ~ and .claude" — the user catching the incomplete check live, 2026-08-24, jleechan-skills session

## Connections

- [[jleechan-skills]] — the repo where this was found and fixed (PR #366)
- Persisted as a standing rule in `~/.claude/CLAUDE.md` under "Verify before reporting" via `/up --global`, same day.
