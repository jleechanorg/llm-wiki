---
title: "Directive-Sentence Cross-Check"
type: concept
tags: [methodology, quality, content-migration]
date: 2026-07-12
---

## Definition

A verification technique for any content-relocation refactor (merging files, moving logic between locations, consolidating duplicate docs): grep the OLD content for directive-marker words (`must`, `never`, `always`, `do not`, `Do not`, `required`, `not allowed`), then explicitly confirm each matched sentence's substance survives in the NEW content — adding it if missing.

## Why it works

A manual read-through pattern-matches on "does this look complete" and is fooled by well-organized new content that's missing specific rules. Grepping for directive words forces exhaustive enumeration of every RULE (not just every topic), turning a fuzzy completeness check into a checklist.

## Track record (2026-07-12)

Caught real content-loss regressions across roughly 10 command-to-skill migrations in one session, including 2 dropped guardrail passages found by an `/advice` review and several more found proactively once the technique was adopted as a standing step.

## Sources

- [Directive-sentence cross-check catches content loss](../sources/feedback-2026-07-12-directive-sentence-cross-check-catches-content-loss.md)

## Related

- [[FatCommandToThinSkillMigration]]
