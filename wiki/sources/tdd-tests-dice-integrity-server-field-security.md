---
title: "TDD Tests for Dice Integrity Server Field Security"
type: source
tags: [python, testing, security, dice-integrity, server-fields, tdd]
source_file: "raw/test_dice_integrity_server_field_security.py"
sources: []
last_updated: 2026-04-08
---

## Summary
TDD tests for dice integrity server field security that validate server-prefixed fields (_server_*) cannot be spoofed by LLM responses. Addresses a critical security vulnerability where LLM-provided _server_dice_fabrication_correction was not cleared when code_exec_fabrication=False, allowing fake corrections to be injected into story context.

## Key Claims
- **Server Field Spoofing Prevention**: LLM cannot spoof _server_* prefixed fields — these are server-only fields
- **Fabrication Correction Clearing**: _server_dice_fabrication_correction must be explicitly cleared when code_exec_fabrication=False
- **Security Fix Location**: Fix should be in llm_service.py around line 5207
- **Test Verification**: Tests simulate LLM responses with spoofed server fields and verify they are properly sanitized

## Key Quotes
> "SECURITY VIOLATION: LLM-provided _server_dice_fabrication_correction was not cleared when code_exec_fabrication=False. This allows spoofed corrections to be injected into story context."

## Connections
- [[DiceIntegrity]] — module being secured
- [[ServerFieldSpoofingPrevention]] — security concept being tested
- [[LLMService]] — where the fix should be implemented (llm_service.py line 5207)

## Contradictions
- None identified
