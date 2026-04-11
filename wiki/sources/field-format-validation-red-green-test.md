---
title: "Field Format Validation Red-Green Test"
type: source
tags: [python, testing, tdd, red-green, field-format, playwright-mcp]
source_file: "raw/test_field_format_mismatch.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Simple RED-GREEN test validating field format mismatch between world_logic.py and main.py translation layer. Tests verify that story entries use the correct field format (text vs story keys) to prevent empty narrative issues in the API-to-Firestore flow.

## Key Claims
- **Field format mismatch causes empty narrative**: The translation layer expects {"text": content} but world_logic.py outputs {"story": content}
- **Playwright MCP used per coding guidelines**: Test uses Playwright MCP functions instead of direct playwright imports for browser automation
- **RED phase test designed to fail initially**: Test demonstrates the bug before the fix is implemented

## Key Test Cases
1. `test_format_mismatch` - Validates the field format issue with Playwright MCP for browser automation

## Connections
- Related to [[Field Format Validation Red-Green Test]] - this is the source test file
- Uses [[Playwright MCP]] for browser automation
- Tests for [[Field format mismatch]] concept

## Contradictions
- None identified
