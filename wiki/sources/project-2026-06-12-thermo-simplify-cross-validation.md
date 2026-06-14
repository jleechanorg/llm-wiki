---
title: "Thermo+Simplify Cross-Validation (dark-factory, 4-Subagent Fanout)"
type: source
tags: [dark-factory, thermo-nuclear, code-review, cross-validation, parallel-subagents, file-disjoint-lanes]
date: 2026-06-12
source_file: /Users/jleechan/.claude/projects/-Users-jleechan-projects-dark-factory/memory/project_2026-06-12_thermo_simplify_cross_validation.md
---

## Summary
4 parallel subagents (2 thermo-nuclear + 2 code-review) on a 15K-LOC codebase yielded 52 findings, with 12 cross-validated by 2+ agents → high confidence. Findings batched into 9 beads and routed to 3 non-overlapping branches via file-overlap analysis.

## Key Claims
- 4 parallel subagents, non-overlapping scope: `thermo-nuclear-code-quality-review` × 2 (runner/ + tests/), `code-review` × 2 (runner/+bin/ + tests/).
- Output format: JSON with `{file, line, category, severity, snippet, diagnosis, suggested_fix}`.
- Ground rule: "real findings only; verify line numbers; skip if clean".
- 52 findings (9 + 11 + 14 + 18); 12 cross-validated by 2+ agents.
- File-overlap analysis: A: parser.py + evidence.py, B: engine.py + perf_log.py + new runner/_git.py, C: tests/. 3 independent branches, 3 PRs.
- HIGH: `parser.py:88-93` duplicate `is_start_node` / `is_exit_node`; `engine._evaluate_expression` ↔ `parser._validate_condition` share 13-entry token spec.
- MED: `evidence.py:2034-2043` GCP-cred strip loop duplicated; `_classify_outcome` duplicated engine.py:84 ↔ perf_log.py:22; `_dot_2branch` helper exists but 20+ tests inline their own DOT; `_pipeline(name)` helper duplicated byte-for-byte in 8 test files; `subprocess.run([conformance])` helper reimplemented in 4+ files.
- Cross-validation is the confidence filter: reuse opportunity flagged by 1 agent may be speculative; flagged by 2 = real pattern.

## Key Quotes
> "Cross-validation gives confidence to act on borderline findings (e.g., a reuse opportunity flagged by only one agent might be too speculative; flagged by two it's a real pattern). 12 cross-validated issues is high yield for 4 subagents of work."

## Connections
- [[ParallelSubagents]] — file-disjoint lanes pre-check
- [[ThermoNuclearCodeQualityReview]] — review skill
- [[CodeReview]] — second review skill
- [[BeadFollowupTemplates]] — bead template for follow-up
