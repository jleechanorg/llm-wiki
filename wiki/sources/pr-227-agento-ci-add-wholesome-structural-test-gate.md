---
title: "PR #227: [agento] ci: add wholesome structural test gate"
type: source
tags: []
date: 2026-03-27
source_file: raw/prs-worldai_claw/pr-227.md
sources: []
last_updated: 2026-03-27
---

## Summary
Structural quality gates (linting, type-checking, test coverage) run continuously — but they don't catch *process violations* like missing prefixes, new `@ts-ignore` directives, or `eslint-disable` added in a branch. The `wholesome` test suite enforces these at CI time with "multiple shots on goal": deterministic structural assertions that fail the build when the diff breaks repository invariants.

## Metadata
- **PR**: #227
- **Merged**: 2026-03-27
- **Author**: jleechan2015
- **Stats**: +371/-0 in 3 files
- **Labels**: none

## Connections
