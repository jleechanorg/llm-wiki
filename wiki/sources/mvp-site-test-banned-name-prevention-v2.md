---
title: "test_banned_name_prevention_v2.py"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/test_banned_name_prevention_v2.py
---

## Summary
Test file verifying that AI character generation instructions prevent banned names from being suggested. Checks behavior and structure, not exact content strings, by examining master_directive.md and mechanics_system_instruction.md for pre-generation directives and banned name examples.

## Key Claims
- Master directive should contain pre-generation check behavior to prevent banned names
- Mechanics instruction should have Option 2 character generation with critical directive
- Banned name examples (Alaric, Corvus, Lysander, Seraphina) should be included
- Directive should apply to all characters in campaign
- Version number should be at least 1.5 when prevention was added

## Key Connections
- [[mvp-site-master-directive]] — Source of pre-generation prevention behavior
- [[mvp-site-mechanics-system-instruction]] — Option 2 character generation rules
- [[mvp-site-banned-names]] — List of forbidden character names

## Test Structure
- `test_master_directive_has_prevention_behavior` — Verifies master directive contains mandatory pre-generation check
- `test_mechanics_instruction_has_prevention_behavior` — Verifies mechanics has Option 2 prevention
- `test_version_indicates_changes` — Version should be >= 1.5
- `test_critical_reminders_include_naming` — Critical reminders must address naming checks

## Related Sources
- [[mvp-site-test-banned-names-loading]] — Tests banned names loading
- [[mvp-site-test-banned-names-visibility-v2]] — Tests banned names visibility