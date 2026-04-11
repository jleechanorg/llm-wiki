---
title: "PR #308: [agento] feat(skeptic): structured FAIL output with Background/Problem/Solution/Consultation sections"
type: source
tags: []
date: 2026-03-30
source_file: raw/prs-worldai_claw/pr-308.md
sources: []
last_updated: 2026-03-30
---

## Summary
Updates the skeptic LLM prompt so that when the verdict is FAIL, the output includes four structured sections that make failures actionable for reviewers and downstream bots:

- **## Background** — PR number, title, and what it claims to do
- **## Current Problem** — root cause, specific file/function/failure mode (concrete, not vague)
- **## Recommended Solution** — numbered actionable steps
- **## Bot Consultation** — @coderabbitai and @cursor[bot] mentions to trigger review by other agents

P

## Metadata
- **PR**: #308
- **Merged**: 2026-03-30
- **Author**: jleechan2015
- **Stats**: +244/-5 in 3 files
- **Labels**: none

## Connections
