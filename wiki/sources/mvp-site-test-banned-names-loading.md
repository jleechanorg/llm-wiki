---
title: "test_banned_names_loading.py"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/test_banned_names_loading.py
---

## Summary
Unit tests verifying that the real banned_names.md file is loaded correctly via world_loader. Tests confirm presence of MASTER DIRECTIVE, all 10 primary banned names, extended names, enforcement directives, and proper file structure with at least 56 names.

## Key Claims
- Banned names file must exist at world_loader.BANNED_NAMES_PATH
- load_banned_names() must return non-empty string content
- Content must contain MASTER DIRECTIVE with ABSOLUTELY FORBIDDEN emphasis
- All 10 primary banned names must be present (Alaric, Blackwood, Corvus, Elara, Kaelen, Lyra, Seraphina, Thorne, Valerius, Isolde)
- Extended names sample should include Aiden, Phoenix, Raven, Luna, Orion, Zephyr
- File must have at least 56 banned names with proper structure

## Key Connections
- [[mvp-site-world-loader]] — Module responsible for loading banned names
- [[mvp-site-banned-names]] — The loaded file containing forbidden names

## Test Structure
- `test_banned_names_file_exists` — Verifies file exists
- `test_load_banned_names_returns_content` — Verifies non-empty string return
- `test_banned_names_contains_master_directive` — Verifies MASTER DIRECTIVE presence
- `test_banned_names_contains_all_primary_names` — Verifies 10 primary names
- `test_banned_names_contains_extended_names` — Verifies extended names
- `test_banned_names_count_verification` — Verifies >= 56 names
- `test_banned_names_enforcement_directive` — Verifies enforcement section
- `test_world_content_includes_banned_names` — Verifies full world content includes banned names

## Related Sources
- [[mvp-site-test-banned-name-prevention-v2]] — Tests prevention behavior
- [[mvp-site-test-banned-names-visibility-v2]] — Tests visibility behavior