---
title: "validate_god_mode_response"
type: entity
tags: [validation, testing, dice-integrity]
sources: ["god-mode-end-to-end-integration-tests"]
last_updated: 2026-04-08
---

## Description
Validation function for god mode responses. Ensures response contains required fields like god_mode_response, session_header, and state_updates.

## Used In
- test_god_mode_end2end.py
- dice_integrity.py

## Connections
- [[GOD MODE]] — validates god mode outputs
- [[NarrativeResponse]] — response schema
