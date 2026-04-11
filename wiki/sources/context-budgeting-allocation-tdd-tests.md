---
title: "Context Budgeting and Allocation TDD Tests"
type: source
tags: [python, testing, context-compaction, budget-allocation, tokens]
source_file: "raw/test_context_budgeting.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test suite validating the context budgeting and allocation system. Tests verify safe context token budget calculation for known and unknown models, component-level budget allocation with minimum guarantees, system instruction warning thresholds, and emergency compaction triggers for oversized components.

## Key Claims
- **Safe Budget Calculation**: Uses MODEL_CONTEXT_WINDOW_TOKENS with CONTEXT_WINDOW_SAFETY_RATIO for known models; falls back to DEFAULT_CONTEXT_WINDOW_TOKENS for unknown providers/models
- **Component Budget Allocation**: Normal-sized components get minimum guarantees (10% system, 5% game, 20% core, 3% entity, 30% story) without compaction
- **Warning Threshold**: System instruction at 41% generates warning but doesn't trigger compaction (stays within 42% allocatable max)
- **Emergency Compaction**: System instruction exceeding 100k tokens triggers emergency compaction regardless of remaining budget

## Key Test Cases
- test_safe_budget_uses_ratio_for_qwen — validates token budget = context_window × safety_ratio
- test_safe_budget_falls_back_for_unknown_model — validates DEFAULT fallback
- test_budget_allocation_normal_components — validates 40%+ story allocation for normal inputs
- test_budget_allocation_system_instruction_above_warn_threshold_generates_warning — validates 40% warning threshold
- test_budget_allocation_emergency_system_instruction_compaction — validates emergency trigger at >100k tokens

## Connections
- [[ContextCompaction]] — module being tested
- [[TokenBudgetAllocation]] — the system under test
- [[ContextWindow]] — concept governing max input sizes
