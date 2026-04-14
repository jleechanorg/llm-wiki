---
title: "run_end2end_tests.py"
type: source
tags: []
sources: []
last_updated: 2026-04-14
---

## Summary
Runner script for end-to-end integration tests. Uses unittest to discover and run all test_*.py files in the test directory.

## Key Claims
- Discovers tests using `unittest.TestLoader().discover()` from the test directory
- Runs with verbosity level 2 for detailed output
- Returns exit code 0 on success, 1 on failure
- Mocks only external services (Firestore & Gemini), tests full application flow

## Connections
- [[test_action_resolution_end2end]] — one of the end-to-end tests run
- [[test_character_creation_turn1_end2end]] — another end-to-end test