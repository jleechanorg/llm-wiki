---
title: "PR #5731: Add opt-in flags for preflight validation and prompt templating"
type: source
tags: []
date: 2026-02-23
source_file: raw/prs-worldarchitect-ai/pr-5731.md
sources: []
last_updated: 2026-02-23
---

## Summary
Refactors agent creation to make pre-flight CLI validation and prompt template injection opt-in features with sensible defaults. Changes the default behavior to skip pre-flight validation (avoiding side effects) and use raw prompts without template injection, while allowing callers to explicitly enable these features via agent_spec flags.

## Metadata
- **PR**: #5731
- **Merged**: 2026-02-23
- **Author**: jleechan2015
- **Stats**: +214/-69 in 8 files
- **Labels**: none

## Connections
