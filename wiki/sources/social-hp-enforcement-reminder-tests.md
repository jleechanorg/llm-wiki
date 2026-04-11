---
title: "Social HP Enforcement Reminder Tests"
type: source
tags: [tdd, unit-testing, social-hp, prompt-validation, python, unittest]
source_file: "raw/social-hp-enforcement-reminder-tests.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests validating that the SOCIAL_HP_ENFORCEMENT_REMINDER prompt contains request severity and resistance tracking fields, and that game_state_instruction.md documents these fields.

## Key Claims
- **REMINDER Contains REQUEST SEVERITY**: SOCIAL_HP_ENFORCEMENT_REMINDER includes REQUEST SEVERITY placeholder for dynamic values
- **Field Tracking**: The reminder tracks request_severity and resistance_shown fields for social encounters
- **PROGRESS MECHANICS Section**: Reminder includes a PROGRESS MECHANICS section for mechanics updates
- **Documentation Coverage**: game_state_instruction.md documents both request_severity and resistance_shown fields

## Key Test Functions
- `test_social_hp_enforcement_reminder_mentions_request_severity_and_resistance`: Validates reminder contains all required field references
- `test_game_state_instruction_documents_request_severity_and_resistance`: Validates prompt file documents these fields

## Connections
- [[SocialHPChallenge]] — related to social HP challenge enforcement
- [[GameStateInstruction]] — the prompt file being tested
- [[RequestSeverity]] — the field being validated in the reminder
- [[ResistanceShown]] — the field tracking resistance in social encounters

## Contradictions
- None identified
