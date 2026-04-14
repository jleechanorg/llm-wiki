# BD-pairv2-llm-driven-failsoft-files

## ID
BD-pairv2-llm-driven-failsoft-files

## Title
pairv2: fail-soft on missing contract/design-doc files and preserve LLM-driven flow

## Status
closed

## Type
enhancement

## Priority
high

## Created
2026-02-24

## Description
Pairv2 should not stop early because user-provided file paths are missing. Missing
left/right contract files or missing design-doc paths are brittle operational issues,
not evidence that implementation is invalid. The workflow should continue via LLM
contract generation and verifier judgment.

## Fix
1. `generate_left_contract`: when provided `left_contract_path` is missing, add note and fall back to LLM generation.
2. `generate_right_contract`: when provided `right_contract_path` is missing, add note and fall back to LLM generation.
3. `_find_design_doc_path`: return empty string when unresolved, so prompts do not include non-existent path.
4. Add tests for missing path fallback and missing design-doc resolution behavior.
5. Add Shadow Execution Gate concrete example to design tenet and add project skill documenting philosophy.

## Scope
- `.claude/pair/pair_execute_v2.py`
- `.claude/pair/tests/test_pair_v2_and_benchmark.py`
- `.claude/pair/DESIGN_TENET.md`
- `.claude/skills/pairv2-llm-driven-philosophy.md`

## Acceptance
- [x] Missing user-provided left contract path no longer hard-fails contract generation.
- [x] Missing user-provided right contract path no longer hard-fails right-contract generation.
- [x] Missing design-doc path is treated as optional context.
- [x] Tests cover missing-path fallback behavior.
- [x] Design doc includes concrete Shadow Execution Gate example.
