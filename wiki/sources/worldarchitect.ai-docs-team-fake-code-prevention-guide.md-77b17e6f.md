---
title: "Team Guide: Fake Code Prevention"
type: source
tags: [fake-code, prevention, orchestration, development, best-practices, decision-framework]
sources: []
source_file: worldarchitect.ai-docs-team-fake-code-prevention_guide.md
date: 2026-04-07
last_updated: 2026-04-07
---

## Summary

Comprehensive adoption guide for an enhanced fake code prevention system that shifts development mindset from "create placeholder and implement later" to "can't implement fully? Use orchestration instead." The system uses a mandatory decision gate ("Can I implement this fully right now?") combined with `/fake3` detection tool and zero-tolerance code review policies.

## Key Claims

- **Decision Gate**: Before writing ANY function, ask "Can I implement this fully right now?" — YES means implement with working code, NO means use orchestration (call existing commands)
- **Mandatory `/fake3`**: Run before every commit to detect fake patterns (TODO, "implement later", placeholder returns)
- **Zero Tolerance**: No placeholder/fake code accepted in code reviews — always suggest orchestration alternatives
- **Orchestration First**: Use existing commands (/commentfetch, /pushl, etc.) before building new functionality
- **Composition Over Implementation**: Build complex functionality by composing simple working parts, not by creating simplified placeholder versions

## Key Quotes

> "Can't implement fully? Use orchestration instead" — core philosophy shift

> "Complex = orchestration of simple working parts" — building complexity through composition

## Connections

- [[Implementation vs Orchestration Decision Framework]] — existing framework this guide builds upon
- [[WorldArchitect.AI]] — the project using this prevention system

## Contradictions

- None detected — this guide reinforces and operationalizes the existing Implementation vs Orchestration Decision Framework already documented in the wiki