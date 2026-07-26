---
title: "Directive-sentence cross-check catches silent content loss during consolidation refactors"
type: source
tags: [claude-code, migration, quality, methodology]
date: 2026-07-12
source_file: raw/feedback_2026-07-12_directive-sentence-cross-check-catches-content-loss.md
---

## Summary

After an `/advice` review caught two silently-dropped guardrail passages during a fat-command-to-thin-skill migration, a systematic technique was adopted for all subsequent migrations: grep the old content for directive-marker words (`must|never|always|do not|Do not|required|not allowed`), then confirm each one's substance survives in the new content, adding it if missing. This caught multiple further real content-loss regressions across roughly 10 subsequent migrations in the same session.

## Key Claims

- A manual read-through pattern-matches on "does this look complete" and is easy to fool with well-organized new content; grepping directive words forces exhaustive enumeration of every RULE, not just every topic.
- The technique is cheap enough to run by default on any content-relocation refactor — moving logic between files, consolidating duplicate docs, merging similar files.

## Connections

- [[FatCommandToThinSkillMigrationRegressionTestCheck]] — companion technique used in the same session.
- [[UsageSignalSubstringCountInvalid]] — same migration effort.
