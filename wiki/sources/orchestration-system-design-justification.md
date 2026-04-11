---
title: "Orchestration System Design Justification"
type: source
tags: [orchestration, github, openclaw, python, integration, design]
source_file: "raw/orchestration-system-design-justification.md"
sources: []
last_updated: 2026-04-07
---

## Summary
This document explains why the orchestration layer uses a custom `gh_integration.py` Python wrapper around the `gh` CLI instead of existing tools like PyGithub, GitHubKit, or direct shell scripts. The wrapper provides type-safe orchestration, fail-closed error handling, GraphQL support for review threads, and testability.

## Key Claims
- **gh CLI is transport layer**: Every GitHub API call shells out to `gh` CLI via the `gh()` function — the wrapper is an orchestration-safe interface
- **Type-safe orchestration**: Python dataclasses (`PRInfo`, `MergeReadiness`, `CIStatus`) provide compile-time-like safety when composing multi-step workflows
- **Fail-closed error handling**: CI check failures propagate (never silently return empty), unknown states map to "failed", GraphQL errors block merges
- **GraphQL for unresolved threads**: The `pullRequest.reviewThreads` query via GraphQL exposes thread resolution state not available in `gh pr view --json`
- **Zero Python dependencies**: The repo has zero non-test Python dependencies — adding PyGithub (5+ deps) or GitHubKit (Pydantic + httpx) would violate this constraint

## Key Quotes
> "gh CLI is the transport layer. gh_integration.py is the orchestration-safe interface to it."

## Connections
- [[mctrl]] — owns orchestration state
- [[ai_orch]] — owns execution, handles agent spawning and CLI invocation
- [[OpenClaw]] — provides agent runtime, gateway, and session management in TypeScript
- [[Mission Control]] — evaluated as UI/control-plane only, not authoritative execution path

## Contradictions
- None identified
