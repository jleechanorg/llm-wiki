---
title: "test_sariel_with_prompts.py"
type: entity
tags: [test-file, prompt-logging, debugging]
sources: [sariel-test-files-analysis]
last_updated: 2026-04-08
---

## Description
Test file running one Sariel campaign with first 10 interactions while logging prompts sent to LLM. Makes 11 API calls: 1 campaign creation + 10 interactions (no state checks).

## Status
**REDUNDANT** — fully covered by test_sariel_consolidated.py with SARIEL_DEBUG_PROMPTS=true

## Key Features
- Monkey patches llm_service to capture prompts
- Logs first 50 lines of each prompt
- Saves captured prompts to JSON file
- Focuses on prompt debugging

## Connections
- [[TestSarielConsolidated]] — replacement test
- [[SarielTestFilesAnalysis]] — source analysis
