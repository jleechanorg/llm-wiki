---
title: "Fat-command-to-thin-skill migration can break a repo's own regression tests"
type: source
tags: [claude-code, migration, testing, dark-factory]
date: 2026-07-12
source_file: raw/feedback_2026-07-12_fat-command-to-thin-skill-migration-regression-test-check.md
---

## Summary

Relocating content from a Claude Code command file into a canonical SKILL.md (thin-stub pattern) broke `dark-factory`'s own `tests/test_slash_command_binary_contract.py`, which asserted literal proof-block text existed inside `f.md`/`fs.md` themselves — exactly the pre-migration architecture the refactor deliberately changed. A "docs-only" file-extension classification does not mean zero code-level regression risk when a repo has tests that assert on markdown/prompt content.

## Key Claims

- `git diff --stat` alone does not surface this risk class; the target repo's test suite must be grepped for references to the files being changed.
- A second guard test in the same file (`test_fs_has_no_read_only_in_session_modes`) caught a genuine wording regression the migration introduced — CI caught it even after 2 rounds of `/advice` and an independent adversarial verification pass.
- Updating a test to match a deliberate architecture change is a legitimate fix, distinct from weakening a test — the distinction matters for how the fix should be characterized in a commit message.

## Key Quotes

> "The test broke not because content was lost, but because it checked the wrong file for the new architecture."

## Connections

- [[UsageSignalSubstringCountInvalid]] — same migration session.
- [[DirectiveSentenceCrossCheck]] — the technique used to verify content actually survived the relocation.
- PR https://github.com/jleechanorg/dark-factory/pull/251
