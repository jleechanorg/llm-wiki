---
title: "Complete Combined Approach (Structured Generation + Validation) Implementation Tests"
type: source
tags: [python, testing, structured-generation, entity-tracking, validation, integration-tests]
source_file: "raw/test_complete_combined_approach.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test suite demonstrating the full implementation of Milestone 1: Combined approach using Structured Generation + Validation for entity tracking in narrative responses. Tests cover prompt creation, JSON parsing, entity validation, and end-to-end workflow.

## Key Claims
- **Structured Prompt Creation**: Entity manifest excludes hidden entities from prompt injection while maintaining tracking requirements
- **JSON Response Parsing**: parse_structured_response extracts narrative and structured data from LLM JSON output
- **Entity Coverage Validation**: validate_entity_coverage() confirms LLM mentioned all visible entities in the scene
- **Complete Workflow Integration**: Full pipeline from game state → structured prompt → LLM response → validation

## Key Test Cases
- test_step1_structured_generation_prompt_creation: Verifies entity manifest excludes hidden entities (Hidden Assassin) and prompt contains all required components
- test_step2_structured_response_parsing: Validates JSON parsing extracts narrative and structured response fields
- test_step3_entity_coverage_validation: Tests validation logic for mentioned vs expected entities
- test_step4_end_to_end_combined_workflow: Full integration test of entire pipeline

## Connections
- [[NarrativeResponseSchema]] — schema definitions for structured response parsing
- [[EntityTracking]] — entity manifest creation from game state
- [[NarrativeSyncValidator]] — entity coverage validation concept
- [[Gideon]] — player character entity
- [[Sariel]] — NPC entity
- [[Rowan]] — NPC entity

## Contradictions
- None identified
