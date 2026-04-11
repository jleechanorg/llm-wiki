---
title: "Beads Database Survey 2026-04-11"
type: source
tags: [beads, failure-patterns, worldarchitect, openclaw]
date: 2026-04-11
source_file: various .beads/ directories
---

## Summary
Systematic survey of beads databases across all repos on 2026-04-11. Found 12+ beads databases containing 300+ issues combined. Prioritized failure patterns, harness gaps, and agent failures.

## Key Beads Databases Found
- `/Users/jleechan/worldarchitect.ai/.beads/beads.db` + `issues.jsonl` — 748KB issues, 22KB BD-*.md files
- `/Users/jleechan/.beads/issues.jsonl` — 307 issues (pair sessions, task tracking)
- `/Users/jleechan/.openclaw/.beads/` — OpenClaw MCP work
- `/Users/jleechan/mcp_mail/.beads/` — MCP mail agent work
- `/Users/jleechan/beads/.beads/` — standalone beads tool
- `/Users/jleechan/jcc-19-fix/.beads/` — jcc-19 fix work
- `/Users/jleechan/projects/.beads/` — general projects

## Prioritized Failure Patterns Ingested as Concepts

### P0-P1 Priority
1. **CircuitBreakerAgentSelection** — Agent selected 52+ consecutive times causing infinite loop
2. **CodeExecutionFalsePositiveFabrication** — ~17% false positive fabrication rate on dice turns
3. **BudgetWarningAPISurface** — Budget warnings computed but never serialized
4. **PromptComplianceDrift** — LLMs ignoring 25K-token prompts; need gating blocks
5. **HookMatcherToolAgnostic** — Hooks hardcoded to 'Bash', miss Gemini/Codex tools
6. **PostMergeDuplicatePRLoop** — Workers create fix PRs after original already merged

### P2 Priority
7. **CompactedStateReversion** — JSON truncation falls back to full state (defeats compaction)
8. **EntityTrackingValidationFailure** — 0-4% entity validation pass rate
9. **PairVerifierCodexPreflight** — Verifier fails when codex preflight validation fails
10. **WorkspacePreservationAcrossRetries** — Correct pattern for verify→implement retry loop
11. **ContextBloatFromMetadataHooks** — 2 error lines per Bash call, 40K char CLAUDE.md
12. **StaleProcessGroupTargeting** — PGID must be cleared before kill to avoid wrong-target

## Connections
- [[StructureDriftPattern]] — related: patterns emerging from behavioral drift
- [[Harness5LayerModel]] — beads capture L1-L5 failures across the harness
- [[FPCalculationTransparency]] — faction FP calculation is a source of compliance drift
