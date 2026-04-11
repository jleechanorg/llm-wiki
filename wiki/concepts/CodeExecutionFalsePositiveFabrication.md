---
title: "Code Execution False Positive Fabrication"
type: concept
tags: [fabrication, false-positive, code-execution, dice, gemini]
sources: []
last_updated: 2026-04-11
---

## Description
LLM dice rolls incorrectly flagged as fabrication when the model used code execution to generate the result. The fabrication detector uses `code_exec_used=False` + `tool_requests_executed=True` as the fabrication signal, but this is a false positive — the model executed code via the Gemini `code_execution` tool which populates `tool_requests` without setting `code_exec_used=True`.

## Symptoms
- ~17% of dice turns (6/35) flagged as fabrication
- Flagged turns: 41, 48, 49, 54, 62, 68
- All have `code_exec_used=False` + `tool_requests_executed=True`

## Root Cause
Gemini's `code_execution` tool populates `tool_requests` but does not set `code_exec_used=True` in the standard code execution flag field. The fabrication detector interprets any `tool_requests_executed=True` without `code_exec_used=True` as fabrication (model claiming to have run code without actually doing so). This is wrong for the Gemini code execution case because the model DID execute code — just via a different mechanism than expected.

## Evidence
Campaign OZTbL5nJ4tDWqAAVQmPr — dice distribution shows:
- Model produces dice roll results
- Results appear legitimate (correct distributions)
- Evidence shows code was executed but `code_exec_used=False`

## Fix
Update fabrication detection to also check for `code_execution` in `tool_requests` type, or add `gemini_code_execution_used` flag alongside `code_exec_used`.

## Connections
- [[HitDiceTracking]] — dice rolls use this detection
- [[LLM-as-Judge-Pattern]] — fabrication detection is a judge pattern
