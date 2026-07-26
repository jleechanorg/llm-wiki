---
title: "HarnessSurfaceConsistency"
type: concept
tags: [harness, process, skills, enforcement]
date: 2026-07-19
---

# HarnessSurfaceConsistency

**Rule:** when a directive changes an agent-harness contract, every surface that teaches that contract must be updated in the SAME pass — slash-command file, skill file, sibling skills that reference it, repo contract tests, and any export mirror. A directive that lands on only some surfaces is indistinguishable from no directive, because agents obey whichever surface actually loads (for Claude Code skills, the Skill-tool-loaded SKILL.md wins over the command-file header).

**Done-check:** after editing, `grep -rl` every surface for the banned/changed pattern, and locally simulate any doc contract tests (literal-glyph regexes, slash-token sweeps) before pushing.

**Escalation:** per harness-fix-durability, a directive violated twice warrants hook- or CI-level enforcement (contract tests over the doc files), not another memory note.

## Origin

Distilled 2026-07-19 from the sidekick team-only migration: a 2026-07-11 user directive lived only in a command header + draft hook while SKILL.md taught the opposite for a week ([PR #337](https://github.com/jleechanorg/claude-commands/pull/337), merged `6462b69`).

## Connections

- [[SkillStaleness]] — sibling failure class (stale probe vs contradictory surface)
- [[HarnessEngineering]] — the discipline this rule belongs to
- [[EvidenceHarnessDiscipline]] — contract tests as the enforcement layer
- Source: [[feedback-2026-07-19-harness-surface-consistency-sidekick]]
