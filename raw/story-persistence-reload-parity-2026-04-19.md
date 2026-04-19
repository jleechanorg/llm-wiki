# Story persistence & reload parity — 2026-04-19

**Source:** `/Users/jleechan/roadmap/learning-2026-04-19-story-persistence-reload-parity.md` + conversation + harness skill draft.

## Tenet

Round-trip parity: persisted campaign/story data must reproduce the same user-visible choices and planning UI after reload as immediately after the turn, unless a field is explicitly session-only / ephemeral.

## PR #6376 issue class

Stripping `planning_block` for god-mode before story persistence prevents reload from showing planning blocks the user saw on the live turn — **wrong** if reload fidelity is required.

## Harness

- Skill: `story-persistence-reload-parity.md` in `jleechanorg/worldarchitect.ai` `.claude/skills/`
- `CLAUDE.md` references the skill in the skill list.

## Links

- https://github.com/jleechanorg/worldarchitect.ai/pull/6376
