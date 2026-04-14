---
title: "test_banned_names_visibility_v2.py"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/test_banned_names_visibility_v2.py
---

## Summary
Test verifying that AI can identify where banned names come from in world content. Checks structure and behavior (not exact content) to ensure world content has naming restrictions section, source identification, and enforcement directives properly embedded.

## Key Claims
- World content should have clearly marked naming restrictions section with section markers and naming keywords
- Content should identify source of naming restrictions (from .md file)
- Banned names loader should include enforcement directive (must/never + enforcement)
- World content header should exist with section dividers
- Combined world content should be substantial (>1000 chars)

## Key Connections
- [[mvp-site-world-loader]] — Loads world content for system instruction
- [[mvp-site-banned-names]] — Source of naming restrictions

## Test Structure
- `test_world_content_includes_naming_restrictions` — Verifies naming restrictions section exists
- `test_banned_names_loader_returns_content` — Verifies loader returns content with enforcement directive
- `test_world_content_structure_includes_all_sections` — Verifies proper structure and substantial content

## Related Sources
- [[mvp-site-test-banned-names-loading]] — Tests loading of banned names
- [[mvp-site-test-banned-name-prevention-v2]] — Tests prevention behavior