---
name: thermo-simplify-cross-validation-pattern
description: 4-subagent fanout for /thermo and /simplify yields 52 findings on 15K LOC codebase; 12 cross-validated by 2+ agents
metadata: 
  node_type: memory
  type: project
  bead: "jleechan-kxf,ige,96f,4t5,6w7,du1,ij1,zz3,gs2"
  originSessionId: ed6f27c4-4378-42f4-bec7-7e711334e555
---

# thermo+simplify cross-validation (dark-factory, 2026-06-12)

## Pattern

4 parallel subagents, non-overlapping scope:
- `thermo-nuclear-code-quality-review` × 2 (runner/ + tests/)
- `code-review` × 2 (runner/+bin/ + tests/)

Each gets:
- File list + line ranges to target
- Output format: JSON with `{file, line, category, severity, snippet, diagnosis, suggested_fix}`
- Ground rule: "real findings only; verify line numbers; skip if clean"

## Result

- 52 findings total (9 + 11 + 14 + 18)
- **12 cross-validated** by 2+ agents → high confidence
- 9 beads created, batched into 3 fix subagents on 3 non-overlapping branches

## Cross-validated findings (12)

1. `parser.py:88-93` duplicate `is_start_node` / `is_exit_node` (HIGH — real bug)
2. `engine._evaluate_expression` ↔ `parser._validate_condition` share 13-entry token spec (HIGH)
3. `evidence.py:2034-2043` GCP-cred strip loop duplicated in same function (MED)
4. `_classify_outcome` duplicated engine.py:84 ↔ perf_log.py:22 (MED)
5. `time.sleep(0.01)` for race window in test_parallel_fanout.py:248 (LOW)
6. 4 near-identical gate implementations in handlers.py (LOW)
7. `_dot_2branch` helper exists but 20+ tests inline their own DOT (MED)
8. `_substitute_state` loop duplicated 3× in `_render_prompt` (LOW)
9. Ad-hoc `type("Node", (), {...})` stubs in test_gates.py (LOW)
10. `_as_text` bytes-coercion + CSV parser + git-rev-parse duplicated 3+4× (LOW)
11. `_pipeline(name)` helper duplicated byte-for-byte in 8 test files (MED)
12. `subprocess.run([conformance])` helper reimplemented in 4+ files (MED)

## File-overlap analysis (the critical pre-check)

Before fanning fix subagents:
- A: parser.py + evidence.py (own)
- B: engine.py + perf_log.py + new runner/_git.py + 3 call sites (handlers/evidence/perf_log) — own
- C: tests/ (conftest + 8+ test files) — own

3 independent branches, 3 PRs.

## Why

Cross-validation gives confidence to act on borderline findings (e.g., a reuse opportunity flagged by only one agent might be too speculative; flagged by two it's a real pattern). 12 cross-validated issues is high yield for 4 subagents of work.

## How to apply

For any future code-quality audit on this repo (or similar 15K-LOC repos):
- 4 subagents with non-overlapping scope
- File-overlap check before fanning fix subagents
- Cross-validation as the confidence filter
- Batch cross-validated findings into beads; single-issue findings get bead-stacked separately
