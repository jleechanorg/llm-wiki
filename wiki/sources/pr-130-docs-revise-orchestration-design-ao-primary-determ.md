---
title: "PR #130: docs: revise orchestration design — AO primary, deterministic-first"
type: source
tags: []
date: 2026-03-14
source_file: raw/prs-worldai_claw/pr-130.md
sources: []
last_updated: 2026-03-14
---

## Summary
- **Architecture revision**: agent-orchestrator (AO) replaces mctrl as primary orchestration layer
- **Deterministic-first principle**: AO reaction engine handles obvious cases (CI fail, review comments), OpenClaw LLM handles judgment calls only
- **Nested Ralph loops**: reframed as headless calls with fresh context per iteration (dodges context exhaustion)
- **Gastown rejection**: quantified — 348k LOC Go vs ~3k LOC actually used from AO
- **Research doc**: competitive analysis across 6 framewo

## Metadata
- **PR**: #130
- **Merged**: 2026-03-14
- **Author**: jleechan2015
- **Stats**: +703/-548 in 2 files
- **Labels**: none

## Connections
