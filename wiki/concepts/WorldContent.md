---
title: "World Content"
type: concept
tags: [world-building, content-loading, system-instruction]
sources: [banned-names-visibility-behavior-tests, banned-names-loading-unit-tests]
last_updated: 2026-04-08
---

## Definition
World content refers to the loaded content from world-building files (like banned_names.md) that is used to provide context to AI systems through system instructions.

## Key Characteristics
- Loaded via `world_loader` module
- Used in system instructions for AI character generation
- Must have identifiable structure with section markers
- Should identify source files for traceability

- Contains enforcement directives for game rules

## Related Concepts
- [[SystemInstruction]] — AI instruction content that incorporates world content
- [[BannedNames]] — Specific world content for naming restrictions
- [[WorldLoader]] — Module that loads world content
