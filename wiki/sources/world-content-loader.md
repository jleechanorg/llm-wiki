---
title: "World Content Loader for WorldArchitect.AI"
type: source
tags: [python, world-building, system-instruction, content-loading]
source_file: raw/world_content_loader.md
sources: []
last_updated: 2026-04-08
---

## Summary
Python module for loading world files and creating combined instruction content for the AI system in WorldArchitect.AI. Loads the World of Assiah campaign setting, optional banned names list, and generates a unified system instruction with world consistency rules.

## Key Claims
- **World Directory**: Permanent location at `mvp_site/world/`
- **Optional Banned Names**: Loaded from `banned_names.md` if present; silently returns empty if missing
- **File Caching**: Uses `read_file_cached` for efficient file loading
- **System Instruction Generation**: Combines world content, banned names restrictions, and 5-6 consistency rules
- **Error Handling**: Fails on file existence but read error; missing world file raises exception

## Key Functions
- `load_banned_names()`: Returns banned names content or empty string if optional file missing
- `load_world_content_for_system_instruction()`: Main function that combines all components into system instruction

## World Consistency Rules
1. Character Consistency: Maintain established character personalities and relationships
2. Timeline Integrity: Respect established historical events and chronology
3. Power Scaling: Follow established power hierarchies and combat abilities
4. Cultural Accuracy: Maintain consistency in world cultures and societies
5. Geographic Consistency: Respect established locations and their descriptions
6. Name Restrictions: Never use any name from banned names list

## Connections
- [[WorldArchitect]] - the project this module belongs to
- [[MvpSite]] - the parent module/package
- [[WorldOfAssiah]] - the campaign world being loaded
- [[SystemInstruction]] - the output format for AI prompts
- [[BannedNames]] - the naming restriction system
