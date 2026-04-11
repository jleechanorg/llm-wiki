---
title: "AI Character Generation Banned Name Prevention Tests"
type: source
tags: [python, testing, unittest, ai-generation, character-naming, prompt-engineering]
source_file: "raw/ai-character-banned-name-prevention-tests.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python unittest suite verifying that AI character generation instructions prevent banned/overused names. Tests check behavior and structure of master directive and mechanics system instruction files for pre-generation name checking.

## Key Claims
- **Pre-generation Directive**: Instructions must contain mandatory pre-generation check behavior
- **Banned Name Examples**: Master directive should include examples of names to avoid (Alaric, Corvus, Lysander, Seraphina)
- **Scope Coverage**: Directive applies to all characters in campaign (NPCs + campaign characters)
- **Mechanics Option 2**: Mechanics instruction includes critical directive for name generation in Option 2
- **Version Enforcement**: Version number must be at least 1.5 when banned name prevention was added
- **Critical Reminders**: Critical reminders section must include naming-related restrictions

## Key Test Components
- **Pre-generation Check Detection**: `_contains_pre_generation_directive()` validates mandatory pre-generation behavior
- **Banned Examples Detection**: `_contains_banned_name_examples()` checks for overused name examples
- **Scope Directive Detection**: `_contains_scope_directive()` verifies all-character coverage
- **Version Validation**: Regex search for `Version: X.Y` format with minimum 1.5
- **Critical Reminders Check**: Validates naming restrictions in critical reminders section

## Test Cases
1. `test_master_directive_has_prevention_behavior` — validates master directive includes pre-generation check
2. `test_mechanics_instruction_has_prevention_behavior` — validates Option 2 has critical naming directive
3. `test_version_indicates_changes` — ensures version >= 1.5
4. `test_critical_reminders_include_naming` — validates naming checks in critical reminders

## Connections
- [[MasterDirective]] — primary file containing banned name prevention instructions
- [[MechanicsSystemInstruction]] — contains Option 2 character generation with naming restrictions
- [[PreGenerationDirective]] — concept for checking before generation
- [[BannedNamePrevention]] — pattern for avoiding overused character names

## Contradictions
- None identified
