---
title: "PR #504: [agento] feat: add ZFC rule to agentRules in agent-orchestrator.yaml"
type: source
tags: []
date: 2026-04-05
source_file: raw/prs-worldai_claw/pr-504.md
sources: []
last_updated: 2026-04-05
---

## Summary
Steve Yegge's Zero-Framework Cognition (ZFC) principle: applications should be thin deterministic shells that delegate ALL judgment, classification, routing, and ranking to AI model calls — never implement heuristics, keyword matching, semantic scoring, or routing logic in application code.

A search of all local branches, PRs, CLAUDE.md, AGENTS.md, and openclaw config found ZERO enforcement of ZFC existed anywhere. This PR adds it to the AO worker agentRules in agent-orchestrator.yaml.

## Metadata
- **PR**: #504
- **Merged**: 2026-04-05
- **Author**: jleechan2015
- **Stats**: +160/-23 in 1 files
- **Labels**: none

## Connections
