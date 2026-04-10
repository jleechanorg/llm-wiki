---
title: "RED-GREEN Testing"
type: concept
tags: [testing, tdd, python]
sources: []
last_updated: 2026-04-08
---

## Description
A testing pattern where tests are written to verify expected behavior (RED - test fails first) before implementing the code to make them pass (GREEN). Used in architectural boundary validation to confirm field format consistency across API layers.

## Application
In the architectural boundary field format validation, RED-GREEN tests confirm:
- Frontend sends "input" field, main.py expects "input"
- main.py translates to "user_input" for MCP protocol
- world_logic.py returns consistent "success"/"error" fields

## Connections
- [[ArchitecturalBoundaryFieldFormatValidation]] — example RED-GREEN test
- [[FieldFormatValidation]] — related concept
