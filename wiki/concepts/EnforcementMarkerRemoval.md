---
title: "Enforcement Marker Removal"
type: concept
tags: [refactoring, code-cleanup, testing]
sources: [social-hp-server-enforcement-markers-removed]
last_updated: 2026-04-08
---

## Summary
A refactoring pattern where enforcement logic markers are systematically removed from production code, with test validation ensuring the removal is complete. Used to decouple social HP mechanics from server-side enforcement.

## Key Characteristics
- **Marker-based Detection**: Uses string markers to identify enforcement code locations
- **Test Verification**: Unit tests validate removal completeness
- **Cleanup Scope**: Targets injection, scaling, progress sync, and resistance tracking

## Usage Context
In WorldAI codebase, enforcement markers like SOCIAL_HP_INJECT, SOCIAL_HP_SCALE were removed from llm_service.py as part of cleaning up social HP mechanics that were no longer needed.
