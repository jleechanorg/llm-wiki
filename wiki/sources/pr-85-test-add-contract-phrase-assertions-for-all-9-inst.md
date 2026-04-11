---
title: "PR #85: test: add contract phrase assertions for all 9 instruction layers"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-worldai_claw/pr-85.md
sources: []
last_updated: 2026-03-26
---

## Summary
Adds a new test file `packages/backend/src/llm/__tests__/system_instruction_layers.test.ts` that performs TDD contract assertions over the `system_instruction.md` file. Each of the 9 instruction layers has targeted phrase-existence checks that serve as regression guards for the system-instruction contract.

## Metadata
- **PR**: #85
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +291/-0 in 1 files
- **Labels**: none

## Connections
