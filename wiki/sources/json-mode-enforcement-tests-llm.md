---
title: "JSON Mode Enforcement Tests for LLM Calls"
type: source
tags: [python, testing, unittest, json-mode, llm-service, mocking]
source_file: "raw/json-mode-enforcement-tests-llm.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python unittest file validating that JSON mode is consistently used for all LLM calls in the WorldArchitect application. Tests dependency mocking patterns for firebase_admin, pydantic, cachetools, and google.genai to ensure comprehensive dependency detection and graceful fallback.

## Key Claims
- **JSON Mode Enforcement**: All LLM calls use JSON response mode instead of text mode
- **Dependency Detection**: Tests properly skip when dependencies are unavailable with comprehensive dependency detection
- **Firebase Admin Mocking**: CRITICAL FIX - mocks firebase_admin completely to avoid google.auth namespace conflicts
- **Pydantic Mocking**: Creates mock BaseModel class with proper class behavior for testing
- **Planning Block Normalization**: _choices_by_id function normalizes planning_block choices to id-keyed dict for assertions

## Key Quotes
> "CRITICAL FIX: Mock firebase_admin completely to avoid google.auth namespace conflicts"

## Connections
- [[GameState]] — tested with GameState from mvp_site
- [[continue_story]] — LLM service function being tested for JSON mode
- [[narrative_response_schema]] — schema utilities for creating JSON instructions

## Contradictions
- None identified
