---
title: "Banned Names Configuration"
type: source
tags: [worldarchitect, naming, content-quality, llm-generation, configuration]
source_file: "raw/banned-names.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Configuration system preventing 56 overused fantasy names from appearing in WorldArchitect.AI generated content. These names are flagged as forbidden for all character, location, organization, and entity generation due to excessive LLM overuse. The system enforces strict name filtering before any content output.

## Key Claims
- **56-Name Blocklist**: Complete catalog of names forbidden across all world content generation contexts
- **Universal Application**: Applies to NPCs, PCs, locations, organizations, ships, and all entity types
- **No Exceptions Policy**: Even explicit user requests for banned names must be overridden with alternative choices
- **Master Directive Status**: Name filtering takes precedence over all other generation parameters

## Key Quotes
> "These names are overused by LLMs and cannot be used in any world content." — Primary directive rationale

> "NO EXCEPTIONS - even if the user specifically requests a name from CRITICAL NAMING RESTRICTIONS" — Enforcement directive

## Connections
- [[PromptBuildingUtilities]] — likely integrates with prompt construction to enforce name restrictions
- [[NarrativeSampleTokenAnalysis]] — similar quality control for narrative content patterns

## Contradictions
- None identified — this is a configuration file, not a claim subject to contradiction
