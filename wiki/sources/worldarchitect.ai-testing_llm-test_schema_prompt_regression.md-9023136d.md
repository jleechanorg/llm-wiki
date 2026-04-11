---
title: "Schema Prompt Regression Test - PR#5584"
type: source
tags: [testing, schema, regression, branch-comparison, PR-5584, prompt-validation]
sources: []
date: 2026-04-07
source_file: /Users/jleechan/projects/worktree_schema/schema_prompt_regression_test.md
last_updated: 2026-04-07
---

## Summary
Regression comparison test for PR #5584. Runs schema validation and smoke tests on both `origin/main` and `schema_followup` branches, then produces a side-by-side report. Confirms that dynamic prompts (agent_prompts.py + prompts/*.md) are semantically equivalent between branches and that schema-test pass rates did not regress.

## Key Claims
- **Phase 1**: Runs 6 test suites on `origin/main`: schema_validation_real_api, schema_enforcement_journey, schema_validation_extended, schema_validation_fallback, schema_migration_flow, test_smoke
- **Phase 2**: Runs identical 6 test suites on `schema_followup` branch
- **Phase 3**: Diff analysis of agent_prompts.py, prompts/*.md, narrative_response_schema.py, schemas/validation.py
- **Phase 4**: Extracts and compares PASS/FAIL counts from all log files
- **Phase 5**: Generates comparison report with pass/fail deltas

## Key Quotes
> "Goal: Confirm that the dynamic prompts (agent_prompts.py + prompts/*.md) are semantically equivalent between the two branches and that schema-test pass rates did not regress."

## Pre-conditions
- `GEMINI_API_KEY` must be set (real API calls, not mock)
- `GOOGLE_APPLICATION_CREDENTIALS` must point to `~/serviceAccountKey.json`
- Worktree at `/Users/jleechan/projects/worktree_schema/`
- Clean temporary worktree for `origin/main` created during setup

## Test Phases

### Phase 1 - Main Branch Tests
- T1a: Schema validation real-API test (main)
- T1b: Schema enforcement journey test (main)
- T1c: Schema validation extended test (main)
- T1d: Schema validation fallback test (main)
- T1e: Schema migration flow test (main)
- T1f: Smoke test (main)

### Phase 2 - Schema Followup Branch Tests
- T2a-T2f: Same 6 tests on schema_followup branch

### Phase 3 - Prompt Diff Analysis
- T3a: Diff agent_prompts.py
- T3b: Diff prompts/*.md files
- T3c: Diff narrative_response_schema.py
- T3d: Diff schemas/validation.py

### Phase 4 - Summarize Pass/Fail Counts
- Extract PASSED/FAILED/ERROR from each log file

### Phase 5 - Generate Comparison Report
- Side-by-side markdown report with pass/fail deltas

## Connections
- [[TestingMCP]] — testing infrastructure
- [[SchemaValidation]] — what is being tested
- [[SchemaFollowup]] — schema_followup branch context
- [[PromptsDirectory]] — prompts/*.md files being diffed

## Contradictions
- None identified

## Test Status
- Not yet executed — requires GEMINI_API_KEY and worktree setup