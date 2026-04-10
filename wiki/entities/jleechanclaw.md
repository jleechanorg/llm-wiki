---
title: "jleechanclaw"
type: entity
tags: [jeffrey, project, github, openclaw, delegation]
sources: [smartclaw-routing-delegation-failures-postmortem, jeffrey-github-patterns]
last_updated: 2026-04-09
---

## Overview

`jleechanorg/jleechanclaw` is Jeffrey's primary delegation workflow repository — a heavily customized OpenClaw setup used as the TARGET_REPO for AI agent task delegation after the March 2026 postmortem.

## Purpose

The jleechanclaw repo serves as the **delegation hub** where:
1. Jeffrey assigns tasks to AI agents
2. Agents execute work and push PRs
3. Jeffrey reviews, comments, and routes back for fixes
4. Automation monitors PR state and routes CI failures/comments

## Relationship to worldarchitect.ai

- **worldarchitect.ai** — Primary platform development (PR 5500+)
- **jleechanclaw** — Delegation workflow and OpenClaw agent config

The AO (Agent Orchestrator) system was originally built for worldarchitect.ai but also manages jleechanclaw PRs. The postmortem after March 2026 routing failures led to jleechanclaw being the canonical target for the delegation workflow.

## Postmortem Reference

The "smartclaw-routing-delegation-failures-postmortem.md" document covers:
- Routing failures in agent delegation
- AO session polling issues
- Fix: dedicated `ao-pr-poller.sh` and Python orchestration layer
- Result: `~/tmp/jleechanorg-pr-workspaces/` worktree isolation pattern

## Key Automation

- `ao-pr-poller.sh` — Polls AO sessions for state transitions
- `dispatch_task.py` — Routes tasks to appropriate agents
- `src/orchestration/` — Python layer for complex orchestration
- PR automation across 44 jleechanorg repos

## Related

- [[JeffreyChan]] — Owner
- [[jleechanorg]] — GitHub organization
- [[WorldArchitect]] — Primary platform
- [[OpenClaw]] — Underlying framework
- [[AgentOrchestrator]] — Orchestration system (AgentLoop)
