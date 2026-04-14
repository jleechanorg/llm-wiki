---
title: "Harness Engineering"
type: source
tags: [harness, quality, debugging, automation, failure-analysis]
sources: []
last_updated: 2026-04-14
---

## Summary

Harness Engineering is a quality methodology that analyzes failures and fixes the harness (instructions, skills, tests, CI) rather than just the symptom. It applies at the user level across all repositories with project-level overrides.

## Key Claims

- Failure classes: mislabeled artifact, wrong approach, missing validation, repeated manual fix, silent degradation, knowledge gap, LLM path error
- Mandatory 5 Whys analysis for both technical failure and agent path on every failure
- Fix durability must match violation severity (Memory < CLAUDE.md instruction < Hook < Hook+commit < Hook+CI gate)
- Default mode (/harness) waits for approval; Fix mode (/harness --fix) implements immediately
- Audit mode (/harness --audit) scans all instruction files for staleness, contradictions, gaps, and duplication

## Key Quotes

> "When this command is invoked, analyze the current situation for harness-level gaps and propose/implement fixes that prevent the same class of mistake from recurring"

> "Same code review comment given 3 conversations in a row = repeated manual fix = mandatory harness fix, no exceptions"

## Connections

- [[CommandSystemDocumentation]] — Part of command system
- [[EvolveLoop]] — Autonomous evolution loop for AO ecosystem
- [[Auton]] — Diagnoses WHY system is not autonomously driving PRs

## Contradictions

- None identified
