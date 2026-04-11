---
title: "Integration Tests for Planning Block Validation and Logging"
type: source
tags: [python, testing, planning-block, integration, logging, validation]
source_file: "raw/test_planning_block_validation_integration.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Integration tests validating the complete flow of `_validate_and_enforce_planning_block` function in `mvp_site.llm_service`. Tests cover missing planning blocks, empty blocks, string format rejection, valid blocks, and crash safety with malformed inputs. The tests verify logging paths for warning, error, and info levels.

## Key Claims
- **Missing planning block**: Logs warning about missing required planning block, adds server warning to `_server_system_warnings` (not `system_warnings` to prevent LLM spoofing)
- **Empty planning block**: Logs warning when thinking/choices are empty, returns original response
- **String format rejected**: Logs error that string planning blocks are no longer supported, only JSON format allowed
- **Valid planning block**: Returns early with info log, no warnings or errors
- **Crash safety**: Function handles None and malformed inputs gracefully

## Key Quotes
> "Verify server warning is added to _server_system_warnings (not system_warnings to prevent LLM spoofing)"

## Connections
- [[NarrativeResponse]] — contains `planning_block` field being validated
- [[GameState]] — provides player_character_data and current_location context
- [[LoggingUtil]] — module providing warning/error/info logging functions

## Contradictions
- None identified
