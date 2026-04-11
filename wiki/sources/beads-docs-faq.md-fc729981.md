---
title: "Beads FAQ"
type: source
tags: [beads, faq, issue-tracker, ai-agents, git-sync, hash-ids]
sources: []
date: 2026-04-07
source_file: docs/faq.md
last_updated: 2026-04-07
---

## Summary
Beads (bd) is a lightweight, git-based issue tracker designed for AI coding agents. It provides typed dependencies with semantics, deterministic ready-work detection, and git-first offline operation with branch-scoped task memory. Hash-based IDs eliminate collisions in multi-agent environments.

## Key Claims

- **Typed Dependencies**: Four types — `blocks`, `related`, `parent-child`, `discovered-from` — each with different behaviors for AI agent task management
- **Deterministic Ready-Work**: `bd ready` computes transitive blocking offline in ~10ms without network
- **Hash-Based IDs**: Eliminates collisions when multiple agents/branches create issues concurrently through progressive length scaling
- **Hierarchical IDs**: Parent-child structure (e.g., `bd-a3f8e9.1`) for epics and subtasks with human-readable numbering
- **Git-First Sync**: No sync server setup required; issues live on branches with branch-scoped task state
- **JSON-First Design**: Every command supports `--json` output for agent integration
- **AI-Resolvable Conflicts**: Automatic collision resolution with dependency consolidation and reference rewriting

## Key Quotes

> "bd is a lightweight, git-based issue tracker designed for AI coding agents."

> "Hash IDs eliminate collisions when multiple agents or branches create issues concurrently."

> "bd automatically extends hash length as your database grows to maintain low collision probability."

## Connections

- [[Beads]] — the main project this FAQ documents
- [[ExclusiveLockProtocol]] — external tools can claim exclusive management preventing daemon interference

## Contradictions

- None identified in this FAQ