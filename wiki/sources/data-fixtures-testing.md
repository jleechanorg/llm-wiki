---
title: "Data Fixtures for Testing"
type: source
tags: [testing, fixtures, python, worldarchitect, game-state]
source_file: "raw/data-fixtures-testing.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module providing realistic sample data for WorldArchitect.AI testing, including campaign data, game states, story contexts, AI responses, and state updates. Designed for unit and integration tests without requiring real service calls.

## Key Claims
- **Sample Campaign Data**: Test campaign with ID, title, user ID, prompts, and timestamps
- **Game State Structure**: Complete player character data (HP, level, experience, MBTI, alignment), world data (location, weather, time), NPC data with relationship and MBTI, custom campaign state with missions and core memories
- **Story Context Sequences**: Conversation sequences between user and AI with mode, sequence IDs, and timestamps
- **AI Response Scenarios**: Multiple response types for different game situations (normal, HP discrepancy, location mismatch, mission completion, state updates)
- **State Update Patterns**: Sample state update objects for testing state update parsing and application

## Key Quotes
> "Note: This is a data fixtures file, not a test file." — clarifies purpose of module

## Connections
- [[TestConfigurationManagement]] — related test infrastructure
- [[WorldArchitectCodeCoverageReport]] — coverage report shows 0% test coverage for this area
- [[CharacterProfileTemplate]] — uses MBTI and alignment in player character data

## Contradictions
- None identified
