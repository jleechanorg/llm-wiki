---
title: "Pair Verifier Codex Preflight Failure"
type: concept
tags: [pair-programming, verifier, codex, preflight, failure]
sources: []
last_updated: 2026-04-11
---

## Description
The pair programming verifier agent uses the Codex CLI by default. When Codex's preflight validation fails in the current environment (e.g., missing credentials, wrong working directory), the verifier agent creation aborts — even though the workflow should continue.

## Symptoms
- Pair session fails during verifier launch
- Error: "agent creation aborted" or "preflight validation failed"
- Codex preflight exits non-zero in this environment

## Root Cause
Verifier launch uses Codex CLI with preflight validation that checks environment state (credentials, repo status, etc.). If any check fails, the launch exits non-zero. The pair infrastructure doesn't distinguish between "agent crashed" and "preflight validation failed" — both result in abort.

## Fix
1. Make preflight failure non-fatal for verifier launch (preflight is advisory, not required)
2. Or: add `--skip-preflight` flag to Codex launch config
3. Or: catch preflight failure and fall back to another verifier CLI

## Connections
- [[PreflightGate]] — preflight validation pattern
- [[AgentAdapter]] — CLI adapter that should normalize preflight behavior
