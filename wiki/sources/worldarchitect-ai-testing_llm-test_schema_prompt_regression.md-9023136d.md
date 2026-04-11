---
title: "WorldArchitect.AI Schema Prompt Regression Test"
type: source
tags: [worldarchitect-ai, testing, schema, regression, prompt-engineering, branch-comparison]
date: 2026-04-07
source_file: raw/schema-prompt-regression-pr5584.md
last_updated: 2026-04-07
---

## Summary
Regression test specification for PR #5584 comparing dynamic prompts (agent_prompts.py + prompts/*.md) between origin/main and schema_followup branches. Runs six schema validation test suites on both branches to confirm semantic equivalence and detect pass-rate regression.

## Key Claims
- **Test Scope**: Six test suites comparing main vs schema_followup branch
- **Tests Run**: Schema validation, schema enforcement journey, schema validation extended, schema validation fallback, schema migration flow, and smoke tests
- **Real API Requirement**: Uses GEMINI_API_KEY for real API calls (not mocked)
- **Prompt Diff Analysis**: Compares agent_prompts.py, prompts/*.md, narrative_response_schema.py, and schemas/validation.py
- **Status**: RED (failing) — test framework defined but execution results pending

## Key Configuration
- **Main worktree**: Temporary directory created via `git worktree add`
- **Branch worktree**: /Users/jleechan/projects/worktree_schema/
- **Port Requirement**: No test server on port 5000
- **Auth Required**: GOOGLE_APPLICATION_CREDENTIALS pointing to ~/serviceAccountKey.json

## Connections
- [[WorldArchitect.AI 20-Turn Test Improvement]] — prior E2E testing iteration
- [[WorldArchitect.AI GitHub Development Statistics]] — development velocity metrics
- [[Testing]] — testing methodology and infrastructure

## Contradictions
- None identified — this is a new test specification
