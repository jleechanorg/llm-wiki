---
title: "Banned Names"
type: concept
tags: [content-filtering, naming-restrictions]
sources: [world-content-loader]
last_updated: 2026-04-08
---

Banned names is a content filtering mechanism in WorldArchitect.AI that prevents the AI from using prohibited names for characters, locations, or entities. Loaded from an optional `banned_names.md` file.

## Behavior
- **Optional**: Missing file returns empty string silently
- **Error on read failure**: If file exists but cannot be read, raises exception
- **Enforcement**: AI must check against list before using any name

## Implementation
The [[WorldContentLoader]] module uses `load_banned_names()` to:
1. Check file existence explicitly (not exception-based)
2. Return empty string if optional file missing
3. Load and strip content if present
4. Include in system instruction with enforcement rules

## Related
- [[SystemInstruction]] - where banned names are enforced
- [[WorldArchitect]] - the project using this concept
