---
title: "CodeRabbit CHANGES_REQUESTED on a docs-only PR can hide a real functional-correctness bug"
type: source
tags: [coderabbit, code-review, pr-workflow, dark-factory]
date: 2026-07-12
source_file: raw/feedback_2026-07-12_coderabbit-changes-requested-can-hide-real-bugs-on-docs-only-pr.md
---

## Summary

On a markdown-only "docs-only" thin-skill-migration PR, CodeRabbit returned CHANGES_REQUESTED with 3 findings: 2 trivial markdownlint issues and 1 real "Major/Functional Correctness" bug — documentation said an argument "defaults to hello" unconditionally, contradicting a Honesty rule added earlier in the same file forbidding invented default values. "Docs-only" describes the diff shape, not the risk class, when the files touched are agent-read prompt/instruction files whose content is executable in the sense that an LLM agent will follow the documented default literally.

## Key Claims

- Never skip reading CodeRabbit's full comment bodies on the assumption that docs-only findings will all be lint noise.
- Fetch every review comment (`gh api repos/OWNER/REPO/pulls/N/comments`) and read the finding text + severity tag before triaging.
- Docs-only classification changes the evidence tier required for merge (per the two-tier `/green` standard), not whether individual findings need to be evaluated on content.

## Connections

- [[FatCommandToThinSkillMigrationRegressionTestCheck]] — same PR, same session.
- PR https://github.com/jleechanorg/dark-factory/pull/251
