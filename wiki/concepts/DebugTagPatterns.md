---
title: "Debug Tag Patterns"
type: concept
tags: [regex, debugging, content-filtering]
sources: []
last_updated: 2026-04-08
---

## Description
Structured markers embedded in LLM output to separate debug information from narrative content. Two formats exist:

### Old Format (Embedded Tags)
- `[DEBUG_START]` ... `[DEBUG_END]` — wrapper for all debug content
- `[DEBUG_STATE_START]` ... `[DEBUG_STATE_END]` — game state updates
- `[DEBUG_ROLL_START]` ... `[DEBUG_ROLL_END]` — dice roll results
- `[STATE_UPDATES_PROPOSED]` ... `[END_STATE_UPDATES_PROPOSED]` — proposed state changes

### New Format (Structured debug_info)
- JSON object in response with structured `debug_info` field
- More machine-parseable, better for testing

## Used In
- [[hybrid-debug-content-system]] — handles both old and new formats for backward compatibility
- [[llm-response]] — shares pattern definitions
- [[narrative-response-schema]] — JSON cleanup patterns

## Purpose
Allow debug information (dice rolls, state updates, planning blocks) to be included in LLM output while enabling clean extraction for display/logging.
