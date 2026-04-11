---
title: "Unit Tests for Banned Names Loading Functionality"
type: source
tags: [python, testing, unittest, world-loader, banned-names, character-generation]
source_file: "raw/banned-names-loading-unit-tests.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python unittest suite verifying that the real banned_names.md file is loaded correctly by the world_loader module. Tests cover file existence, content structure, presence of all primary and extended banned names, and integration with world content loading.

## Key Claims
- **Banned Names File**: The banned_names.md file must exist at the path specified by world_loader.BANNED_NAMES_PATH
- **Content Structure**: load_banned_names returns non-empty string content with proper sections
- **Master Directive**: Content must contain "MASTER DIRECTIVE" and "ABSOLUTELY FORBIDDEN" enforcement language
- **Primary Names**: All 10 primary banned names must be present (Alaric, Blackwood, Corvus, Elara, Kaelen, Lyra, Seraphina, Thorne, Valerius, Isolde)
- **Extended Names**: Extended banned names sample (Aiden, Phoenix, Raven, Luna, Orion, Zephyr) must be present
- **Name Count**: File must contain at least 56 banned names with proper section headers
- **Enforcement Directive**: Content must include "Enforcement Directive" section with "NO EXCEPTIONS" policy
- **World Integration**: load_world_content_for_system_instruction must include banned names section

## Key Quotes
> "Test that banned names are loaded correctly from banned_names.md"

> "assert os.path.exists(world_loader.BANNED_NAMES_PATH)"

## Connections
- [[WorldLoader]] — module being tested for banned names loading
- [[BannedNamesMd]] — the source file being validated
- [[BannedNamePrevention]] — related to AI character generation banned name prevention

## Contradictions
- None identified
