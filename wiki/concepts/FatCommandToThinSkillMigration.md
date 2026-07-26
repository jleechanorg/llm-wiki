---
title: "Fat-Command-to-Thin-Skill Migration"
type: concept
tags: [claude-code, architecture, migration]
date: 2026-07-12
---

## Definition

The pattern of converting a Claude Code slash-command file that carries all its inline logic (often 100s-1000s of lines) into two pieces: a thin pointer stub (`~/.claude/commands/X.md`, typically <40 lines, "Read `~/.claude/skills/X/SKILL.md` and execute it") and a canonical `SKILL.md` that becomes the single source of truth for the full logic. Multiple entry-point commands can point at the same skill (e.g. `/f` and `/factory` both point at `dark-factory/SKILL.md`).

## Why it matters

Prevents drift between duplicate copies of the same instructions across multiple command aliases, and makes the skill auto-discoverable (skill descriptions feed the model's skill catalog for automatic invocation, not just explicit `/command` typing).

## Risks (learned 2026-07-12 migration)

- [[UsageSignalSubstringCountInvalid]] — prioritizing which commands are worth migrating needs a reliable usage signal.
- [[FatCommandToThinSkillMigrationRegressionTestCheck]] — the target repo's own tests may assert on the OLD structure.
- [[DirectiveSentenceCrossCheck]] — content can be silently dropped during the relocation; needs an explicit check.

## Sources

- [Usage-signal substring count is invalid](../sources/feedback-2026-07-12-usage-signal-substring-count-invalid.md)
- [Fat-command-to-thin-skill migration regression test check](../sources/feedback-2026-07-12-fat-command-to-thin-skill-migration-regression-test-check.md)
- [Shared checkout daemon collision](../sources/feedback-2026-07-12-shared-checkout-daemon-collision-use-worktree.md)
- [Don't override Agent() mode](../sources/feedback-2026-07-12-dont-override-agent-mode-stricter-than-ambient-default.md)
- [Directive-sentence cross-check](../sources/feedback-2026-07-12-directive-sentence-cross-check-catches-content-loss.md)
- [CodeRabbit CHANGES_REQUESTED on docs-only PRs](../sources/feedback-2026-07-12-coderabbit-changes-requested-can-hide-real-bugs-on-docs-only-pr.md)
- PR https://github.com/jleechanorg/dark-factory/pull/251 (reference implementation: `/f`, `/factory`, `/fs`, `/factory-spec`)
